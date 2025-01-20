import pygame
from pygame.locals import *
from aliens import Aliens, MysteryState
from scoreboard import Scoreboard
from ship import Ship
from shots import Shots
import time

# initializing pygame
pygame.init()
clock = pygame.time.Clock()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FONT = pygame.font.SysFont('couriernew', 24)
FONT_GAME_OVER = pygame.font.SysFont('couriernew', 48)
NUM_LIVES = 4
FRAME_RATE = 120  # Frames per second

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Space Invaders")

scoreboard = Scoreboard(NUM_LIVES, FONT, FONT_GAME_OVER)
ship = Ship(NUM_LIVES)
aliens = Aliens()
shots = Shots()


def main():
    ship_delta_x = 0
    last_key_press = pygame.time.get_ticks()

    game_is_on = True
    while game_is_on:
        screen.fill((0, 0, 0))  # black background
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_is_on = False
            # control the ship movement and shooting with keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ship_delta_x = -1.7
                elif event.key == pygame.K_RIGHT:
                    ship_delta_x = 1.7
                elif event.key == pygame.K_SPACE:
                    current_time_stamp = pygame.time.get_ticks()
                    if current_time_stamp - last_key_press > 100:  # debounce time in ms
                        shots.shoot_from_ship(pos=ship.get_shot_position())
                        last_key_press = current_time_stamp
            elif event.type == pygame.KEYUP:
                ship_delta_x = 0

        aliens.move()
        ship.control_ship(ship_delta_x)
        shots.shoot_from_alien(aliens.get_random_alien_position())
        if aliens.get_mystery_state() != MysteryState.HIDDEN:
            shots.shoot_from_mystery(aliens.get_mystery_position())
        shots.move()
        scoreboard.increase_score(
            aliens.detect_hit_by_shot_and_get_points(shots))
        scoreboard.update_score()
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

        shots.housekeeping()
        clock.tick(FRAME_RATE)
        pygame.display.update()

    pygame.event.pump()
    pygame.event.wait()
    pygame.quit()


if __name__ == '__main__':
    main()
