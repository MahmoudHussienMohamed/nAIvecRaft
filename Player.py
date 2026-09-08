import os
import turtle
from Aircraft import Aircraft, SPEED

PLAYER_DIR = 'player'

class Player(Aircraft):
    def __init__(self, screen: turtle._Screen, imgs_dir: str = PLAYER_DIR, speed: int = SPEED):
        super().__init__(screen, imgs_dir, default_x=0, default_y=-270, speed=speed)

    def init_img_paths(self, imgs_dir: str = PLAYER_DIR):
        super().init_img_paths(imgs_dir)
        self.left1 = os.path.join(self.dir, 'left1.gif')
        self.right1 = os.path.join(self.dir, 'right1.gif')
        self.left2 = os.path.join(self.dir, 'left2.gif')
        self.right2 = os.path.join(self.dir, 'right2.gif')

    def get_movt_img_pairs(self):
        pairs = super().get_movt_img_pairs()
        pairs = (
            *pairs,
            (Aircraft.Movement.LEFT.value,        self.left1),
            (Aircraft.Movement.LEFT.value * 2,    self.left2),
            (Aircraft.Movement.RIGHT.value,       self.right1),   
            (Aircraft.Movement.RIGHT.value * 2,   self.right2),
        )
        return pairs

    def get_shapes(self):
        shapes = super().get_shapes()
        return *shapes, self.left1, self.left2, self.right1, self.right2

    def handle_shape_change(self, movement: Aircraft.Movement):
        current = self.get_current_image()
        current_movt = self.get_movement_from(current)
        shift = movement.value

        if movement in (Aircraft.Movement.UP, Aircraft.Movement.DOWN):
            shift = -current_movt
        elif movement == Aircraft.Movement.LEFT:
            if current == self.left1:
                shift *= 2
        elif movement == Aircraft.Movement.RIGHT:
            if current == self.right1:
                shift *= 2

        shift = shift + current_movt
        shift = max(shift, Aircraft.Movement.LEFT.value * 2)
        shift = min(shift, Aircraft.Movement.RIGHT.value * 2)

        shape = self.get_img_from(shift)

        self.update_image(shape)