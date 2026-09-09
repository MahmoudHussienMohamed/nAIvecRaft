import os
from Core.Environment import Environment

IMGS_DIR    = os.path.abspath('./assets')
LANDS_DIR   = os.path.join(IMGS_DIR, 'environment', 'lands')
LANDS_PATHS = tuple(os.path.join(LANDS_DIR, f'land{i}.gif') for i in range(15))


class Land(Environment):
    def __init__(self, screen, count: int = 1):
        super().__init__(screen, LANDS_PATHS, count, speed=2)
