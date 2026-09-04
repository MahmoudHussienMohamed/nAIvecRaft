# import random
# import turtle


# class Wave:
#     def __init__(self, count=80):
#         self.waves = []

#         for _ in range(count):
#             wave = turtle.Turtle()
#             wave.hideturtle()
#             wave.penup()
#             wave.color("#5B8BC0")
#             wave.goto(
#                 random.randint(-500, 500),
#                 random.randint(-500, 500)
#             )
#             wave.setheading(0)
#             wave.pendown()
#             wave.forward(random.randint(5, 20))
#             wave.penup()

#             self.waves.append(wave)

#     def move_down(self):
#         for wave in self.waves:
#             y = wave.ycor() - 2

#             if y < -500:
#                 y = 500
#                 wave.setx(random.randint(-500, 500))

#             wave.sety(y)

import os
import random
import turtle
from PIL import Image

WAVE_PATH = r"D:\MSc\Advanced Computer Graphics\task\assets\environment\waves\light"

WAVE_FRAMES = [
    f"{WAVE_PATH}\\_wave_frame_{i}.gif"
    for i in range(24)
]


# class Wave:
#     def __init__(self, count=10):
#         self.fps = 10
#         self.cnt = 0
#         self.waves = []

#         for _ in range(count):
#             wave = turtle.Turtle()

#             # Pick a random animation frame
#             wave.shape(random.choice(WAVE_FRAMES))

#             wave.speed(0)
#             wave.penup()
#             wave.goto(
#                 random.randint(-500, 500),
#                 random.randint(-500, 500)
#             )

#             self.waves.append(wave)

# class Wave:
#     def __init__(self, count=10):
#         self.fps = 10
#         self.cnt = 0
#         self.waves = []

#         rows = 5
#         columns = count // rows

#         for i in range(count):
#             wave = turtle.Turtle()

#             wave.shape(random.choice(WAVE_FRAMES))
#             wave.speed(0)
#             wave.penup()

#             row = i // columns
#             column = i % columns

#             # Evenly spaced base position
#             x = -450 + column * (900 / max(columns - 1, 1))
#             y = 400 - row * 180

#             # Add randomness so it doesn't look like a grid
#             x += random.randint(-50, 50)
#             y += random.randint(-40, 40)

#             wave.goto(x, y)

#             self.waves.append(wave)

#     def move_down(self):
#         self.cnt += 1
#         for wave in self.waves:
#             y = wave.ycor() - 2

#             if y < -500:
#                 y = 500
#                 wave.setx(random.randint(-500, 500))
#             if self.cnt >= self.fps:
#                 wave.shape(random.choice(WAVE_FRAMES))
#             wave.sety(y)

#         if self.cnt >= self.fps:
#             self.cnt = 0

class Wave:
    def __init__(self, count=20):
        self.fps = 10
        self.cnt = 0
        self.speed = 2
        self.waves = []

        self.img = WAVE_FRAMES[0]
        self.width, self.height = Image.open(self.img).size

        self.padding = 20

        self.min_x = self.width + self.padding
        self.min_y = self.height + self.padding

        # Create waves
        for _ in range(count):
            position = self.find_valid_position()

            if position is None:
                break

            wave = turtle.Turtle()
            wave.shape(random.choice(WAVE_FRAMES))
            wave.speed(0)
            wave.penup()
            wave.goto(*position)
            self.waves.append(wave)

    def is_valid_position(self, x, y, ignore=None):
        for other in self.waves:
            if other is ignore:
                continue

            if (
                abs(x - other.xcor()) < self.min_x
                and abs(y - other.ycor()) < self.min_y
            ):
                return False

        return True

    def find_valid_position(self):
        """
        Find a non-overlapping position inside the screen.
        """
        for _ in range(5000):
            x = random.randint(
                -500 + self.width // 2,
                500 - self.width // 2
            )

            y = random.randint(
                -500 + self.height // 2,
                500 - self.height // 2
            )

            if self.is_valid_position(x, y):
                return x, y

        return None

    def find_spawn_position(self, wave):
        """
        Find a non-overlapping spawn position above the screen.

        This NEVER loops forever.
        """

        min_x = -500 + self.width // 2
        max_x = 500 - self.width // 2

        # Try several positions in a band above the screen.
        for y in range(
            500 + self.height // 2 + self.padding,
            1000,
            max(1, self.min_y // 2)
        ):

            # Try random X positions
            for _ in range(100):

                x = random.randint(min_x, max_x)

                if self.is_valid_position(
                    x,
                    y,
                    ignore=wave
                ):
                    return x, y

        # Guaranteed fallback:
        # put the wave above every other wave.
        highest_y = max(
            (other.ycor() for other in self.waves if other is not wave),
            default=500
        )

        y = highest_y + self.min_y + self.padding

        # Find the X position with the most horizontal space.
        best_x = min_x
        best_distance = -1

        for x in range(
            int(min_x),
            int(max_x) + 1,
            max(1, self.min_x // 2)
        ):
            distance = min(
                (
                    abs(x - other.xcor())
                    for other in self.waves
                    if other is not wave
                ),
                default=float("inf")
            )

            if distance > best_distance:
                best_distance = distance
                best_x = x

        return best_x, y

    def move_down(self):
        self.cnt += 1

        for wave in self.waves:

            # Smooth movement
            y = wave.ycor() - self.speed

            # Entire sprite has left the bottom
            if y + self.height // 2 < -500:

                x, spawn_y = self.find_spawn_position(wave)

                wave.goto(x, spawn_y)

            else:
                wave.sety(y)

            # Animation
            if self.cnt >= self.fps:
                wave.shape(random.choice(WAVE_FRAMES))

        if self.cnt >= self.fps:
            self.cnt = 0

'''
import os
import random
import turtle
from PIL import Image

IMGS_DIR = os.path.abspath('./assets')
ENV_DIR = os.path.join(IMGS_DIR, 'environment')
WAVES_DIR = os.path.join(ENV_DIR, 'waves')
WAVES_PATHS = tuple(os.path.join(WAVES_DIR, f'wave{i}.gif') for i in range(10))

SPEED = 2

class Wave:
    def __init__(self, speed: float = SPEED):
        self.img = Wave.get_rand_img()
        self.width, self.height = Image.open(self.img).size
        self.speed = speed
        self.turtle = None

    def init_turtle(self, x: float = 0, y: float = 500):
        self.turtle = turtle.Turtle()
        self.turtle.shape(self.img)
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.goto(x, y)

    def get_shapes(self):
        return self.img

    def update(self):
        self.img = Wave.get_rand_img()
        self.width, self.height = Image.open(self.img).size
        self.turtle.shape(self.img)

    def move_down(self):
        y = self.turtle.ycor() - self.speed
        if y - self.height // 2 < -500:
            self.update()
            y = 500 + self.height // 2
            x = random.randint(-500 + self.width // 2, 500 - self.width // 2)
            self.turtle.setx(x)
        self.turtle.sety(y)

    @staticmethod
    def get_rand_img():
        return WAVES_PATHS[random.randint(0, len(WAVES_PATHS) - 1)]'''