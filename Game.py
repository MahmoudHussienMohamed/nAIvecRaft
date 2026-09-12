import time
import turtle
from Core import HUD
from Environment import Lands, Explosions, Waves, Clouds
from Aircrafts import Bullet, Bullets, Enemy, Player, Enemies

TITLE    = "nAIvecRaft"
WATER_BG = "#4779B2"
COLLISION_TOLERANCE = 30

class Game:
    MAX_LIVES         = 3
    INVINCIBLE_FRAMES = 90
    SCORE_PER_KILL    = 100

    def __init__(self, width: int = 1000, height: int = 1000):
        self._init_screen(width, height)
        self.lives            = self.MAX_LIVES
        self.score            = 0
        self.invincible_timer = 0
        self.game_over        = False
        self.bullets    = Bullets(self.win)
        self.explosions = Explosions(self.win)
        self.keys = set()

    def _init_screen(self, width: int, height: int):
        self.win = turtle.Screen()
        self.win.title(TITLE)
        self.win.bgcolor(WATER_BG)
        self.win.setup(width=width, height=height)
        self.win.tracer(0)

    def setup(self):
        self.waves   = Waves(self.win, 10)
        self.land    = Lands(self.win)
        self.clouds  = Clouds(self.win, 5)
        self.enemies = Enemies(self.win, count=7)
        self.player  = Player(self.win, speed=8)

        self.hud = HUD(self.win, max_lives=self.MAX_LIVES)
        self.hud.update(self.score, self.lives)

        self._bind_events()

    def create_bullet(self):
        self.bullets.add(self.player.x, self.player.top)

    def _bind_events(self):
        self.win.listen()

        canvas = self.win.getcanvas()

        canvas.bind(
            "<KeyPress-Left>",
            lambda event: self.keys.add("Left")
        )
        canvas.bind(
            "<KeyPress-Right>",
            lambda event: self.keys.add("Right")
        )

        canvas.bind(
            "<KeyRelease-Left>",
            lambda event: self.keys.discard("Left")
        )
        canvas.bind(
            "<KeyRelease-Right>",
            lambda event: self.keys.discard("Right")
        )

        canvas.bind(
            "<KeyPress-Up>",
            lambda event: self.keys.add("Up")
        )
        canvas.bind(
            "<KeyPress-Down>",
            lambda event: self.keys.add("Down")
        )

        canvas.bind(
            "<KeyRelease-Up>",
            lambda event: self.keys.discard("Up")
        )
        canvas.bind(
            "<KeyRelease-Down>",
            lambda event: self.keys.discard("Down")
        )

        canvas.bind(
            "<KeyPress-space>",
            lambda event: self.keys.add("Space")
        )
        canvas.bind(
            "<KeyRelease-space>",
            lambda event: self.keys.discard("Space")
        )

        self.win.onkeypress(self._quit, 'q')

    def _update_player(self):
        if "Left" in self.keys:
            self.player.move_left()
        elif "Right" in self.keys:
            self.player.move_right()
        else:
            self.player.stop()

        if "Space" in self.keys:
            self.create_bullet()

    def _quit(self):
        self.win.bye()

    def _check_collisions(self):
        if self.invincible_timer > 0:
            return

        for enemy in self.enemies.enemies:
            if not enemy.is_visible():
                continue

            for bullet in self.bullets.bullets:
                if bullet.is_collided_with(enemy):
                    self.on_enemy_shot(enemy, bullet)

            if self.player.is_collided_with(enemy, COLLISION_TOLERANCE):
                self._on_hit()
                return

    def on_enemy_shot(self, enemy: Enemy, bullet: Bullet):
        self.explosions.add(enemy.x, enemy.y, enemy.speed)
        enemy.hide()
        self.bullets.remove([bullet])

        self.score += self.SCORE_PER_KILL
        self.hud.update(self.score, self.lives)

    def _on_hit(self):
        self.lives -= 1
        self.hud.update(self.score, self.lives)

        if self.lives <= 0:
            self.game_over = True

            self.keys.clear()

            self.player.hide()
            self.hud.show_game_over(self.score)
        else:
            self.invincible_timer = self.INVINCIBLE_FRAMES

    def _tick_invincibility(self):
        if self.invincible_timer <= 0:
            self.player.show()
            return

        self.invincible_timer -= 1

        if self.invincible_timer % 6 < 3:
            self.player.hide()
        else:
            self.player.show()

    def play(self):
        while True:

            self.waves.move_down()
            self.land.move_down()
            self.clouds.move_down()
            self.enemies.move_down()
            self.enemies.vibrate()

            if self.game_over:
                self.win.update()
                time.sleep(1 / 60)
                continue

            self.score += 1

            self._update_player()
            self.player.vibrate()
            self.bullets.tick()
            self.bullets.move_up()
            self.bullets.clean()
            self.explosions.move_down()
            self.explosions.clean()

            self._tick_invincibility()
            self._check_collisions()

            if self.score % 60 == 0:
                self.hud.update(self.score, self.lives)

            self.win.update()
            time.sleep(1 / 60)