import os
import random
import turtle
from math import sin
from enum import Enum

IMGS_DIR = os.path.abspath('./assets')
AIRCRAFTS_DIR = os.path.join(IMGS_DIR, 'aircrafts')
ENEMY_DIR = os.path.join(AIRCRAFTS_DIR, 'enemy')

SPEED = 5

class Enemy:

    class Movement(Enum):
        LEFT    = -1
        RIGHT   =  1
        UP      =  0
        DOWN    =  0

    def __init__(self, imgs_dir: str = ENEMY_DIR, speed: float = SPEED):
        self.boundry = 270
        self.frame = 0
        self.init_img_paths(imgs_dir)
        self.init_lookups()
        self.speed = speed
        self.turtle = None

    def init_img_paths(self, imgs_dir: str = ENEMY_DIR):
        self.normal = os.path.join(imgs_dir, 'normal.gif')
        self.left1 = os.path.join(imgs_dir, 'left.gif')
        self.right1 = os.path.join(imgs_dir, 'right.gif')
        self.left2 = self.left1
        self.right2 = self.right1

    def init_lookups(self):
        movt_img_pairs = (
            (Enemy.Movement.LEFT.value,        self.left1),
            (Enemy.Movement.LEFT.value * 2,    self.left2),
            (Enemy.Movement.RIGHT.value,       self.right1),   
            (Enemy.Movement.RIGHT.value * 2,   self.right2),
            (Enemy.Movement.UP.value,          self.normal),
            (Enemy.Movement.DOWN.value,        self.normal),
        )
        self.movt_lookup = dict()
        self.img_lookup = dict()
        for movt, img in movt_img_pairs:
            self.movt_lookup[movt] = img
            self.img_lookup[img] = movt

    def get_movement_from(self, img_path: str):
        return self.img_lookup.get(img_path, Enemy.Movement.UP.value)

    def get_img_from(self, movement_path: str):
        return self.movt_lookup.get(movement_path, self.normal)

    def get_shapes(self):
        return self.normal, self.left1, self.left2, self.right1, self.right2

    def init_turtle(self):
        self.turtle = turtle.Turtle()
        self.turtle.shape(self.normal)
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.goto(0, -self.boundry)
    
    def move_left(self):
        self.handle_shape_change(Enemy.Movement.LEFT)
        x = self.turtle.xcor()
        x = max(x - SPEED, -self.boundry)
        self.turtle.setx(x)

    def move_right(self):
        self.handle_shape_change(Enemy.Movement.RIGHT)
        x = self.turtle.xcor()
        x = min(x + SPEED, self.boundry)
        self.turtle.setx(x)

    def stop(self, *args, **kwargs):
        self.handle_shape_change(Enemy.Movement.UP)

    def get_current_shape(self):
        return self.turtle.shape()

    def handle_shape_change(self, movement: Movement):
        current = self.get_current_shape()
        current_movt = self.get_movement_from(current)
        shift = movement.value
        if movement in (Enemy.Movement.UP, Enemy.Movement.DOWN):
            shift = -current_movt

        elif movement == Enemy.Movement.LEFT:
            if current == self.left1:
                shift *= 2

        elif movement == Enemy.Movement.RIGHT:
            if current == self.right1:
                shift *= 2

        shift = shift + current_movt

        shift = max(shift, Enemy.Movement.LEFT.value * 2)
        shift = min(shift, Enemy.Movement.RIGHT.value * 2)

        shape = self.get_img_from(shift)

        self.turtle.shape(shape)

    def vibrate(self):
        self.frame += 1
        y_shake = sin(self.frame * 0.8) * 1.5
        self.turtle.sety(-self.boundry + y_shake)
        x_shake = y_shake * 0.5
        self.turtle.setx(self.turtle.xcor() + x_shake)
