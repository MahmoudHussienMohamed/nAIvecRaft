import os
import random
import turtle
from PIL import Image

IMGS_DIR = os.path.abspath('./assets')
ENV_DIR = os.path.join(IMGS_DIR, 'environment')
LANDS_DIR = os.path.join(ENV_DIR, 'lands')
LANDS_PATHS = tuple(os.path.join(LANDS_DIR, f'land{i}.gif') for i in range(15))

SPEED = 2

class Land:
    def __init__(self, count=1):
        self.speed = SPEED
        self.lands = []

        self.width, self.height = Image.open(LANDS_PATHS[0]).size
        self.padding = 20
        self.min_x = self.width + self.padding
        self.min_y = self.height + self.padding

        for _ in range(count):
            position = self.find_valid_position()

            if position is None:
                break

            land = turtle.Turtle()
            land.shape(random.choice(LANDS_PATHS))
            land.speed(0)
            land.penup()
            land.goto(*position)
            self.lands.append(land)

    def is_valid_position(self, x, y, ignore=None):
        for other in self.lands:
            if other is ignore:
                continue
            if abs(x - other.xcor()) < self.min_x and abs(y - other.ycor()) < self.min_y:
                return False
        return True

    def find_valid_position(self):
        for _ in range(5000):
            x = random.randint(-500 + self.width // 2, 500 - self.width // 2)
            y = random.randint(-500 + self.height // 2, 500 - self.height // 2)
            if self.is_valid_position(x, y):
                return x, y
        return None

    def find_spawn_position(self, land):
        min_x = -500 + self.width // 2
        max_x = 500 - self.width // 2

        for y in range(
            500 + self.height // 2 + self.padding,
            1000,
            max(1, self.min_y // 2)
        ):
            for _ in range(100):
                x = random.randint(min_x, max_x)
                if self.is_valid_position(x, y, ignore=land):
                    return x, y

        highest_y = max(
            (other.ycor() for other in self.lands if other is not land),
            default=500
        )
        y = highest_y + self.min_y + self.padding

        best_x = min_x
        best_distance = -1
        for x in range(int(min_x), int(max_x) + 1, max(1, self.min_x // 2)):
            distance = min(
                (abs(x - other.xcor()) for other in self.lands if other is not land),
                default=float("inf")
            )
            if distance > best_distance:
                best_distance = distance
                best_x = x

        return best_x, y

    def move_down(self):
        for land in self.lands:
            y = land.ycor() - self.speed

            if y + self.height // 2 < -500:
                land.shape(random.choice(LANDS_PATHS))
                x, spawn_y = self.find_spawn_position(land)
                land.goto(x, spawn_y)
            else:
                land.sety(y)