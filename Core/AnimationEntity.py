import turtle
from PIL import Image

class AnimationEntity:
    def __init__(
            self, screen: turtle._Screen, img_path: str, 
            default_x: int, default_y: int, speed: int,
            xboundary: int = None, yboundary: int = None,
            possible_images: list[str] = None, padding: int = 10
    ):
        self.screen = screen
        self.speed = speed
        self.padding = padding
        self.register_images(img_path, possible_images)
        self.init_turtle(default_x, default_y)
        self.update_image(img_path, xboundary, yboundary)

    def register_images(self, default_img: str, imgs: list[str]):
        self.screen.register_shape(default_img)
        if not imgs: return
        for img in imgs:
            self.screen.register_shape(img)

    def init_turtle(self, default_x: int, default_y: int):
        self.defx = default_x
        self.defy = default_y
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.penup()
        self.goto(default_x, default_y)

    def get_current_image(self):
        return self.turtle.shape()

    def update_image(self, new_img_path: str, xboundary: int = None, yboundary: int = None):
        self.img = new_img_path
        self.width, self.height = Image.open(self.img).size
        self.hwidth = self.width    // 2    # half width
        self.hheight = self.height  // 2    # half height
        self.xboundary = xboundary or (self.screen_border_x - self.hwidth - self.padding) 
        self.yboundary = yboundary or (self.screen_border_y - self.hheight - self.padding)
        self.turtle.shape(self.img)

    def goto(self, x: int, y: int):
        self.turtle.goto(x, y)

    def move(self, distance_x: int, distance_y: int):
        x = self.x + distance_x
        y = self.y + distance_y
        self.goto(x, y)

    def move_left(self, dist: int = None):
        dist = dist or self.speed
        self.turtle.setx(max(self.x - dist, -self.xboundary))

    def move_right(self, dist: int = None):
        dist = dist or self.speed
        self.turtle.setx(min(self.x + dist, self.xboundary))

    def move_up(self, dist: int = None):
        dist = dist or self.speed
        self.turtle.sety(min(self.y + dist, self.yboundary))

    def move_down(self, dist: int = None):
        dist = dist or self.speed
        self.turtle.sety(max(self.y - dist, -self.yboundary))

    def return_to_default(self):
        self.goto(self.defx, self.defy)

    def is_collided_with(self, other: 'AnimationEntity', tolerance: int = 0):
        non_overlapping = (
            self.left + tolerance > other.right or  # self is completely on the right side of other
            self.right - tolerance < other.left or  # self is completely on the left side of other
            self.top - tolerance < other.bottom or  # self is completely under other
            self.bottom + tolerance > other.top     # self is completely above other
        )
        return not non_overlapping

    @property
    def x(self):
        '''Object's middle point's x-coordinate'''
        return self.turtle.xcor()

    @property
    def y(self):
        '''Object's middle point's y-coordinate'''
        return self.turtle.ycor()

    @property
    def left(self):
        '''Object's least x-coordinate'''
        return self.x - self.hwidth
    
    @property
    def right(self):
        '''Object's most x-coordinate'''
        return self.x + self.hwidth

    @property
    def bottom(self):
        '''Object's least y-coordinate'''
        return self.y - self.hheight
    
    @property
    def top(self):
        '''Object's most y-coordinate'''
        return self.y + self.hheight

    @property
    def screen_border_x(self):
        return self.screen.window_width() // 2

    @property
    def screen_border_y(self):
        return self.screen.window_height() // 2