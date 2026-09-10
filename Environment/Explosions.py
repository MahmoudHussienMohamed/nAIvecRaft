import os
import turtle
from Core import AnimationEntity, SPEED

IMGS_DIR    = os.path.abspath('./assets')
PROJECTILES_DIR = os.path.join(IMGS_DIR, 'projectiles')
EXPLOSIONS_FRAMES_NO = 5
EXPLOSIONS_PATHS = tuple(os.path.join(PROJECTILES_DIR, f'explosion{i}.gif') for i in range(EXPLOSIONS_FRAMES_NO))


class Explosion(AnimationEntity):
    def __init__(self, screen: turtle._Screen, default_x: int, default_y: int, speed: int = SPEED):
        self.fps = 10
        self.cnt = 0
        self.current = 0
        super().__init__(screen, EXPLOSIONS_PATHS[0], default_x, default_y, speed, possible_images=EXPLOSIONS_PATHS)

    def move_up(self, dist: int = None):
        self.cnt += 1
        dist = dist or self.speed
        self.turtle.sety(self.y + dist)
        if self.cnt >= self.fps:
            self.current = (self.current + 1) % EXPLOSIONS_FRAMES_NO
            self.update_image(EXPLOSIONS_PATHS[self.current])
            self.cnt = 0
