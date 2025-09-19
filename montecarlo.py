import random
# s = number of simulations where t points or more were acheived
s = 0
# n = number of simulations
n = 10000
# g = array with probability of average team winning each game
g = []
# t = target number of points per simulation
t = 0
# v = percentage of matches that end in a draw (varies by league)
v = .15
for i in range(n):
    x = 0
    for p in g:
        # random number for opposition performance
        a = random.random()
        # upper limit for a draw
        upperDraw = p + (p * v)
        # lower limit for a draw
        lowerDraw = p - (p * v)
        # if below the lower limit for a draw, our average team won
        if a <= lowerDraw:
            x = x + 3
        # if above the upper limit for a draw, our average team lost
        elif a >= upperDraw:
            x = x + 0
        # if inside the limits, the match was a draw
        else:
            x = x + 1
    # if we hit our target, increase s
    if x >= t:
        s = s + 1
# m is the percentage of times we hit the target
m = s / n
print(m)



