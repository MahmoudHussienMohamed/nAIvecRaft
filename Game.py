import time
import turtle
from Cloud import Cloud, CLOUDS_PATHS
from Enemy import Enemy, Enemies
from Land import Land, LANDS_PATHS
from Player import Player
from Wave import Wave, WAVE_FRAMES

TITLE = "nAIvecRaft"
WATER_BG = "#4779B2"

class Game:
    def __init__(self, width: int = 1000, height: int = 1000):
        self.init_screen(width, height)

    def init_screen(self, width: int, height: int):
        self.width = width
        self.height = height
        self.win = turtle.Screen()
        self.win.title(TITLE)
        self.win.bgcolor(WATER_BG)
        self.win.setup(width=self.width, height=self.height)
        self.win.tracer(0)

    def setup(self):
        self.player = Player(speed=8)
        for shape in self.player.get_shapes():
            self.win.register_shape(shape)

        for shape in WAVE_FRAMES:
            self.win.register_shape(shape)
        for shape in LANDS_PATHS:
            self.win.register_shape(shape)
        for shape in CLOUDS_PATHS:
            self.win.register_shape(shape)

        # Instantiation order = z-order (later = on top)
        self.waves = Wave(10)       # ocean surface, bottom layer
        self.land = Land()          # islands, above waves
        self.clouds = Cloud(5)      # clouds, above islands

        # Register enemy shapes before creating Enemies
        sample_enemy = Enemy()
        for shape in sample_enemy.get_shapes():
            self.win.register_shape(shape)

        self.enemies = Enemies(count=5)  # above clouds
        self.player.init_turtle()        # player on top

        self.bind_events()

    def bind_events(self):
        self.win.listen()
        self.win.onkeypress(self.player.move_left, 'Left')
        self.win.onkeypress(self.player.move_right, 'Right')
        self.win.onkeypress(self.player.stop, 'Down')
        self.win.onkeypress(self.player.stop, 'Up')

        canvas = self.win.getcanvas()
        canvas.bind("<KeyRelease-Left>", self.player.stop)
        canvas.bind("<KeyRelease-Right>", self.player.stop)

        self.win.listen()

    def play(self):
        while True:
            self.waves.move_down()
            self.land.move_down()
            self.clouds.move_down()
            self.enemies.move_down()
            self.player.vibrate()
            self.win.update()
            time.sleep(1 / 60)