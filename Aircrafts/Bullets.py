import turtle

from .Bullet import Bullet

COOLDOWN = 20

class Bullets:
    def __init__(self, screen: turtle._Screen, bullets: list[Bullet] = None):
        self.screen = screen
        self.bullets = bullets or []
        self._cooldown = 0

    def tick(self):
        if self._cooldown > 0:
            self._cooldown -= 1

    def add(self, x: int, y: int):
        if self._cooldown > 0:
            return
        self._cooldown = COOLDOWN
        bullet = Bullet(self.screen, x, y)
        self.bullets.append(bullet)

    def move_up(self, dist: int = None):
        for bullet in self.bullets:
            bullet.move_up(dist)

    def remove(self, bullets: list[Bullet]):
        if not bullets:
            return
        for bullet in bullets:
            if bullet.is_visible():
                bullet.hide()
            self.bullets.remove(bullet)

    def clean(self):
        removed_bullets = []
        for bullet in self.bullets:
            if bullet.y - bullet.hheight >= bullet.yboundary:
                bullet.hide()
                removed_bullets.append(bullet)

        self.remove(removed_bullets)