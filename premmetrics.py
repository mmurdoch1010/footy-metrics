import random
import csv
import argparse

# n = number of simulations
number_Sims = 10000
# v = percentage of matches that end in a draw (varies by league) divided by 2
# serie a: .14
# bundesliga: .125
# prem: .12
# la liga: .13
# ligue 1: .1
draw_Variable = .125
# elo values for each team at the start of the season
starting_Elo = {}
# the current table
current_Table = {}
# the list of fixtures for each team
fixtures = {}
# function for loading the current table from a csv
def load_Current_Table_And_Elo(table_Filename):
    with open(table_Filename, 'r', newline='') as file:
        csv_File = csv.reader(file)
        for row in csv_File:
            current_Table[row[0]] = int(row[1])
            starting_Elo[row[0]] = float(row[2])

# function for loading the fixture list from a csv
def load_Fixtures(fixtures_Filename):
    with open(fixtures_Filename, 'r', newline='') as file:
        csv_File = csv.reader(file)
        for row in csv_File:
            for match in row:
                if match != 'x':
                    teams = match.split('-')
                    fixtures[teams[0]][teams[1]] += 1
                    fixtures[teams[1]][teams[0]] += 1

# function for writing the results to a csv file
def write_Results(metric_Standings):
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for team in metric_Standings:
            writer.writerow([team, metric_Standings[team]])


# function for creating the fixture list data structure
def create_Fixture_List():
    for team in current_Table:
        fixtures[team] = {}
        for opponent in current_Table:
            if team != opponent:
                fixtures[team][opponent] = 0

# function for getting the command line arguments
def get_Command_Line_Args():
    parser = argparse.ArgumentParser(description='A program for generating SOR metrics for soccer teams, using elo and monte carlo simulations.')
    parser.add_argument("table_filename", help='A csv file containing the league table, and each teams ELO')
    parser.add_argument("fixtures_filename", help='A csv file containing the list of fixtures for the league')
    parser.add_argument("-w", "--write", action="store_true", help='Option to write output to a csv file')
    args = parser.parse_args()
    return args

# function for running a monte carlo simulation
# team is the key for the team, n is the number of times to run the simulation, v is the percentage of matches that end in a draw / 2
def monte_Carlo(team, n, v):
    # t = target number of points
    t = current_Table[team]
    # s = number of simulations where t points or more were acheived
    s = 0
    # g = array for the probability of winning each match on their fixture
    g = []
    # get each teams fixture and probabilities
    for opponent in fixtures[team]:
        match fixtures[team][opponent]:
            case 1:
                g.append(elo_Win_Prob(starting_Elo[team], starting_Elo[opponent]))
            case 2:
                g.append(elo_Win_Prob(starting_Elo[team], starting_Elo[opponent]))
                g.append(elo_Win_Prob(starting_Elo[team], starting_Elo[opponent]))
    for i in range(n):
        x = 0
        for p in g:
            # random number for opposition performance
            a = random.random()
            # upper limit for a draw
            upperDraw = p + (p * v)
            # lower limit for a draw
            lowerDraw = p - (p * v)
            # if below the lower limit for a draw, our team won
            if a <= lowerDraw:
                x += 3
            # if above the upper limit for a draw, our team lost
            elif a >= upperDraw:
                x += 0
            # if inside the limits, the match was a draw
            else:
                x += 1
        # if we hit our target, increase s
        if x >= t:
            s += 1
    # m is the percentage of times we hit the target
    m = s / n
    return m

# function for calculating win probability for a match based on elo
# team is the elo of the team we are calculating for, opponent is the elo for their opponent
def elo_Win_Prob(team, opponent):
    exponent = (opponent - team) / 400
    return 1 / (1 + (10 ** exponent))
    
# main function for running the monte carlo sim for each team
def main():
    args = get_Command_Line_Args()
    
    load_Current_Table_And_Elo(args.table_filename)
    create_Fixture_List()
    load_Fixtures(args.fixtures_filename)
    
    metric_Standings = {}

    for team in current_Table:
        m = monte_Carlo(team, number_Sims, draw_Variable)
        metric_Standings[team] = m
    
    for team in metric_Standings:
        print(f"{team}: {metric_Standings[team]}")
    
    if args.write:
        write_Results(metric_Standings)
    
if __name__ == "__main__":
    main()
