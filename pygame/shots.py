import pygame
from distance import get_distance
import time

NUM_MAX_SHOTS_SHIP = 7  # shots on screen at a time
NUM_MAX_SHOTS_ALIENS = 10  # alien shots on screen at a time
NUM_MAX_SHOTS_MYSTERY = 18  # mystery shots on screen at a time
HEADING_NORTH = 90
HEADING_SOUTH = 270
SHIP_SHOT_SPEED = 3.0
ALIEN_SHOT_SPEED = 1.0
ALIEN_SHOT_INTERVAL = 0.5
MYSTERY_SHOT_INTERVAL = 0.6
SHOT_INIT_POS_X = -20
SHOT_INIT_POS_Y = -20
SHOT_WIDTH = 2
SHOT_HEIGHT = 10
DISTANCE_SHIP_COLLISION = 19.0


class Shots():
    def __init__(self):
        """Initialize the shot buffers and the time."""
        self.screen = pygame.display.get_surface()
        self.ship_shot_buffer = [None for _ in range(NUM_MAX_SHOTS_SHIP)]
        self.alien_shot_buffer = [None for _ in range(NUM_MAX_SHOTS_ALIENS)]
        self.mystery_shot_buffer = [None for _ in range(NUM_MAX_SHOTS_MYSTERY)]
        self.time = time.time()
        self.time_mystery_shots = time.time()

    def reset(self):
        """Reset the shot buffers."""
        for i in range(NUM_MAX_SHOTS_SHIP):
            self.ship_shot_buffer[i] = None
        for i in range(NUM_MAX_SHOTS_ALIENS):
            self.alien_shot_buffer[i] = None
        for i in range(NUM_MAX_SHOTS_MYSTERY):
            self.mystery_shot_buffer[i] = None

    def find_free_shot_ship(self):
        """Find the 1st free buffer slot in the ship's shot buffer."""
        for i in range(NUM_MAX_SHOTS_SHIP):
            # create rectangle if not already existent
            if self.ship_shot_buffer[i] == None:
                self.ship_shot_buffer[i] = pygame.Rect(
                    SHOT_INIT_POS_X, SHOT_INIT_POS_Y, SHOT_WIDTH, SHOT_HEIGHT)
            # return index of free slot
            if self.ship_shot_buffer[i].y <= SHOT_INIT_POS_Y:
                return i

        return NUM_MAX_SHOTS_SHIP  # not found - return invalid index

    def find_free_shot_alien(self):
        """Find the 1st free buffer slot in the alien's shot buffer."""
        for i in range(NUM_MAX_SHOTS_ALIENS):
            # create rectangle if not already existent
            if self.alien_shot_buffer[i] == None:
                self.alien_shot_buffer[i] = pygame.Rect(
                    SHOT_INIT_POS_X, SHOT_INIT_POS_Y, SHOT_WIDTH, SHOT_HEIGHT)
            # return index of free slot
            if self.alien_shot_buffer[i].y <= SHOT_INIT_POS_Y:
                return i

        return NUM_MAX_SHOTS_ALIENS

    def find_free_shot_mystery(self):
        """Find the 1st free buffer slot in the mystery's shot buffer."""
        for i in range(NUM_MAX_SHOTS_MYSTERY):
            # create rectangle if not already existent
            if self.mystery_shot_buffer[i] == None:
                self.mystery_shot_buffer[i] = pygame.Rect(
                    SHOT_INIT_POS_X, SHOT_INIT_POS_Y, SHOT_WIDTH, SHOT_HEIGHT)
            # return index of free slot
            if self.mystery_shot_buffer[i].y <= SHOT_INIT_POS_Y:
                return i

        return NUM_MAX_SHOTS_MYSTERY

    def draw_shot(self, shot):
        """Draw a shot on the screen."""
        pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), shot)

    def shoot_from_ship(self, pos):
        """
        Fires a shot from the ship if there is an available slot in the shot buffer.
        Args:
            pos (tuple): A tuple containing the x and y coordinates where the shot should be fired from.
        """
        i = self.find_free_shot_ship()
        if i < NUM_MAX_SHOTS_SHIP:
            self.ship_shot_buffer[i].x = pos[0]
            self.ship_shot_buffer[i].y = pos[1]
            self.draw_shot(self.ship_shot_buffer[i])

    def shoot_from_alien(self, pos):
        """
        Fires a shot from an alien if there is an available slot in the shot buffer.
        Args:
            pos (tuple): A tuple containing the x and y coordinates where the shot should be fired from.
        """
        interval = time.time() - self.time
        if interval > ALIEN_SHOT_INTERVAL:
            self.time = time.time()
            i = self.find_free_shot_alien()
            if i < NUM_MAX_SHOTS_ALIENS:
                self.alien_shot_buffer[i].x = pos[0]
                self.alien_shot_buffer[i].y = pos[1]
                self.draw_shot(self.alien_shot_buffer[i])

    def shoot_from_mystery(self, pos):
        """
        Shoots a projectile from the mystery alien at the given position.
        This method checks if the time interval since the last shot is greater than 0.4 seconds.
        If so, it updates the time and finds a free slot in the alien shot buffer to teleport
        the shot to the given position and make it visible.
        Args:
            pos (tuple): A tuple containing the x and y coordinates where the shot should be teleported.
        """
        interval = time.time() - self.time_mystery_shots
        if interval > MYSTERY_SHOT_INTERVAL:
            self.time_mystery_shots = time.time()
            i = self.find_free_shot_mystery()
            if i < NUM_MAX_SHOTS_MYSTERY:
                self.mystery_shot_buffer[i].x = pos[0]
                self.mystery_shot_buffer[i].y = pos[1]
                self.draw_shot(self.mystery_shot_buffer[i])

    def move(self):
        """Move the shots on the screen."""
        for i in range(NUM_MAX_SHOTS_SHIP):
            if self.ship_shot_buffer[i] != None:
                if self.ship_shot_buffer[i].y > SHOT_INIT_POS_Y:
                    self.ship_shot_buffer[i].move_ip(0, -SHIP_SHOT_SPEED)
                    self.draw_shot(self.ship_shot_buffer[i])
                else:
                    self.ship_shot_buffer[i] = None

        for i in range(NUM_MAX_SHOTS_ALIENS):
            if self.alien_shot_buffer[i] != None:
                self.alien_shot_buffer[i].move_ip(0, ALIEN_SHOT_SPEED)
                self.draw_shot(self.alien_shot_buffer[i])

        for i in range(NUM_MAX_SHOTS_MYSTERY):
            if self.mystery_shot_buffer[i] != None:
                self.mystery_shot_buffer[i].move_ip(0, ALIEN_SHOT_SPEED)
                self.draw_shot(self.mystery_shot_buffer[i])

    def detect_collision_with_ship(self, pos):
        """Check if a shot has hit the ship."""
        for shot in self.alien_shot_buffer:
            if shot != None and get_distance(pos[0], pos[1], shot.x, shot.bottom) < DISTANCE_SHIP_COLLISION:
                return True
        for shot in self.mystery_shot_buffer:
            if shot != None and get_distance(pos[0], pos[1], shot.x, shot.bottom) < DISTANCE_SHIP_COLLISION:
                return True

        return False

    def housekeeping(self):
        """
        Shot buffer handling
        Creating an object for every shot is avoided.
        Shots are prepared for re-use when they run out of sight.
        """
        for i in range(NUM_MAX_SHOTS_SHIP):
            if self.ship_shot_buffer[i] != None and self.ship_shot_buffer[i].y < 0:
                self.ship_shot_buffer[i] = None
        for i in range(NUM_MAX_SHOTS_ALIENS):
            if self.alien_shot_buffer[i] != None and self.alien_shot_buffer[i].y > self.screen.get_height():
                self.alien_shot_buffer[i] = None
        for i in range(NUM_MAX_SHOTS_MYSTERY):
            if self.mystery_shot_buffer[i] != None and self.mystery_shot_buffer[i].y > self.screen.get_height():
                self.mystery_shot_buffer[i] = None
