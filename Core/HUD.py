import turtle

FONT_FACE = "Courier"

class HUD:
    # Ratios relative to half-screen height (verified against 1000×1000)
    _PAD       = 0.04    # edge padding for lives/score  →  20 px
    _HUD_Y     = 0.91    # top-bar Y                     → 455 px
    _OVERLAY_Y = 0.16    # game-over title Y             →  80 px
    _SUB_Y     = -0.04   # game-over score Y             → -20 px
    _HINT_Y    = -0.20   # game-over hint Y              → -100 px
    _FONT_SM   = 0.048   # small font                    →  24 pt
    _FONT_MD   = 0.056   # medium font                   →  28 pt
    _FONT_LG   = 0.112   # large font                    →  56 pt

    def __init__(self, screen: turtle._Screen, max_lives: int = 3):
        self.max_lives = max_lives
        hw = screen.window_width()  // 2
        hh = screen.window_height() // 2

        self._font_sm = (FONT_FACE, max(1, int(hh * self._FONT_SM)), "bold")
        self._font_md = (FONT_FACE, max(1, int(hh * self._FONT_MD)), "bold")
        self._font_lg = (FONT_FACE, max(1, int(hh * self._FONT_LG)), "bold")

        pad = hh * self._PAD
        self._lives_t   = self._make_turtle(-hw + pad, hh * self._HUD_Y)
        self._score_t   = self._make_turtle( hw - pad, hh * self._HUD_Y)
        self._overlay_t = self._make_turtle(0,         hh * self._OVERLAY_Y)
        self._sub_t     = self._make_turtle(0,         hh * self._SUB_Y)
        self._hint_t    = self._make_turtle(0,         hh * self._HINT_Y)

    def _make_turtle(self, x: float, y: float) -> turtle.Turtle:
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        t.goto(x, y)
        return t

    def update(self, score: int, lives: int):
        self._lives_t.clear()
        self._lives_t.color("#FF4C4C")
        hearts = "♥ " * lives + "♡ " * (self.max_lives - lives)
        self._lives_t.write(hearts, font=self._font_sm)

        self._score_t.clear()
        self._score_t.color("white")
        self._score_t.write(f"SCORE  {score:06d}", align="right", font=self._font_sm)

    def show_game_over(self, score: int):
        self._overlay_t.color("#FF4C4C")
        self._overlay_t.write("GAME OVER", align="center", font=self._font_lg)

        self._sub_t.color("white")
        self._sub_t.write(f"SCORE  {score:06d}", align="center", font=self._font_md)

        self._hint_t.color("#AAAAAA")
        self._hint_t.write("press  Q  to  quit", align="center", font=self._font_sm)