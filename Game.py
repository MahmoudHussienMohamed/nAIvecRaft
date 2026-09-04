import time
import turtle
from Cloud import Cloud, CLOUDS_PATHS
from Enemy import Enemy
from Land import Land, LANDS_PATHS
from Player import Player
from Wave import Wave, WAVE_PATH, WAVE_FRAMES

main_window = turtle.Screen()
main_window.title("falling hearts")
# main_window.bgcolor('skyblue')
# main_window.bgcolor('cadetblue')
main_window.bgcolor('#4779B2')
main_window.setup(width=1000, height=1000)
main_window.tracer(0)

# player = Player(speed=30)
# player = Enemy()

# cloud = Cloud()
land = Land()
# main_window.register_shape(WAVE_PATH)
for shape in WAVE_FRAMES:
    main_window.register_shape(shape)
waves = Wave()


# for shape in player.get_shapes():
#     main_window.register_shape(shape)
# for shape in CLOUDS_PATHS:
#     main_window.register_shape(shape)
for shape in LANDS_PATHS:
    main_window.register_shape(shape)

# player.init_turtle()
# cloud.init_turtle()
land.init_turtle()

main_window.listen()

# main_window.onkeypress(player.move_left, 'Left')
# main_window.onkeypress(player.move_right, 'Right')
# main_window.onkeypress(player.stop, 'Down')
# main_window.onkeypress(player.stop, 'Up')
# canvas = main_window.getcanvas()

# canvas.bind("<KeyRelease-Left>", player.stop)
# canvas.bind("<KeyRelease-Right>", player.stop)

while True:

    # player.vibrate()
    # cloud.move_right()
    land.move_down()
    waves.move_down()

    main_window.update()

    time.sleep(1 / 60)

main_window.mainloop()