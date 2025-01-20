from turtle import Screen, Turtle
from aliens import Aliens, MysteryState
from scoreboard import Scoreboard
from ship import Ship
from shots import Shots
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
Y_FLOOR = -350
Y_MOVING_BASE = Y_FLOOR + 20  # The ship's bottom line
NUM_LIVES = 4
FRAME_RATE = 120  # Frames per second
TIME_FOR_1_FRAME = 1 / FRAME_RATE  # Seconds

screen = Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.title("My Space Invaders")
screen.bgcolor('black')
screen.tracer(0, 0)
scoreboard = Scoreboard(NUM_LIVES, screen)
ship = Ship(0, Y_MOVING_BASE, NUM_LIVES, screen)
aliens = Aliens(width=SCREEN_WIDTH)
shots = Shots()


def draw_line(color):
    line = Turtle(shape='classic', visible=False)
    line.penup()
    line.color(color)
    line.pensize(2)
    line.teleport(x=SCREEN_WIDTH / -2, y=Y_FLOOR)
    line.setheading(0)
    line.pendown()
    line.speed('fastest')
    line.showturtle()
    line.goto((SCREEN_WIDTH / 2 + 10, Y_FLOOR))


def shoot():
    shots.shoot_from_ship(pos=ship.get_position())


# control the ship movement and shooting with keys
screen.listen()
screen.onkeypress(key='Left', fun=ship.move_left)
screen.onkeypress(key='Right', fun=ship.move_right)
screen.onkeypress(key='space', fun=shoot)


def main():
    draw_line('yellow')

    game_is_on = True
    while game_is_on:
        timer_this_frame = time.time()

        aliens.move()
        shots.shoot_from_alien(aliens.get_random_alien_position())
        if aliens.mystery_state != MysteryState.HIDDEN:
            shots.shoot_from_mystery(aliens.get_mystery_position())
        shots.move()
        scoreboard.increase_score(
            aliens.detect_hit_by_shot_and_get_points(shots))
        if aliens.detect_collision_with_ship_or_bottomline(pos=ship.get_position()) or shots.detect_collision_with_ship(pos=ship.get_position()):
            if scoreboard.decrease_lives_and_check_if_game_over(ship):
                game_is_on = False
            else:  # game ongoing
                shots.reset()
                aliens.reset()
                time.sleep(2)
        if aliens.get_num_on_screen() <= 0:  # All aliens are destroyed.
            shots.reset()
            aliens.reset()

        shots.housekeeping(SCREEN_HEIGHT)

        time_for_this_frame = time.time() - timer_this_frame
        if time_for_this_frame < TIME_FOR_1_FRAME:
            time.sleep(TIME_FOR_1_FRAME - time_for_this_frame)
        screen.update()

    screen.exitonclick()


if __name__ == '__main__':
    main()
