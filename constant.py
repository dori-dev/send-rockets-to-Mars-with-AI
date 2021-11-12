"""
The  project constant variables
"""

# Standard library imports
from os.path import join, dirname

# Third party imports
from EasyDraw.Vector import Vector

WIDTH = 800  # Screen width
HEIGHT = 600  # Screen height
MARS_Y, EARTH_Y = 60, 80
BH_DIST = 160  # black holes distance

# image directory(it work in any operating system)
IMAGE_DIR = join(dirname(__file__), 'images/')

# number of rockets population
POPULATION_SIZE = 10
# It is like the fuel that every rocket has to travel,
# and it decreases in each frame
ROCKET_LIFESPAN = 200
# Percentage of genes that mutate in each generation
MUTATION_RATE = 0.10

STARS_COUNT = 250
BLACKHOLES_COUNT = 3

MARS_COORDS = Vector(WIDTH // 2, MARS_Y)  # mars coordinates
EARTH_COORDS = Vector(WIDTH // 2, HEIGHT + EARTH_Y)  # earth coordinates
