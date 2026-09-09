import os
import random
from Environment import Environment

IMGS_DIR        = os.path.abspath('./assets')
LIGHT_WAVES_DIR = os.path.join(IMGS_DIR, 'environment', 'waves', 'light')
WAVE_FRAMES     = tuple(os.path.join(LIGHT_WAVES_DIR, f'_wave_frame_{i}.gif') for i in range(24))


class Wave(Environment):
    def __init__(self, screen, count: int = 20):
        self.fps = 10
        self.cnt = 0
        super().__init__(screen, WAVE_FRAMES, count, speed=2)

    def _on_respawn(self, item):
        pass  # animation counter drives shape changes, not respawn

    def move_down(self):
        self.cnt += 1
        super().move_down()
        if self.cnt >= self.fps:
            for item in self.items:
                item.shape(random.choice(self.imgs))
            self.cnt = 0
