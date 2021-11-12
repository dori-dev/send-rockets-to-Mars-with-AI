"""Testing the fitness to get the best performance.
"""
from math import ceil
from constant import WIDTH, ROCKET_LIFESPAN

# dist => 0, WIDTH
# reached => False, True
# crashed => False, True
# alive_time = 1, ROCKET_LIFESPAN


def calculate_fitness(dist, reached, crashed, alive_time):
    """calculate the fitness,
    with distance, alive_time, reached and crashed
    These calculations can be modified to obtain different outputs
    """
    # If the distance is greater than WIDTH, it becomes WIDTH
    dist = min(dist, WIDTH)

    # The shorter the distance, the more fitness are calculated
    fitness = WIDTH + 1 - dist
    # Calculating fitness based on when rocket survive
    fitness *= alive_time ** 0.5 + 1
    # If the rocket reached or crashed, the fitness changes
    if reached:
        fitness *= alive_time ** 0.5 * 2
    if crashed:
        fitness /= dist ** 0.5 + 1

    # Return the ceiling of x as an Integral.
    fitness = ceil(fitness)

    return fitness


print(calculate_fitness(800, False, True, 1))
print(calculate_fitness(0, True, False, ROCKET_LIFESPAN))
