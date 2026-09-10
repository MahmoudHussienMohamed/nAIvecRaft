import os
import turtle
from Core import AnimationEntity, SPEED

IMGS_DIR    = os.path.abspath('./assets')
PROJECTILES_DIR = os.path.join(IMGS_DIR, 'projectiles')
BULLET_DIR = os.path.join(PROJECTILES_DIR, 'bullet.gif')

class Bullet(AnimationEntity):
    def __init__(self, screen: turtle._Screen, default_x: int, default_y: int, speed: int = SPEED * 3):
        super().__init__(screen, BULLET_DIR, default_x, default_y, speed)
        self.yboundary = self.screen_border_y + self.hheight

    def move_up(self, dist: int = None):
        dist = dist or self.speed
        self.turtle.sety(self.y + dist)