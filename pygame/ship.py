import pygame


class Ship():
    def __init__(self, num_lives):
        """Initialize the ship with the given number of lives."""
        self.screen = pygame.display.get_surface()
        self.ship = pygame.image.load('resources/ship.gif').convert()
        self.x_pos = self.screen.get_width() / 2 - self.ship.get_width() / 2
        self.num_ships_left = num_lives - 1
        self.bottom_line = self.screen.get_height() - 35
        self.ship_bottom_line = self.bottom_line - 28  # The ship's bottom line

    def draw_replacement_ships(self):
        """Draw the replacement ships at the bottom of the screen."""
        x = 0
        y = self.screen.get_height() - self.ship.get_height() - 5
        for _ in range(self.num_ships_left):
            self.screen.blit(self.ship, (x, y))
            x += self.ship.get_width() + 5

    def draw_ship(self, x, y):
        """Draw the ship at the given x and y position as well as the line and the replacement ships."""
        self.screen.blit(self.ship, (x, y))
        self.draw_line('yellow')
        self.draw_replacement_ships()

    def decrease_lives(self):
        """Decrease the number of lives left by 1 and draw the replacement ships."""
        self.num_ships_left -= 1
        self.draw_replacement_ships()

    def draw_line(self, color):
        """Draw a line at the bottom of the screen (under the ship)."""
        pygame.draw.line(self.screen, color, (0, self.bottom_line),
                         (self.screen.get_width(), self.bottom_line), 2)

    def control(self, delta_x):
        """Control the ship's movement."""
        if delta_x != 0:
            self.x_pos += delta_x
            if self.x_pos < 0:
                self.x_pos = 0
            elif self.x_pos > self.screen.get_width() - self.ship.get_width():
                self.x_pos = self.screen.get_width() - self.ship.get_width()
        self.draw_ship(self.x_pos, self.ship_bottom_line)

    def get_shot_position(self):
        """Return the ship's shot position. (1 is half the width of the shot.)"""
        return self.x_pos + 1 + self.ship.get_width() / 2, self.ship_bottom_line

    def get_position(self):
        """Return the ship's position."""
        return self.x_pos + self.ship.get_width() / 2, self.bottom_line
