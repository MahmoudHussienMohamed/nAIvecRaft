import os
import random
import turtle
from math import sin
from enum import Enum
from PIL import Image

IMGS_DIR = os.path.abspath('./assets')
ENV_DIR = os.path.join(IMGS_DIR, 'environment')
LANDS_DIR = os.path.join(ENV_DIR, 'lands')
LANDS_PATHS = tuple(os.path.join(LANDS_DIR, f'land{i}.gif') for i in range(15))

SPEED = 5
class Land:
    def __init__(self, speed: float = SPEED):
        self.img = Land.get_rand_img()
        self.width, self.height = Image.open(self.img).size
        self.boundry = 270
        self.speed = speed
        self.turtle = None

    def init_turtle(self):
        self.turtle = turtle.Turtle()
        self.turtle.shape(self.img)
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.goto(random.randint(-500, 500), -self.boundry)

    def get_shapes(self):
        return self.img

    def update(self):
        self.img = Land.get_rand_img()
        self.width, self.height = Image.open(self.img).size
        self.turtle.shape(self.img)
    
    # def move_left(self):
    #     self.handle_shape_change(Player.Movement.LEFT)
    #     x = self.turtle.xcor()
    #     x = max(x - SPEED, -self.boundry)
    #     self.turtle.setx(x)

    def move_down(self):
        y = self.turtle.ycor()
        print(self.img, y, self.height, y-self.height)
        y = y - self.speed
        if y + self.height // 2 < -500:
            self.update()
            y = 500 + self.height
            self.turtle.setx(random.randint(-500, 500))
        # y = min(y + SPEED, self.boundry)

        self.turtle.sety(y)

    # def stop(self, *args, **kwargs):
    #     self.handle_shape_change(Player.Movement.UP)

    # def get_current_shape(self):
    #     return self.turtle.shape()

    @staticmethod
    def get_rand_img():
        idx = random.randint(0, len(LANDS_PATHS) - 1)
        return LANDS_PATHS[idx]