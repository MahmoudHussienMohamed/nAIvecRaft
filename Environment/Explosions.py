import turtle
from .Explosion import Explosion

class Explosions:
    def __init__(self, screen: turtle._Screen, explosions: list[Explosion] = None):
        self.screen = screen
        self.explosions = explosions or []

    def add(self, x: int, y: int, speed: int):
        explosion = Explosion(self.screen, x, y, speed)
        self.explosions.append(explosion)

    def move_down(self, dist: int = None):
        for explosion in self.explosions:
            explosion.move_down(dist)

    def remove(self, explosions: list[Explosion]):
        if not explosions:
            return
        for explosion in explosions:
            if explosion.is_visible():
                explosion.hide()
            self.explosions.remove(explosion)

    def clean(self):
        removed_explosions = []
        for explosion in self.explosions:
            if explosion.is_done():
                explosion.hide()
                removed_explosions.append(explosion)

        self.remove(removed_explosions)