from pico2d import *
import pico2d.pico2d as pico2d_module
import math
from sdl2 import (
    SDL_PumpEvents,
    SDL_RaiseWindow,
    SDL_SetWindowPosition,
    SDL_SetWindowSize,
    SDL_ShowWindow,
    SDL_WINDOWPOS_CENTERED,
)


def draw_boy(x, y):
    clear_canvas()
    boy.draw(x, y)
    update_canvas()
    delay(0.01)


def move_circle():
    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)

        draw_boy(x, y)


def move_top():
    print("top")
    for x in range(50, 751, 5):
        draw_boy(x, 550)


def move_right():
    print("right")
    for y in range(550, 49, -5):
        draw_boy(750, y)


def move_bottom():
    print("bottom")
    for x in range(750, 49, -5):
        draw_boy(x, 50)


def move_left():
    print("left")
    for y in range(50, 551, 5):
        clear_canvas()
        boy.draw(50, y)
        update_canvas()
        delay(0.01)


def move_rectangle():
    print("move_rectangle")
    move_top()
    move_right()
    move_bottom()
    move_left()


def move_triangle():
    print("move_triangle")



open_canvas(800, 600)
SDL_SetWindowSize(pico2d_module.window, 800, 600)
SDL_SetWindowPosition(pico2d_module.window, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED)
SDL_PumpEvents()
SDL_ShowWindow(pico2d_module.window)
SDL_RaiseWindow(pico2d_module.window)
SDL_PumpEvents()
boy = load_image('../../LEC05/character.png')

while True:
    move_circle()
    move_rectangle()
    move_triangle()

close_canvas()
