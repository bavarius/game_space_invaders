import pygame
from distance import get_distance
from random import randint, choice
from enum import Enum

ALIENS_PER_ROW = 11
NUM_ROWS = 5
X_POS_COL0 = 322
TO_LEFT = -1
TO_RIGHT = 1
STANDSTILL = 0
VERTICAL_SPACE = 45
HORIZONTAL_SPACE = 45
INITIAL_SPEED = 1
MAX_SPEED = 2
MYSTERY_SPEED = 1
MYSTERY_APPEARANCE_PROBABILITY = 1000
MYSTERY_POINTS = [100, 200, 500, 750, 1000]
DISTANCE_SHOT_COLLISION = 15.0
DISTANCE_SHIP_COLLISION = 12.0


class MysteryState(Enum):
    HIDDEN = 0
    MOVING_LEFT = 1
    MOVING_RIGHT = 2


class Aliens():
    def __init__(self):
        """Initialize the aliens."""
        self.screen = pygame.display.get_surface()
        self.alien1 = pygame.image.load('resources/alien1.gif').convert()
        self.alien2 = pygame.image.load('resources/alien2.gif').convert()
        self.alien3 = pygame.image.load('resources/alien3.gif').convert()
        self.mystery_surface = pygame.image.load(
            'resources/mystery.gif').convert()
        self.mystery = self.mystery_surface.get_rect(bottomleft=(
            self.screen.get_width(), self.screen.get_height() / 2 - VERTICAL_SPACE * 7))
        self.alien_kinds = [
            # row0 = bottom row
            dict(pic=self.alien1, points=10, y_pos=self.screen.get_height(
            ) / 2 - VERTICAL_SPACE * 2),  # row0
            dict(pic=self.alien1, points=10, y_pos=self.screen.get_height(
            ) / 2 - VERTICAL_SPACE * 3),  # row1
            dict(pic=self.alien2, points=20, y_pos=self.screen.get_height(
            ) / 2 - VERTICAL_SPACE * 4),  # row2
            dict(pic=self.alien2, points=20, y_pos=self.screen.get_height(
            ) / 2 - VERTICAL_SPACE * 5),  # row3
            dict(pic=self.alien3, points=30, y_pos=self.screen.get_height(
            ) / 2 - VERTICAL_SPACE * 6),  # row4
        ]
        self.stage_number = 0
        self.speed = INITIAL_SPEED
        self.moving_direction = TO_LEFT
        self.num_aliens_on_screen = NUM_ROWS * ALIENS_PER_ROW
        # Create array of aliens
        self.alien_surfaces = [[self.alien_kinds[row]['pic']
                                for _ in range(ALIENS_PER_ROW)] for row in range(NUM_ROWS)]
        # Create array to hold all the alien rectangles
        self.aliens = [[None for _ in range(ALIENS_PER_ROW)]
                       for _ in range(NUM_ROWS)]
        for row in range(NUM_ROWS):
            x_pos = X_POS_COL0
            for col in range(ALIENS_PER_ROW):
                self.aliens[row][col] = dict(rect=self.alien_surfaces[row][col].get_rect(
                    center=(x_pos, self.alien_kinds[row]['y_pos'])), visible=True)
                x_pos += HORIZONTAL_SPACE
        self.mystery_state = MysteryState.HIDDEN
        self.mystery_direction = TO_LEFT
        self.display()

    def draw_alien(self, pic, x, y):
        """Draw an alien at the given x and y position."""
        self.screen.blit(pic, (x, y))

    def display(self):
        """Display all aliens and the mystery on the screen."""
        for row in range(NUM_ROWS):
            for col in range(ALIENS_PER_ROW):
                if self.aliens[row][col]['visible'] == True:
                    self.draw_alien(
                        self.alien_surfaces[row][col], self.aliens[row][col]['rect'].x, self.aliens[row][col]['rect'].y)
        if self.mystery_state != MysteryState.HIDDEN:
            self.draw_alien(self.mystery_surface,
                            self.mystery.x, self.mystery.y)

    def reset(self):
        """Reset object positions, states and speed."""
        for row in range(NUM_ROWS):
            x_pos = X_POS_COL0
            for col in range(ALIENS_PER_ROW):
                self.aliens[row][col]['rect'].centerx = x_pos
                self.aliens[row][col]['rect'].centery = self.alien_kinds[row]['y_pos']
                self.aliens[row][col]['visible'] = True
                x_pos += HORIZONTAL_SPACE
        self.mystery.left = self.screen.get_width()
        self.mystery_state = MysteryState.HIDDEN
        self.num_aliens_on_screen = NUM_ROWS * ALIENS_PER_ROW
        self.speed = INITIAL_SPEED  # reset speed

    def change_direction(self, direction):
        """Change moving direction of all aliens"""
        self.moving_direction = direction

    def detect_collision_with_wall(self) -> bool:
        """Let the array of aliens change direction when hitting the wall."""
        if self.moving_direction == TO_LEFT:
            for col in range(ALIENS_PER_ROW):
                for row in range(NUM_ROWS):
                    if self.aliens[row][col]['visible'] == True:
                        if self.aliens[row][col]['rect'].left <= 0:
                            return True
                        else:
                            return False
        elif self.moving_direction == TO_RIGHT:
            for col in range(ALIENS_PER_ROW - 1, -1, -1):
                for row in range(NUM_ROWS):
                    if self.aliens[row][col]['visible'] == True:
                        if self.aliens[row][col]['rect'].right >= self.screen.get_width():
                            return True
                        else:
                            return False

        return False

    def detect_collision_with_ship_or_bottomline(self, pos) -> bool:
        """Detect if an alien hits the ship or the bottom line."""
        for row in range(NUM_ROWS):
            for col in range(ALIENS_PER_ROW):
                if self.aliens[row][col]['visible'] == True:
                    if get_distance(self.aliens[row][col]['rect'].centerx, self.aliens[row][col]['rect'].centery, pos[0], pos[1]) < DISTANCE_SHIP_COLLISION \
                            or self.aliens[row][col]['rect'].bottom > self.screen.get_height():
                        return True

        return False

    def detect_hit_by_shot_and_get_points(self, shots) -> int:
        """Detect if an alien is hit by a shot and return the points."""
        for i, shot in enumerate(shots.ship_shot_buffer):
            if shot == None:
                continue
            for row in range(NUM_ROWS):
                for col in range(ALIENS_PER_ROW):
                    if self.aliens[row][col]['visible'] == True:
                        if get_distance(self.aliens[row][col]['rect'].centerx, self.aliens[row][col]['rect'].bottom, shot.x, shot.top) < DISTANCE_SHOT_COLLISION:
                            self.aliens[row][col]['visible'] = False
                            self.num_aliens_on_screen -= 1
                            shots.ship_shot_buffer[i] = None
                            return self.alien_kinds[row]['points']

            if self.mystery_state != MysteryState.HIDDEN:
                if get_distance(self.mystery.centerx, self.mystery.bottom, shot.x, shot.top) < DISTANCE_SHOT_COLLISION:
                    self.mystery_state = MysteryState.HIDDEN
                    shots.ship_shot_buffer[i] = None
                    return choice(MYSTERY_POINTS)

            self.control_speed()

        return 0

    def get_random_alien_position(self):
        """Return the position of a random alien that is visible."""
        while True:
            row = randint(0, NUM_ROWS - 1)
            col = randint(0, ALIENS_PER_ROW - 1)
            if self.aliens[row][col]['visible'] == True:
                return self.aliens[row][col]['rect'].center

    def get_mystery_position(self):
        """Return the mystery's position."""
        return self.mystery.centerx, self.mystery.centery

    def control_mystery(self):
        """Control the mystery's appearance and movement."""
        if self.mystery_state == MysteryState.HIDDEN:
            if self.num_aliens_on_screen < NUM_ROWS * ALIENS_PER_ROW - 10 and randint(0, MYSTERY_APPEARANCE_PROBABILITY) == 0:
                self.mystery.left = self.screen.get_width()
                self.mystery_direction = TO_LEFT
                self.mystery_state = MysteryState.MOVING_LEFT
        elif self.mystery_state == MysteryState.MOVING_LEFT:
            if self.mystery.left <= 0:
                self.mystery_direction = TO_RIGHT
                self.mystery_state = MysteryState.MOVING_RIGHT
        else:
            if self.mystery.left >= self.screen.get_width():
                self.mystery_direction = STANDSTILL
                self.mystery_state = MysteryState.HIDDEN

    def move_down_one_row(self):
        """Move all aliens down one row."""
        for col in range(ALIENS_PER_ROW):
            for row in range(NUM_ROWS):
                self.aliens[row][col]['rect'].y += VERTICAL_SPACE

    def move_all(self):
        """Move all aliens and the mystery."""
        for row in range(NUM_ROWS):
            for col in range(ALIENS_PER_ROW):
                self.aliens[row][col]['rect'].x += self.moving_direction * self.speed
        self.mystery.move_ip(self.mystery_direction * MYSTERY_SPEED, 0)

    def move(self):
        """Move the aliens and control the mystery."""
        if self.detect_collision_with_wall():
            if self.moving_direction == TO_LEFT:
                self.change_direction(TO_RIGHT)
            else:
                self.change_direction(TO_LEFT)
                self.move_down_one_row()

        self.move_all()
        self.control_mystery()
        self.display()

    def control_speed(self):
        """Control the speed of the aliens."""
        if self.num_aliens_on_screen == 1:
            self.speed = MAX_SPEED
        elif self.num_aliens_on_screen == 3:
            self.speed = MAX_SPEED - 0.2
        elif self.num_aliens_on_screen == 5:
            self.speed = MAX_SPEED - 0.4
        elif self.num_aliens_on_screen == 10:
            self.speed = MAX_SPEED - 0.7
        elif self.num_aliens_on_screen >= 15:
            self.speed = MAX_SPEED - 1

    def get_num_on_screen(self):
        """Return the number of aliens on the screen."""
        return self.num_aliens_on_screen

    def get_mystery_state(self):
        """Return the mystery state (visibility and moving direction)."""
        return self.mystery_state
