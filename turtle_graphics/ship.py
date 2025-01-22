from turtle import Turtle, register_shape

Y_FLOOR = -350  # the y-position of the line under the ship
Y_MOVING_BASE = Y_FLOOR + 20  # The ship's bottom line
SHIP_GIF = 'resources/ship.gif'
register_shape(SHIP_GIF)
SHIP_WIDTH = 38  # width of the gif-file


class Ship(Turtle):
    def __init__(self, x, num_lives, screen):
        """Initialize the ship with the given number of lives."""
        super().__init__(visible=False)
        self.ship = Turtle(SHIP_GIF, visible=False)
        self.ship.penup()
        self.x_pos = x
        self.ship.teleport(x, Y_MOVING_BASE)
        self.ship.setheading(90)  # north
        self.ship.speed('fastest')
        self.ship.showturtle()
        self.window_width = screen.window_width()
        self.window_height = screen.window_height()
        self.num_ships_left = num_lives - 1
        self.draw_line('yellow')
        self.draw_replacement_ships()

    def draw_replacement_ships(self):
        """Draw the replacement ships at the bottom of the screen."""
        self.ships_left = []
        x = self.window_width / -2 + 22
        y = self.window_height / -2 + 30
        for ship in range(self.num_ships_left):
            self.ships_left.append(Turtle(SHIP_GIF, visible=False))
            self.ships_left[ship].teleport(x, y)
            self.ships_left[ship].showturtle()
            x += 45

    def decrease_lives(self):
        """Decrease the number of lives left by 1 and draw the replacement ships."""
        self.num_ships_left -= 1
        self.ships_left[self.num_ships_left].hideturtle()

    def draw_line(self, color):
        """Draw a line at the bottom of the screen (under the ship)."""
        line = Turtle(shape='classic', visible=False)
        line.penup()
        line.color(color)
        line.pensize(2)
        line.teleport(x=self.window_width / -2, y=Y_FLOOR)
        line.setheading(0)
        line.pendown()
        line.speed('fastest')
        line.showturtle()
        line.goto((self.window_width / 2 + 10, Y_FLOOR))

    def control(self, delta_x):
        """Control the ship's movement."""
        if delta_x != 0:
            self.x_pos += delta_x
            if self.x_pos < self.window_width / -2 + SHIP_WIDTH / 2 + 1:
                self.x_pos = self.window_width / -2 + SHIP_WIDTH / 2 + 1
            elif self.x_pos > self.window_width / 2 - SHIP_WIDTH / 2 - 8:
                self.x_pos = self.window_width / 2 - SHIP_WIDTH / 2 - 8

        self.ship.setx(self.x_pos)

    def get_position(self):
        """Return the ship's position."""
        return self.ship.position()
