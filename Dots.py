import arcade
import time
import random

WIDTH = 1280
HEIGHT = 720

INFECTION_RADIUS = 6
CHANCE_OF_INFECTION = 20

mouse_x = 0
mouse_y = 0
mouse_press = False
ball_pos = []
ball_mvmt = []

for i in range(25):
    ball_pos.append([random.randrange(100, WIDTH-100), random.randrange(100, HEIGHT-100), arcade.color.BLACK])
    ball_mvmt.append(random.randrange(-2, 3))
for i in range(1):
    ball_pos[0][2] = arcade.color.RED


def setup():
    arcade.open_window(WIDTH, HEIGHT, "TOHACKS SARS COV-2 Model")
    arcade.set_background_color(arcade.color.WHITE)
    arcade.schedule(update, 1/60)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release
    window.on_mouse_press = on_mouse_press
    window.on_mouse_release = on_mouse_release
    window.on_mouse_motion = on_mouse_motion

    arcade.run()


def update(delta_time):
    global ball_mvmt, position, ball_pos
    for i in range(len(ball_mvmt)):
        if random.randrange(30) == 0:
            ball_mvmt[i] = random.randrange(-2, 3)
    for i in range(len(ball_pos)):
        k = random.randrange(3)
        if 100 < ball_pos[i][1] < HEIGHT - 100 or 100 < ball_pos[i][0] < WIDTH - 100:
            if k == 0:
                ball_pos[i][0] += ball_mvmt[i]
                ball_pos[i][1] += ball_mvmt[i]
            elif k == 1:
                ball_pos[i][0] += ball_mvmt[i]
            else:
                ball_pos[i][1] += ball_mvmt[i]
        


def is_infected(position1, position2):
    if (position2[0] - INFECTION_RADIUS <= position1[0] and position1[0] <= position2[0] + INFECTION_RADIUS) and (position2[1] - INFECTION_RADIUS <= position1[1] and position1[1] <= position2[1] + INFECTION_RADIUS):
        return random.randrange(100) < CHANCE_OF_INFECTION
    else:
        return False


class Person:
    infected = False
    position = []

    def __init__(self, infected, position):
        self.infected = infected
        self.position = position


person1 = Person(False, [50, 50])
person2 = Person(False, [49, 48])

if is_infected(person1.position, person2.position):
    person1.infected = True

print(person1.infected)


def on_draw():
    arcade.start_render()
    # Draw in here...
    # arcade.draw_circle_filled(mouse_x, mouse_y, 25, ball_color)
    for i in range(len(ball_pos)):
        arcade.draw_circle_filled(ball_pos[i][0], ball_pos[i][1], 5, ball_pos[i][2])

def on_key_press(key, modifiers):
    pass


def on_key_release(key, modifiers):
    pass


def on_mouse_press(x, y, button, modifiers):
    global mouse_press
    if button == arcade.MOUSE_BUTTON_LEFT:
        mouse_press = True


def on_mouse_release(x, y, button, modifiers):
    global mouse_press
    if button == arcade.MOUSE_BUTTON_LEFT:
        mouse_press = False


def on_mouse_motion(x, y, dx, dy):
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = y


if __name__ == '__main__':
    setup()
