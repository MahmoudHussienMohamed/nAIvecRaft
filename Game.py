import time
import turtle
from PIL import Image

from Cloud import Cloud, CLOUDS_PATHS
from Enemy import Enemy, Enemies
from HUD import HUD
from Land import Land, LANDS_PATHS
from Player import Player
from Wave import Wave, WAVE_FRAMES

TITLE    = "nAIvecRaft"
WATER_BG = "#4779B2"

class Game:
    MAX_LIVES          = 3
    INVINCIBLE_FRAMES  = 90          # 1.5 s at 60 fps
    SCORE_PER_SECOND   = 60         # +1 every frame → displayed as pts/sec

    def __init__(self, width: int = 1000, height: int = 1000):
        self._init_screen(width, height)
        self.lives            = self.MAX_LIVES
        self.score            = 0
        self.invincible_timer = 0
        self.game_over        = False

    def _init_screen(self, width: int, height: int):
        self.width = width
        self.height = height
        self.win = turtle.Screen()
        self.win.title(TITLE)
        self.win.bgcolor(WATER_BG)
        self.win.setup(width=self.width, height=self.height)
        self.win.tracer(0)

    # ------------------------------------------------------------------ setup

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

        sample_enemy = Enemy()
        for shape in sample_enemy.get_shapes():
            self.win.register_shape(shape)

        # Instantiation order = z-order (later = on top)
        self.waves   = Wave(10)
        self.land    = Land()
        self.clouds  = Cloud(5)
        self.enemies = Enemies(count=8)
        self.player.init_turtle()

        # HUD always last so it renders above everything
        self.hud = HUD(max_lives=self.MAX_LIVES)
        self.hud.update(self.score, self.lives)

        self._compute_hitbox()
        self._bind_events()

    def _compute_hitbox(self):
        pw, ph = Image.open(self.player.normal).size
        ew, eh = self.enemies.width, self.enemies.height
        # Slightly forgiving: use ~40 % of the combined half-widths
        self._hit_x = (pw + ew) * 0.20
        self._hit_y = (ph + eh) * 0.20

    # --------------------------------------------------------------- controls

    def _bind_events(self):
        self.win.listen()
        self.win.onkeypress(self.player.move_left,  'Left')
        self.win.onkeypress(self.player.move_right, 'Right')
        self.win.onkeypress(self.player.stop,       'Down')
        self.win.onkeypress(self.player.stop,       'Up')
        self.win.onkeypress(self._quit,             'q')

        canvas = self.win.getcanvas()
        canvas.bind("<KeyRelease-Left>",  self.player.stop)
        canvas.bind("<KeyRelease-Right>", self.player.stop)

        self.win.listen()

    def _unbind_movement(self):
        for key in ('Left', 'Right', 'Up', 'Down'):
            self.win.onkeypress(None, key)

    def _quit(self):
        self.win.bye()

    # ------------------------------------------------------------ game logic

    def _check_collisions(self):
        if self.invincible_timer > 0:
            return

        px = self.player.turtle.xcor()
        py = self.player.turtle.ycor()

        for enemy in self.enemies.enemies:
            if (abs(px - enemy.turtle.xcor()) < self._hit_x and
                    abs(py - enemy.turtle.ycor()) < self._hit_y):
                self._on_hit()
                return

    def _on_hit(self):
        self.lives -= 1
        self.hud.update(self.score, self.lives)

        if self.lives <= 0:
            self.game_over = True
            self.player.turtle.hideturtle()
            self._unbind_movement()
            self.hud.show_game_over(self.score)
        else:
            self.invincible_timer = self.INVINCIBLE_FRAMES

    def _tick_invincibility(self):
        if self.invincible_timer <= 0:
            self.player.turtle.showturtle()
            return

        self.invincible_timer -= 1
        # Flash: visible 3 frames, hidden 3 frames
        if self.invincible_timer % 6 < 3:
            self.player.turtle.hideturtle()
        else:
            self.player.turtle.showturtle()

    # ------------------------------------------------------------------- loop

    def play(self):
        while True:
            if self.game_over:
                self.win.update()
                time.sleep(1 / 60)
                continue

            self.score += 1

            self.waves.move_down()
            self.land.move_down()
            self.clouds.move_down()
            self.enemies.move_down()
            self.player.vibrate()

            self._tick_invincibility()
            self._check_collisions()

            if self.score % 60 == 0:          # update HUD once per second
                self.hud.update(self.score, self.lives)

            self.win.update()
            time.sleep(1 / 60)