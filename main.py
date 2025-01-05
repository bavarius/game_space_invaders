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
DISPLAY_DELAY = 0.1  # seconds

screen = Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.title("My Space Invaders")
screen.bgcolor('black')
screen.tracer(0, 0)
scoreboard = Scoreboard(NUM_LIVES, screen)
ship = Ship(0, Y_MOVING_BASE, NUM_LIVES, screen)
aliens = Aliens()
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
    shots.shoot(pos=ship.get_position())


# reacting upon keys
screen.listen()
screen.onkeypress(key='Left', fun=ship.move_left)
screen.onkeypress(key='Right', fun=ship.move_right)
screen.onkeypress(key='space', fun=shoot)


def main():
    draw_line('yellow')
    start = time.time()
    game_is_on = True
    while game_is_on:
        last = time.time()

        if last - start > DISPLAY_DELAY:
            aliens.move()
            ship_position = ship.get_position()
            if aliens.detect_collision_with_ship(ship_position) or shots.detect_collision_with_ship(ship_position):
                if scoreboard.decrease_lives():
                    scoreboard.store_highscore()
                    game_is_on = False
                else:  # game ongoing
                    ship.redraw_ships_left(
                        scoreboard.get_current_num_lives() - 1)
                    shots.reset()
                    aliens.reset()
                    time.sleep(2)
            if aliens.get_num_on_screen() <= 0:  # All aliens are destroyed.
                shots.reset()
                aliens.reset()

            shots.shoot_from_alien(aliens.get_random_alien_position())
            if aliens.mystery_state != MysteryState.HIDDEN:
                shots.shoot_from_mystery(aliens.get_mystery_position())
            shots.move()
            shots_from_ship = shots.get_ship_shot_buffer()
            for shot in shots_from_ship:
                points = aliens.detect_collision_with_shot(shot)
                if points > 0:  # If the returned points are greater than 0, an alien was hit by a shot from the ship.
                    scoreboard.increase_score(points)
                    shot.hideturtle()
            shots.housekeeping(SCREEN_HEIGHT)
            start = time.time()

        screen.update()

    screen.exitonclick()


if __name__ == '__main__':
    main()
