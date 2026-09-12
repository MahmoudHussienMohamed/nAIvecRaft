import turtle

FONT_SM  = ("Courier", 24, "bold")
FONT_MD  = ("Courier", 28, "bold")
FONT_LG  = ("Courier", 56, "bold")

class HUD:
    def __init__(self, max_lives: int = 3):
        self.max_lives = max_lives

        self._lives_t   = self._make_turtle(-480,  455)
        self._score_t   = self._make_turtle( 480,  455)
        self._overlay_t = self._make_turtle(   0,   80)
        self._sub_t     = self._make_turtle(   0,  -20)
        self._hint_t    = self._make_turtle(   0, -100)

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
        self._lives_t.write(hearts, font=FONT_SM)

        self._score_t.clear()
        self._score_t.color("white")
        self._score_t.write(f"SCORE  {score:06d}", align="right", font=FONT_SM)

    def show_game_over(self, score: int):
        self._overlay_t.color("#FF4C4C")
        self._overlay_t.write("GAME OVER", align="center", font=FONT_LG)

        self._sub_t.color("white")
        self._sub_t.write(f"SCORE  {score:06d}", align="center", font=FONT_MD)

        self._hint_t.color("#AAAAAA")
        self._hint_t.write("press  Q  to  quit", align="center", font=FONT_SM)