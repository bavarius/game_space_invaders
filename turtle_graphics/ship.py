from turtle import Turtle, register_shape

STEP_WIDTH = 12
SHIP_GIF = 'resources/ship.gif'
register_shape(SHIP_GIF)


class Ship(Turtle):
    def __init__(self, x, y, num_lives, screen):
        """Initialize the ship with the given number of lives."""
        super().__init__(visible=False)
        self.ship = Turtle(SHIP_GIF, visible=False)
        self.ship.penup()
        self.ship.teleport(x, y)
        self.ship.setheading(90)  # north
        self.ship.speed('fastest')
        self.ship.showturtle()
        self.window_width = screen.window_width()
        self.window_height = screen.window_height()
        self.num_ships_left = num_lives - 1
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

    def move_left(self):
        """move ship left"""
        self.ship.setheading(180)  # west
        if self.ship.xcor() > self.window_width / -2:
            self.ship.forward(STEP_WIDTH)

    def move_right(self):
        """move ship right"""
        self.ship.setheading(0)  # east
        if self.ship.xcor() < self.window_width / 2:
            self.ship.forward(STEP_WIDTH)

    def get_position(self):
        """Return the ship's position."""
        return self.ship.position()
