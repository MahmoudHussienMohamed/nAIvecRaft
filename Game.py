import os
import time
import turtle

from Environment.Bullet import Bullet
from Environment.Cloud import Cloud, CLOUDS_PATHS
# from Player import Player
# from Enemy import Enemies
from Aircrafts import Player, Enemies
from HUD import HUD
from Environment.Land import Land, LANDS_PATHS
from Environment.Explosions import Explosion, EXPLOSIONS_PATHS
from Environment.Wave import Wave, WAVE_FRAMES

TITLE    = "nAIvecRaft"
WATER_BG = "#4779B2"
COLLISION_TOLERANCE = 30

PROJECTILES_DIR = os.path.join(os.path.abspath('./assets'), 'projectiles')

class Game:
    MAX_LIVES         = 3
    INVINCIBLE_FRAMES = 90          # 1.5 s at 60 fps

    def __init__(self, width: int = 1000, height: int = 1000):
        self._init_screen(width, height)
        self.lives            = self.MAX_LIVES
        self.score            = 0
        self.invincible_timer = 0
        self.game_over        = False

    def _init_screen(self, width: int, height: int):
        self.win = turtle.Screen()
        self.win.title(TITLE)
        self.win.bgcolor(WATER_BG)
        self.win.setup(width=width, height=height)
        self.win.tracer(0)

    # ------------------------------------------------------------------ setup

    def setup(self):
        # Wave/Cloud/Land manage raw turtles — register shapes manually
        # for shape in WAVE_FRAMES:
        #     self.win.register_shape(shape)
        # for shape in EXPLOSIONS_PATHS:
        #     self.win.register_shape(shape)
        # for shape in LANDS_PATHS:
        #     self.win.register_shape(shape)
        # for shape in CLOUDS_PATHS:
        #     self.win.register_shape(shape)

        # Instantiation order = z-order (later = on top)
        # Player and Enemies auto-register their shapes via AnimationEntity
        self.waves   = Wave(self.win, 10)
        self.land    = Land(self.win)
        self.explosion = Explosion(self.win)
        self.bullet = Bullet(self.win)
        self.clouds  = Cloud(self.win, 5)
        self.enemies = Enemies(self.win, count=5)
        self.player  = Player(self.win, speed=8)

        # HUD always last so text renders above all sprites
        self.hud = HUD(max_lives=self.MAX_LIVES)
        self.hud.update(self.score, self.lives)

        self._bind_events()

    # --------------------------------------------------------------- controls

    def _bind_events(self):
        self.win.listen()
        self.win.onkeypress(self.player.move_left,  'Left')
        self.win.onkeypress(self.player.move_right, 'Right')
        self.win.onkeypress(self.player.stop,       'Up')
        self.win.onkeypress(self.player.stop,       'Down')
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
        for enemy in self.enemies.enemies:
            if self.player.is_collided_with(enemy, COLLISION_TOLERANCE):
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
            self.explosion.move_down()
            self.bullet.move_down()
            self.clouds.move_down()
            self.enemies.move_down()
            self.player.vibrate()
            self.enemies.vibrate()

            self._tick_invincibility()
            self._check_collisions()

            if self.score % 60 == 0:
                self.hud.update(self.score, self.lives)

            self.win.update()
            time.sleep(1 / 60)