import os
from Core.Environment import Environment

IMGS_DIR    = os.path.abspath('./assets')
PROJECTILES_DIR = os.path.join(IMGS_DIR, 'projectiles')
BULLET_DIR = os.path.join(PROJECTILES_DIR, 'bullet.gif')
# BULLET_DIR = os.path.join(PROJECTILES_DIR, 'bullet10percent.gif')
# BULLET_DIR = os.path.join(PROJECTILES_DIR, 'bullet20percent.gif')

class Bullet(Environment):
    def __init__(self, screen, count: int = 1):
        super().__init__(screen, [BULLET_DIR], count, speed=2)
