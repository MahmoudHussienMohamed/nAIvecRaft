import os
import random
import turtle
from PIL import Image

from Aircraft import Aircraft, AIRCRAFTS_DIR, SPEED

ENEMY_DIR  = 'enemy'
_ENEMY_IMG = os.path.join(AIRCRAFTS_DIR, ENEMY_DIR)


class Enemy(Aircraft):
    def __init__(
            self, screen: turtle._Screen,
            imgs_dir: str  = ENEMY_DIR,
            default_x: int = 0,
            default_y: int = 270,
            speed: int     = SPEED
    ):
        super().__init__(screen, imgs_dir, default_x=default_x, default_y=default_y, speed=speed)

    def init_img_paths(self, imgs_dir: str):
        super().init_img_paths(imgs_dir)
        self.left1  = os.path.join(self.dir, 'left.gif')
        self.right1 = os.path.join(self.dir, 'right.gif')

    def get_movt_img_pairs(self):
        return (
            *super().get_movt_img_pairs(),
            (Aircraft.Movement.LEFT.value,  self.left1),
            (Aircraft.Movement.RIGHT.value, self.right1),
        )

    def get_shapes(self):
        return *super().get_shapes(), self.left1, self.right1

    def handle_shape_change(self, movement: Aircraft.Movement):
        current      = self.get_current_image()
        current_movt = self.get_movement_from(current)
        shift        = movement.value

        if movement in (Aircraft.Movement.UP, Aircraft.Movement.DOWN):
            shift = -current_movt

        shift = shift + current_movt
        shift = max(shift, Aircraft.Movement.LEFT.value)
        shift = min(shift, Aircraft.Movement.RIGHT.value)
        self.update_image(self.get_img_from(shift))


class Enemies:
    def __init__(self, screen: turtle._Screen, count: int = 5, speed: int = SPEED):
        self.screen  = screen
        self.speed   = speed
        self.enemies = []
        self.padding = 30

        self.width, self.height = Image.open(os.path.join(_ENEMY_IMG, 'normal.gif')).size
        self.min_x = self.width  + self.padding
        self.min_y = self.height + self.padding

        for _ in range(count):
            position = self.find_valid_position()
            if position is None:
                break
            enemy = Enemy(screen, default_x=position[0], default_y=position[1])
            self._randomize(enemy)
            self.enemies.append(enemy)

    def _randomize(self, enemy: Enemy):
        enemy.speed        = random.uniform(self.speed * 0.5, self.speed * 1.5)
        enemy.moves        = random.random() < 0.5
        enemy.vx           = random.uniform(-4, 4) if enemy.moves else 0
        enemy.change_timer = random.randint(20, 60)

    def is_valid_position(self, x: float, y: float, ignore: Enemy = None) -> bool:
        for enemy in self.enemies:
            if enemy is ignore:
                continue
            if abs(x - enemy.x) < self.min_x and abs(y - enemy.y) < self.min_y:
                return False
        return True

    def find_valid_position(self):
        for _ in range(5000):
            x = random.randint(-500 + self.width // 2, 500 - self.width // 2)
            y = random.randint(self.height // 2, 500 - self.height // 2)
            if self.is_valid_position(x, y):
                return x, y
        return None

    def find_spawn_position(self, enemy: Enemy):
        min_x = -500 + self.width // 2
        max_x =  500 - self.width // 2

        for y in range(
            500 + self.height // 2 + self.padding,
            1000,
            max(1, self.min_y // 2)
        ):
            for _ in range(100):
                x = random.randint(min_x, max_x)
                if self.is_valid_position(x, y, ignore=enemy):
                    return x, y

        highest_y = max(
            (e.y for e in self.enemies if e is not enemy),
            default=500
        )
        y = highest_y + self.min_y + self.padding

        best_x = min_x
        best_distance = -1
        for x in range(int(min_x), int(max_x) + 1, max(1, self.min_x // 2)):
            distance = min(
                (abs(x - e.x) for e in self.enemies if e is not enemy),
                default=float('inf')
            )
            if distance > best_distance:
                best_distance = distance
                best_x = x

        return best_x, y

    def move_down(self):
        min_x = -500 + self.width // 2
        max_x =  500 - self.width // 2

        for enemy in self.enemies:
            enemy.frame += 1
            y = enemy.y - enemy.speed

            if y + self.height // 2 < -500:
                x, spawn_y = self.find_spawn_position(enemy)
                self._randomize(enemy)
                enemy.goto(x, spawn_y)
                enemy.update_image(enemy.normal)
            else:
                if enemy.moves:
                    enemy.change_timer -= 1
                    if enemy.change_timer <= 0:
                        enemy.vx           = random.uniform(-4, 4)
                        enemy.change_timer = random.randint(20, 60)

                    x = enemy.x + enemy.vx
                    if x < min_x or x > max_x:
                        enemy.vx *= -1
                        x = max(min_x, min(max_x, x))

                    if enemy.vx < -1:
                        enemy.update_image(enemy.left1)
                    elif enemy.vx > 1:
                        enemy.update_image(enemy.right1)
                    else:
                        enemy.update_image(enemy.normal)

                    enemy.turtle.setx(x)

                enemy.turtle.sety(y)