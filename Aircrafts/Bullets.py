import turtle

from .Bullet import Bullet

class Bullets:
    def __init__(self, screen: turtle._Screen, bullets: list[Bullet] = None):
        self.screen = screen
        self.bullets = bullets or []

    def add(self, x: int, y: int):
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
            if bullet.y - 100 >= bullet.yboundary:
                bullet.hide()
                removed_bullets.append(bullet)

        self.remove(removed_bullets)