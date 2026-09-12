import os
from Core.Environment import Environment

IMGS_DIR     = os.path.abspath('./assets')
CLOUDS_DIR   = os.path.join(IMGS_DIR, 'environment', 'clouds')
CLOUDS_PATHS = tuple(os.path.join(CLOUDS_DIR, f'cloud{i}.gif') for i in range(10))


class Clouds(Environment):
    def __init__(self, screen, count: int = 20):
        super().__init__(screen, CLOUDS_PATHS, count, speed=5)
