import os
import random
import turtle
from math import sin
from enum import Enum
from PIL import Image

IMGS_DIR = os.path.abspath('./assets')
ENV_DIR = os.path.join(IMGS_DIR, 'environment')
CLOUDS_DIR = os.path.join(ENV_DIR, 'clouds')
CLOUDS_PATHS = tuple(os.path.join(CLOUDS_DIR, f'cloud{i}.gif') for i in range(10))

SPEED = 5
class Cloud:
    def __init__(self, speed: float = SPEED):
        self.img = Cloud.get_rand_img()
        self.width, self.height = Image.open(self.img).size
        self.boundry = 270
        self.speed = speed
        self.turtle = None

    def init_turtle(self):
        self.turtle = turtle.Turtle()
        self.turtle.shape(self.img)
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.goto(0, -self.boundry)

    def get_shapes(self):
        return self.img

    def update(self):
        self.img = Cloud.get_rand_img()
        self.width, self.height = Image.open(self.img).size
        self.turtle.shape(self.img)
    
    # def move_left(self):
    #     self.handle_shape_change(Player.Movement.LEFT)
    #     x = self.turtle.xcor()
    #     x = max(x - SPEED, -self.boundry)
    #     self.turtle.setx(x)

    def move_right(self):
        x = self.turtle.xcor()
        print(self.img, x, self.width, x-self.width)
        x = x + self.speed
        if x - self.width // 2 > 500:
            self.update()
            x = -500 - self.width
        # x = min(x + SPEED, self.boundry)
        self.turtle.setx(x)

    # def stop(self, *args, **kwargs):
    #     self.handle_shape_change(Player.Movement.UP)

    # def get_current_shape(self):
    #     return self.turtle.shape()

    @staticmethod
    def get_rand_img():
        idx = random.randint(0, len(CLOUDS_PATHS) - 1)
        return CLOUDS_PATHS[idx]