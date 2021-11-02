"""testing the fitness to get the best performance.
"""
from math import ceil
from constant import WIDTH, ROCKET_LIFESPAN

# dist => 0, WIDTH
# reached => False, True
# crashed => False, True
# alive_tick = 1, ROCKET_LIFESPAN


def calculate_fitness(dist, reached, crashed, alive_tick):
    dist = min(dist, WIDTH)

    fitness = WIDTH + 1 - dist
    fitness *= alive_tick ** 0.5 + 1
    if reached:
        fitness *= alive_tick ** 0.5 * 2
    if crashed:
        fitness /= dist ** 0.5 + 1

    fitness = ceil(fitness)

    return fitness


print(calculate_fitness(800, False, True, 1))
print(calculate_fitness(0, True, False, ROCKET_LIFESPAN))
