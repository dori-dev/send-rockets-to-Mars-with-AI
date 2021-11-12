"""
The  project functions
"""

# local imports
from constant import EARTH_COORDS, IMAGE_DIR


def draw_moon(app):
    """create, rotate and draw the moon

    Args:
        app (EasyDraw.EasyDraw): application variable
    """
    canvas = app.canvas  # alias for app.canvas

    # 1- saving current states(without the new moon)
    canvas.push()
    # 2- change translate to earth position
    # because the moon revolves around the earth
    canvas.translate(EARTH_COORDS.x, EARTH_COORDS.y)
    # 3- rotate canvas(but then pop() status just rotate moon),
    # rotate with app.tick(in frame (add 1) to it value)
    canvas.rotate(-app.tick/2)
    # 4- create and draw moon image in screen
    canvas.create_image(230, 0, IMAGE_DIR + 'moon.png', scale=0.3)
    # 5- pop last states
    canvas.pop()


def draw_blackhole(app, blackhole):
    """create, rotate and draw the blackhole

    Args:
        app (EasyDraw.EasyDraw): application variable
        blackhole (Vector): blackhole vector
    """
    canvas = app.canvas  # alias for app.canvas

    # 1- saving current states(without the new blackhole)
    canvas.push()
    # 2- change translate to blackhole position
    canvas.translate(blackhole.x, blackhole.y)
    # 3- rotate canvas(but then pop() canvas just rotate this blackhole),
    # rotate with app.tick(in frame (add 1) to it value)
    canvas.rotate(app.tick/2)
    # 4- create and draw blackhoe image in screen
    canvas.create_image(0, 0, IMAGE_DIR + 'blackhole.png')
    # 5- using saved states
    canvas.pop()
