import arcade
import time
import random

WIDTH = 1600
HEIGHT = 900

DOT_WIDTH = 640
DOT_HEIGHT = 480

INFECTION_RADIUS = 10
CHANCE_OF_INFECTION = 20
CURE_RATE = 1
BASE_TIME = 3000000000
PEOPLE_INFECTED = []

mouse_x = 0
mouse_y = 0
mouse_press = False
ball_pos = []
ball_mvmt = []
history = []
time_elapsed = 0
start = False
reset = True # Button

for i in range(90):
    ball_pos.append([random.randrange(100, DOT_WIDTH-100), random.randrange(100, DOT_HEIGHT-100), arcade.color.BLACK, 0])
    ball_mvmt.append(random.randrange(-2, 3))
for i in range(1):
    ball_pos[0][2] = arcade.color.RED

def dots():
    global ball_mvmt, position, ball_pos, time_elapsed
    for i in range(len(ball_mvmt)):
        if random.randrange(50) == 0:
            ball_mvmt[i] = random.randrange(-2, 3)
            if (ball_mvmt[i] == 0 and random.randrange(2) == 1):
                ball_mvmt[i] = 2
            elif ball_mvmt[i] == 0:
                ball_mvmt[i] = -2
    for i in range(len(ball_pos)):
        k = random.randrange(5)
        if ball_pos[i][0] >= DOT_WIDTH - 100 or ball_pos[i][1] >= DOT_HEIGHT - 100:
            ball_mvmt[i] = -1 * (abs(ball_mvmt[i]))
        if ball_pos[i][1] <= 100 or ball_pos[i][0] <= 100:
            ball_mvmt[i] = abs(ball_mvmt[i])
        if k == 0:
            ball_pos[i][0] += ball_mvmt[i]
            ball_pos[i][1] += ball_mvmt[i]
        elif k == 1:
            ball_pos[i][0] += ball_mvmt[i]
        elif k == 2:
            ball_pos[i][1] += ball_mvmt[i]
        elif k == 3:
            ball_pos[i][0] += ball_mvmt[i]
            ball_pos[i][1] -= ball_mvmt[i]
        else:
            ball_pos[i][0] -= ball_mvmt[i]
            ball_pos[i][1] += ball_mvmt[i]

    for i in range(len(ball_pos)):
        for j in range(i + 1, len(ball_pos)):
            if ball_pos[j][2] != ball_pos[i][2]:
                distance = ((ball_pos[j][0] - ball_pos[i][0]) ** 2 + (ball_pos[j][1] - ball_pos[i][1]) ** 2) ** (1 / 2)
                if distance <= INFECTION_RADIUS:
                    if ball_pos[i][2] == arcade.color.RED and ball_pos[j][2] != arcade.color.GRAY and ball_pos[j][2] != arcade.color.YELLOW:
                        ball_pos[j][2] = arcade.color.RED
                        ball_pos[j][3] = time.time()
                        if [i, j] not in history:
                            history.append([i, j])
                    elif ball_pos[j][2] == arcade.color.RED and ball_pos[i][2] != arcade.color.GRAY and ball_pos[i][2] != arcade.color.YELLOW:
                        ball_pos[i][2] = arcade.color.RED
                        ball_pos[i][3] = time.time()
                        if [j, i] not in history:
                            history.append([j, i])

                    if ball_pos[i] not in PEOPLE_INFECTED:
                        PEOPLE_INFECTED.append(ball_pos[i])

                    if ball_pos[j] not in PEOPLE_INFECTED:
                        PEOPLE_INFECTED.append(ball_pos[j])
    time_elapsed += 0.05
    cure()
    print(history)


def setup():
    arcade.open_window(WIDTH, HEIGHT, "TOHACKS SARS COV-2 Model")
    arcade.set_background_color(arcade.color.LIGHT_STEEL_BLUE)
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
    if start:
        dots()


def cure():
    pop_list = []

    for i in range(len(PEOPLE_INFECTED)):
        if random.randrange(100) < CURE_RATE and time.time() - PEOPLE_INFECTED[i][3] >= BASE_TIME:
            luckyBoi = random.choice(PEOPLE_INFECTED)
            pop_list.append(PEOPLE_INFECTED.index(luckyBoi))
            luckyBoi[2] = arcade.color.GRAY

    for i in range(0, len(pop_list), -1):
        PEOPLE_INFECTED.pop(pop_list[i])
        
        
def mortality():
    pop_list = []

    for i in range(len(PEOPLE_INFECTED)):
        if random.randrange(100) < DEATH_RATE and time.time() - PEOPLE_INFECTED[i][3] >= BASE_TIME:
            unluckyBoi = random.choice(PEOPLE_INFECTED)
            pop_list.append(PEOPLE_INFECTED.index(unluckyBoi))
            unluckyBoi[2] = arcade.color.YELLOW

    for i in range(0, len(pop_list), -1):
        PEOPLE_INFECTED.pop(pop_list[i])
        
        
class Person:
    infected = False
    position = []

    def __init__(self, infected, position):
        self.infected = infected
        self.position = position


def on_draw():
    arcade.start_render()
    # Draw in here...
    # arcade.draw_circle_filled(mouse_x, mouse_y, 25, ball_color)
    arcade.draw_rectangle_filled(WIDTH * 1/5 + 20, HEIGHT / 4 + 30, 640, 480, arcade.color.LIGHT_GREEN)
    for i in range(len(ball_pos)):
        arcade.draw_circle_filled(ball_pos[i][0], ball_pos[i][1], 5, ball_pos[i][2])
    for i in range(len(history)):
        arcade.draw_line(ball_pos[history[i][0]][0], ball_pos[history[i][0]][1], ball_pos[history[i][1]][0], ball_pos[history[i][1]][1], arcade.color.RED)
    arcade.draw_text(f'Number infected: {len(history) + 1}\nTime elapsed: {(time_elapsed):.2f}', 20, HEIGHT / 2 + 200,
                     arcade.color.BLACK, 18)
    if not start:
        draw_button(WIDTH - 100, 50, 100, 30, arcade.color.GREEN, 'Start', arcade.color.LIGHT_GREEN, arcade.color.RED)
    else:
        draw_button(WIDTH - 100, 50, 100, 30, arcade.color.GREEN, 'Pause', arcade.color.LIGHT_GREEN, arcade.color.RED)

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


def draw_button(x, y, button_width, button_height, colour_default, text,
                colour_hover, colour_press):
    global start, reset
    if x + (button_width / 2) > mouse_x > x - (button_width / 2) and \
            y - (button_height / 2) < mouse_y < y + (button_height / 2) and \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, button_width, button_height,
                                     colour_press)
        if not start and reset:
            start = True
            reset = False
        elif start and reset:
            start = False
            reset = False
    elif x + (button_width / 2) > mouse_x > x - (button_width / 2) and \
            y - (button_height / 2) < mouse_y < y + (button_height / 2) and \
            not mouse_press:
        arcade.draw_rectangle_filled(x, y, button_width, button_height,
                                     colour_hover)
        reset = True
    else:
        arcade.draw_rectangle_filled(x, y, button_width, button_height,
                                     colour_default)
    arcade.draw_text_2(text, x-25, y-7, arcade.color.BLACK, 12, bold=True)



if __name__ == '__main__':
    setup()
