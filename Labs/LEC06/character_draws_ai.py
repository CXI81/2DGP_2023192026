from pico2d import *

import math


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
FRAME_DELAY = 0.01

CIRCLE_CENTER = (400, 300)
CIRCLE_RADIUS = 200

RECT_LEFT = 50
RECT_RIGHT = 750
RECT_BOTTOM = 50
RECT_TOP = 550
RECT_STEP = 5

TRIANGLE_A = (100, 100)
TRIANGLE_B = (700, 100)
TRIANGLE_C = (400, 500)
TRIANGLE_STEPS = 100


def circle_points():
    center_x, center_y = CIRCLE_CENTER
    for degree in range(360):
        theta = math.radians(degree)
        x = center_x + CIRCLE_RADIUS * math.cos(theta)
        y = center_y + CIRCLE_RADIUS * math.sin(theta)
        yield x, y


def rectangle_points():
    for x in range(RECT_LEFT, RECT_RIGHT + 1, RECT_STEP):
        yield x, RECT_TOP
    for y in range(RECT_TOP, RECT_BOTTOM - 1, -RECT_STEP):
        yield RECT_RIGHT, y
    for x in range(RECT_RIGHT, RECT_LEFT - 1, -RECT_STEP):
        yield x, RECT_BOTTOM
    for y in range(RECT_BOTTOM, RECT_TOP + 1, RECT_STEP):
        yield RECT_LEFT, y


def line_points(start, end, steps):
    if steps <= 0:
        raise ValueError('steps must be positive')

    x0, y0 = start
    x1, y1 = end
    for step in range(steps + 1):
        t = step / steps
        yield (
            x0 + (x1 - x0) * t,
            y0 + (y1 - y0) * t,
        )


def triangle_points():
    yield from line_points(TRIANGLE_A, TRIANGLE_B, TRIANGLE_STEPS)
    yield from line_points(TRIANGLE_B, TRIANGLE_C, TRIANGLE_STEPS)
    yield from line_points(TRIANGLE_C, TRIANGLE_A, TRIANGLE_STEPS)


def motion_points():
    while True:
        yield from circle_points()
        yield from rectangle_points()
        yield from triangle_points()


def should_quit():
    for event in get_events():
        if event.type == SDL_QUIT:
            return True
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return True
    return False


def draw_frame(character, x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(FRAME_DELAY)


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    character = load_image('../../LEC05/character.png')
    try:
        for x, y in motion_points():
            if should_quit():
                break
            draw_frame(character, x, y)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
