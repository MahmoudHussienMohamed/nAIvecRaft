import os
from Core.Environment import Environment

IMGS_DIR    = os.path.abspath('./assets')
PROJECTILES_DIR = os.path.join(IMGS_DIR, 'projectiles')
EXPLOSIONS_FRAMES_NO = 5
EXPLOSIONS_PATHS = tuple(os.path.join(PROJECTILES_DIR, f'explosion{i}.gif') for i in range(EXPLOSIONS_FRAMES_NO))


class Explosion(Environment):
    def __init__(self, screen, count: int = 1):
        self.fps = 10
        self.cnt = 0
        self.current = 0
        super().__init__(screen, EXPLOSIONS_PATHS, count, speed=2)

    def _on_respawn(self, item):
        pass  # animation counter drives shape changes, not respawn

    def move_down(self):
        self.cnt += 1
        super().move_down()
        if self.cnt >= self.fps:
            for item in self.items:
                self.current = (self.current + 1) % EXPLOSIONS_FRAMES_NO
                item.shape(EXPLOSIONS_PATHS[self.current])
            self.cnt = 0