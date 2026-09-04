import os
import random
import turtle
from math import sin
from enum import Enum
from PIL import Image

IMGS_DIR = os.path.abspath('./assets')
AIRCRAFTS_DIR = os.path.join(IMGS_DIR, 'aircrafts')
ENEMY_DIR = os.path.join(AIRCRAFTS_DIR, 'enemy')

SPEED = 5

class Enemy:

    class Movement(Enum):
        LEFT    = -1
        RIGHT   =  1
        UP      =  0
        DOWN    =  0

    def __init__(self, imgs_dir: str = ENEMY_DIR, speed: float = SPEED):
        self.boundry = 270
        self.frame = 0
        self.init_img_paths(imgs_dir)
        self.init_lookups()
        self.speed = speed
        self.turtle = None

    def init_img_paths(self, imgs_dir: str = ENEMY_DIR):
        self.normal = os.path.join(imgs_dir, 'normal.gif')
        self.left1 = os.path.join(imgs_dir, 'left.gif')
        self.right1 = os.path.join(imgs_dir, 'right.gif')
        self.left2 = self.left1
        self.right2 = self.right1

    def init_lookups(self):
        movt_img_pairs = (
            (Enemy.Movement.LEFT.value,        self.left1),
            (Enemy.Movement.LEFT.value * 2,    self.left2),
            (Enemy.Movement.RIGHT.value,       self.right1),
            (Enemy.Movement.RIGHT.value * 2,   self.right2),
            (Enemy.Movement.UP.value,          self.normal),
            (Enemy.Movement.DOWN.value,        self.normal),
        )
        self.movt_lookup = dict()
        self.img_lookup = dict()
        for movt, img in movt_img_pairs:
            self.movt_lookup[movt] = img
            self.img_lookup[img] = movt

    def get_movement_from(self, img_path: str):
        return self.img_lookup.get(img_path, Enemy.Movement.UP.value)

    def get_img_from(self, movement_path: str):
        return self.movt_lookup.get(movement_path, self.normal)

    def get_shapes(self):
        return self.normal, self.left1, self.left2, self.right1, self.right2

    def init_turtle(self):
        self.turtle = turtle.Turtle()
        self.turtle.shape(self.normal)
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.goto(0, -self.boundry)

    def move_left(self):
        self.handle_shape_change(Enemy.Movement.LEFT)
        x = self.turtle.xcor()
        x = max(x - SPEED, -self.boundry)
        self.turtle.setx(x)

    def move_right(self):
        self.handle_shape_change(Enemy.Movement.RIGHT)
        x = self.turtle.xcor()
        x = min(x + SPEED, self.boundry)
        self.turtle.setx(x)

    def stop(self, *args, **kwargs):
        self.handle_shape_change(Enemy.Movement.UP)

    def get_current_shape(self):
        return self.turtle.shape()

    def handle_shape_change(self, movement: Movement):
        current = self.get_current_shape()
        current_movt = self.get_movement_from(current)
        shift = movement.value
        if movement in (Enemy.Movement.UP, Enemy.Movement.DOWN):
            shift = -current_movt
        elif movement == Enemy.Movement.LEFT:
            if current == self.left1:
                shift *= 2
        elif movement == Enemy.Movement.RIGHT:
            if current == self.right1:
                shift *= 2
        shift = shift + current_movt
        shift = max(shift, Enemy.Movement.LEFT.value * 2)
        shift = min(shift, Enemy.Movement.RIGHT.value * 2)
        shape = self.get_img_from(shift)
        self.turtle.shape(shape)

    def vibrate(self):
        self.frame += 1
        y_shake = sin(self.frame * 0.8) * 1.5
        self.turtle.sety(-self.boundry + y_shake)
        x_shake = y_shake * 0.5
        self.turtle.setx(self.turtle.xcor() + x_shake)


class Enemies:
    def __init__(self, count=5, speed=SPEED):
        self.speed = speed
        self.enemies = []
        self.padding = 30

        sample = Enemy()
        self.width, self.height = Image.open(sample.normal).size
        self.min_x = self.width + self.padding
        self.min_y = self.height + self.padding

        for _ in range(count):
            position = self.find_valid_position()

            if position is None:
                break

            enemy = Enemy()
            enemy.init_turtle()
            enemy.turtle.goto(*position)
            self._randomize(enemy)
            self.enemies.append(enemy)

    def _randomize(self, enemy):
        enemy.speed        = random.uniform(self.speed * 0.5, self.speed * 1.5)
        enemy.moves        = random.random() < 0.5
        enemy.vx           = random.uniform(-4, 4) if enemy.moves else 0
        enemy.change_timer = random.randint(20, 60)

    def get_shapes(self):
        if self.enemies:
            return self.enemies[0].get_shapes()
        return ()

    def is_valid_position(self, x, y, ignore=None):
        for enemy in self.enemies:
            if enemy is ignore:
                continue
            if (abs(x - enemy.turtle.xcor()) < self.min_x and
                    abs(y - enemy.turtle.ycor()) < self.min_y):
                return False
        return True

    def find_valid_position(self):
        for _ in range(5000):
            x = random.randint(-500 + self.width // 2, 500 - self.width // 2)
            y = random.randint(self.height // 2, 500 - self.height // 2)
            if self.is_valid_position(x, y):
                return x, y
        return None

    def find_spawn_position(self, enemy):
        min_x = -500 + self.width // 2
        max_x = 500 - self.width // 2

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
            (e.turtle.ycor() for e in self.enemies if e is not enemy),
            default=500
        )
        y = highest_y + self.min_y + self.padding

        best_x = min_x
        best_distance = -1
        for x in range(int(min_x), int(max_x) + 1, max(1, self.min_x // 2)):
            distance = min(
                (abs(x - e.turtle.xcor()) for e in self.enemies if e is not enemy),
                default=float("inf")
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
            y = enemy.turtle.ycor() - enemy.speed

            if y + self.height // 2 < -500:
                x, spawn_y = self.find_spawn_position(enemy)
                self._randomize(enemy)
                enemy.turtle.goto(x, spawn_y)
                enemy.turtle.shape(enemy.normal)
            else:
                if enemy.moves:
                    enemy.change_timer -= 1
                    if enemy.change_timer <= 0:
                        enemy.vx           = random.uniform(-4, 4)
                        enemy.change_timer = random.randint(20, 60)

                    x = enemy.turtle.xcor() + enemy.vx
                    if x < min_x or x > max_x:
                        enemy.vx *= -1
                        x = max(min_x, min(max_x, x))

                    if enemy.vx < -1:
                        enemy.turtle.shape(enemy.left1)
                    elif enemy.vx > 1:
                        enemy.turtle.shape(enemy.right1)
                    else:
                        enemy.turtle.shape(enemy.normal)

                    enemy.turtle.setx(x)

                enemy.turtle.sety(y)