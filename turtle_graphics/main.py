from turtle import Screen
from aliens import Aliens, MysteryState
from scoreboard import Scoreboard
from ship import Ship
from shots import Shots
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
X_MOVE_DISTANCE = 8
NUM_LIVES = 4

screen = Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.title("My Space Invaders")
screen.bgcolor('black')
screen.tracer(0, 2)
scoreboard = Scoreboard(NUM_LIVES, screen)
ship = Ship(0, NUM_LIVES, screen)
aliens = Aliens(width=SCREEN_WIDTH)
shots = Shots()


def shoot():
    """Shoot a bullet from the ship's position."""
    shots.shoot_from_ship(pos=ship.get_position())


# control the ship movement and shooting with keys
screen.listen()
screen.onkeypress(lambda delta=-X_MOVE_DISTANCE: ship.control(delta), 'Left')
screen.onkeypress(lambda delta=X_MOVE_DISTANCE: ship.control(delta), 'Right')
screen.onkeypress(key='space', fun=shoot)


def main():
    global ship_delta_x
    ship.draw_line('yellow')

    game_is_on = True
    while game_is_on:
        aliens.move()
        shots.shoot_from_alien(aliens.get_random_alien_position())
        if aliens.get_mystery_state != MysteryState.HIDDEN:
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

        screen.update()

    screen.exitonclick()


if __name__ == '__main__':
    main()
