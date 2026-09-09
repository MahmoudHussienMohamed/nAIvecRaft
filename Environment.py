import random
import turtle
from PIL import Image
from Core.AnimationEntity import AnimationEntity


class Environment(AnimationEntity):
    def __init__(
            self, screen: turtle._Screen,
            imgs: tuple, count: int, speed: float, padding: int = 20
    ):
        # Set screen first — screen_border_x/y and register_images need it
        self.screen  = screen
        self.speed   = speed
        self.padding = padding
        self.imgs    = imgs
        self.items   = []

        self.register_images(imgs[0], imgs)  # inherited from AnimationEntity

        self.width,  self.height  = Image.open(imgs[0]).size
        self.hwidth, self.hheight = self.width // 2, self.height // 2
        self.min_x = self.width  + padding
        self.min_y = self.height + padding

        for _ in range(count):
            position = self.find_valid_position()
            if position is None:
                break
            item = turtle.Turtle()
            item.shape(random.choice(imgs))
            item.speed(0)
            item.penup()
            item.goto(*position)
            self.items.append(item)

    # --------------------------------------------------------- position logic

    def is_valid_position(self, x: float, y: float, ignore=None) -> bool:
        for other in self.items:
            if other is ignore:
                continue
            if abs(x - other.xcor()) < self.min_x and abs(y - other.ycor()) < self.min_y:
                return False
        return True

    def find_valid_position(self):
        bx, by = self.screen_border_x, self.screen_border_y
        for _ in range(5000):
            x = random.randint(-bx + self.hwidth,  bx - self.hwidth)
            y = random.randint(-by + self.hheight, by - self.hheight)
            if self.is_valid_position(x, y):
                return x, y
        return None

    def find_spawn_position(self, item):
        bx, by = self.screen_border_x, self.screen_border_y
        min_x  = -bx + self.hwidth
        max_x  =  bx - self.hwidth

        for y in range(
            by + self.hheight + self.padding,
            by * 2,
            max(1, self.min_y // 2)
        ):
            for _ in range(100):
                x = random.randint(min_x, max_x)
                if self.is_valid_position(x, y, ignore=item):
                    return x, y

        highest_y = max(
            (other.ycor() for other in self.items if other is not item),
            default=by
        )
        y = highest_y + self.min_y + self.padding

        best_x, best_distance = min_x, -1
        for x in range(int(min_x), int(max_x) + 1, max(1, self.min_x // 2)):
            distance = min(
                (abs(x - other.xcor()) for other in self.items if other is not item),
                default=float('inf')
            )
            if distance > best_distance:
                best_distance = distance
                best_x = x

        return best_x, y

    # ------------------------------------------------------ movement + hooks

    def _on_respawn(self, item):
        item.shape(random.choice(self.imgs))

    def move_down(self):
        for item in self.items:
            y = item.ycor() - self.speed
            if y + self.hheight < -self.screen_border_y:
                self._on_respawn(item)
                x, spawn_y = self.find_spawn_position(item)
                item.goto(x, spawn_y)
            else:
                item.sety(y)
