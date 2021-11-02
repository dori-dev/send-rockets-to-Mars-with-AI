"""Send rockets to Mars with artificial intelligence(Genetic algorithm).
"""
# Standard library imports
from random import randint

# Third party imports
from EasyDraw import EasyDraw
from EasyDraw.Vector import Vector

# Local imports
from constant import WIDTH, HEIGHT, MARS_Y, EARTH_Y, BH_DIST
from constant import IMAGE_DIR, MARS_COORDS, EARTH_COORDS
from constant import POPULATION_SIZE, ROCKET_LIFESPAN
from constant import STARS_COUNT, BLACKHOLES_COUNT
from classes import Population
from functions import draw_moon, draw_blackhole


def setup(app):
    """Setup EasyDraw in project

    Args:
        app (EasyDraw.EasyDraw): application variable
    """
    app.lifespan_count = 0

    # make stars
    app.stars = []
    for _ in range(STARS_COUNT):
        app.stars.append((randint(0, WIDTH), randint(0, HEIGHT)))

    # make blackholes
    app.blackholes = []
    for _ in range(BLACKHOLES_COUNT):
        x_pos = randint(BH_DIST, WIDTH-BH_DIST)
        y_pos = randint(MARS_Y+BH_DIST, HEIGHT - (EARTH_Y+BH_DIST))
        app.blackholes.append(Vector(x_pos, y_pos))

    app.population = Population()

    app.generation_index = 1
    app.canvas.font_family('Tahoma 14')
    app.canvas.font_color('white')
    app.canvas.text_anchor('sw')


def draw(app):
    """function for EasyDraw to draw in screen

    Args:
        app (EasyDraw.EasyDraw): application variable
    """
    canvas = app.canvas  # alias for app.canvas
    app.lifespan_count += 1  # lifespan is increased in each frame

    # counting rocket modes
    crashed = 0
    reached = 0
    for rocket in app.population.rockets:
        if rocket.crashed:
            crashed += 1
        if rocket.reached:
            reached += 1

    # checking values, for go to next generation
    if app.lifespan_count >= ROCKET_LIFESPAN or \
            (crashed + reached) == POPULATION_SIZE:

        app.population.evaluate()
        app.population.selection()
        app.generation_index += 1
        app.lifespan_count = 0

    # draw stars in screen
    for star in app.stars:
        canvas.point(star[0], star[1], 'white')

    # draw items
    for blackhole in app.blackholes:
        draw_blackhole(app, blackhole)
    canvas.create_image(EARTH_COORDS, IMAGE_DIR + 'earth.png', scale=0.7)
    canvas.create_image(MARS_COORDS, IMAGE_DIR + 'mars.png', scale=0.5)
    draw_moon(app)

    # calling the rocket's run function
    app.population.run(app)

    # show information
    canvas.text(16, HEIGHT - 16,
                f'Generation: {app.generation_index}\n'
                f'Fuel Storage: {ROCKET_LIFESPAN - app.lifespan_count}\n'
                f'Reached: {reached}\n'
                f'Crashed: {crashed}')


# Launching the EasyDraw
EasyDraw(width=WIDTH,
         height=HEIGHT,
         fps=30,
         background='black',
         title='Rocket to Mars',
         autoClear=True,
         showStats=False,
         setupFunc=setup,
         drawFunc=draw)
