import os
import turtle
from math import sin
from enum import Enum
from .AnimationEntity import AnimationEntity

IMGS_DIR = os.path.abspath('./assets')
AIRCRAFTS_DIR = os.path.join(IMGS_DIR, 'aircrafts')
SPEED = 5

class Aircraft(AnimationEntity):

    class Movement(Enum):
        LEFT    = -1
        RIGHT   =  1
        UP      =  0
        DOWN    =  0

    def __init__(
            self, screen: turtle._Screen, imgs_dir: str, 
            default_x: int = 0, default_y: int = -270, speed: int = SPEED, 
            xboundary: int = None, yboundary: int = None
    ):
        self.init_img_paths(imgs_dir)
        super().__init__(screen, self.normal, default_x, default_y, speed, xboundary, yboundary, self.get_shapes())
        self.boundry = 270
        self.frame = 0
        self.init_lookups()

    def init_img_paths(self, imgs_dir: str):
        self.dir = os.path.join(AIRCRAFTS_DIR, imgs_dir)
        main_img = os.path.join(self.dir, 'normal.gif')
        if not os.path.exists(main_img):
            raise ValueError(f"'{main_img}' is missing!")
        self.normal = main_img

    def get_movt_img_pairs(self):
        return (
        (Aircraft.Movement.UP.value,          self.normal),
        (Aircraft.Movement.DOWN.value,        self.normal),
    )

    def init_lookups(self):
        movt_img_pairs = self.get_movt_img_pairs()
        self.movt_lookup = dict()
        self.img_lookup = dict()
        for movt, img in movt_img_pairs:
            self.movt_lookup[movt] = img
            self.img_lookup[img] = movt

    def get_shapes(self):
        return (self.normal, )

    def get_movement_from(self, img_path: str):
        return self.img_lookup.get(img_path, Aircraft.Movement.UP.value)

    def get_img_from(self, movement: Movement):
        return self.movt_lookup.get(movement, self.normal)

    def move_left(self):
        self.handle_shape_change(Aircraft.Movement.LEFT)
        super().move_left()

    def move_right(self):
        self.handle_shape_change(Aircraft.Movement.RIGHT)
        super().move_right()

    def stop(self, *args, **kwargs):
        self.handle_shape_change(Aircraft.Movement.UP)

    def handle_shape_change(self, movement: Movement):
        raise NotImplementedError()

    def vibrate(self):
        self.frame += 1
        y_shake = sin(self.frame * 0.8) * 1.5
        self.turtle.sety(self.y + y_shake)
        x_shake = y_shake * 0.5
        self.turtle.setx(self.turtle.xcor() + x_shake)