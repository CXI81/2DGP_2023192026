from pico2d import *
import math


def move_circle():
    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)

        clear_canvas()
        boy.draw(x, y)
        update_canvas()
        delay(0.01)


def move_top():
    print("top")
    for x in range(50, 751, 5):
        clear_canvas()
        boy.draw(x, 550)
        update_canvas()
        delay(0.01)


def move_right():
    print("right")


def move_bottom():
    print("bottom")


def move_left():
    print("left")


def move_rectangle():
    print("move_rectangle")
    move_top()
    move_right()
    move_bottom()
    move_left()


def move_triangle():
    print("move_triangle")



open_canvas(800, 600)
boy = load_image('../../LEC05/character.png')

while True:
    move_circle()
    move_rectangle()
    move_triangle()

close_canvas()
