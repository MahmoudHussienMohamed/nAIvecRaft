import os
import turtle
from Core import Aircraft, SPEED

ENEMY_DIR  = 'enemy'

class Enemy(Aircraft):
    def __init__(
            self, screen: turtle._Screen,
            imgs_dir: str  = ENEMY_DIR,
            default_x: int = 0,
            default_y: int = 270,
            speed: int     = SPEED
    ):
        super().__init__(screen, imgs_dir, default_x=default_x, default_y=default_y, speed=speed)

    def init_img_paths(self, imgs_dir: str):
        super().init_img_paths(imgs_dir)
        self.left1  = os.path.join(self.dir, 'left.gif')
        self.right1 = os.path.join(self.dir, 'right.gif')

    def get_movt_img_pairs(self):
        return (
            *super().get_movt_img_pairs(),
            (Aircraft.Movement.LEFT.value,  self.left1),
            (Aircraft.Movement.RIGHT.value, self.right1),
        )

    def get_shapes(self):
        return *super().get_shapes(), self.left1, self.right1

    def handle_shape_change(self, movement: Aircraft.Movement):
        current      = self.get_current_image()
        current_movt = self.get_movement_from(current)
        shift        = movement.value

        if movement in (Aircraft.Movement.UP, Aircraft.Movement.DOWN):
            shift = -current_movt

        shift = shift + current_movt
        shift = max(shift, Aircraft.Movement.LEFT.value)
        shift = min(shift, Aircraft.Movement.RIGHT.value)
        self.update_image(self.get_img_from(shift))