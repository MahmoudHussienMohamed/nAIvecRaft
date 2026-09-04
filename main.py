# import os
# import turtle
# import random
# from playsound3 import playsound

# IMG_DIR = os.path.abspath('./assets')
# AIRCRAFTS_DIR = os.path.join(IMG_DIR, 'aircrafts')
# PLAYER_DIR = os.path.join(AIRCRAFTS_DIR, 'player')

# LEFT_PATH = os.path.join(PLAYER_DIR, 'left1.gif')
# RIGHT_PATH = os.path.join(PLAYER_DIR, 'right1.gif')
# NORMAL_PATH = os.path.join(PLAYER_DIR, 'normal.gif')

# SPEED = 5

# print((LEFT_PATH))
# print(os.path.exists(LEFT_PATH))

# score = 0
# lives = 10

# main_window = turtle.Screen()
# main_window.title("falling hearts")
# # main_window.bgpic('back.gif')
# main_window.setup(width=1000, height=1000)
# # main_window.tracer(0)


# main_window.register_shape(LEFT_PATH)
# main_window.register_shape(RIGHT_PATH)
# main_window.register_shape(NORMAL_PATH)

# # direction = 'stop'

# actor = turtle.Turtle()
# actor.shape('circle')
# actor.shape(NORMAL_PATH)
# actor.speed(0)
# actor.penup()
# actor.goto(0, -270)


# def move_left():
#     # global actor
#     actor.shape(LEFT_PATH)
#     x = actor.xcor()
#     x -= SPEED

#     if x < -270:
#         x = -270

#     actor.setx(x)
    


# def move_right():
#     # global actor
#     actor.shape(RIGHT_PATH)
#     x = actor.xcor()
#     x += SPEED

#     if x > 270:
#         x = 270

#     actor.setx(x)


# def stop_actor():
#     actor.shape(NORMAL_PATH)


# main_window.listen()

# main_window.onkeypress(move_left, 'Left')
# main_window.onkeypress(move_right, 'Right')
# main_window.onkeypress(stop_actor, 'Down')
# main_window.onkeypress(stop_actor, 'Up')


# # while True:
# #     main_window.update()

#     # if direction == 'left':
#     #     actor.shape(LEFT_PATH)

#     #     x = actor.xcor()
#     #     x -= 0.05

#     #     if x < -270:
#     #         x = -270

#     #     actor.setx(x)

#     # if direction == 'right':
#     #     actor.shape(RIGHT_PATH)

#     #     x = actor.xcor()
#     #     x += 0.05

#     #     if x > 270:
#     #         x = 270

#     #     actor.setx(x)

#     # if direction == 'stop':
#     #     actor.shape(NORMAL_PATH)

# # main_window.mainloop()

import time
import turtle
from Enemy import Enemy
from Player import Player

main_window = turtle.Screen()
main_window.title("falling hearts")
# main_window.bgpic('back.gif')
main_window.setup(width=1000, height=1000)
main_window.tracer(0)

# player = Player(speed=30)
player = Enemy()



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