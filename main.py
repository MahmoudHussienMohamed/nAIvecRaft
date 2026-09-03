import time
import turtle
from Player import Player

main_window = turtle.Screen()
main_window.title("falling hearts")
main_window.setup(width=1000, height=1000)
main_window.tracer(0)

player = Player(speed=7)

for shape in player.get_shapes():
    main_window.register_shape(shape)

player.init_turtle()

main_window.listen()

main_window.onkeypress(player.move_left, 'Left')
main_window.onkeypress(player.move_right, 'Right')
main_window.onkeypress(player.stop, 'Down')
main_window.onkeypress(player.stop, 'Up')
canvas = main_window.getcanvas()

canvas.bind("<KeyRelease-Left>", player.stop)
canvas.bind("<KeyRelease-Right>", player.stop)

while True:

    player.vibrate()

    main_window.update()

    time.sleep(1 / 60)

main_window.mainloop()