from turtle import Turtle, register_shape

STEP_WIDTH = 12
SHIP_GIF = 'resources/ship.gif'
register_shape(SHIP_GIF)


class Ship(Turtle):
    def __init__(self, x, y, num_lives, screen):
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
        self.create_replacement_ships()

    def create_replacement_ships(self):
        self.ships_left = []
        x = self.window_width / -2 + 22
        y = self.window_height / -2 + 30
        for ship in range(self.num_ships_left):
            self.ships_left.append(Turtle(SHIP_GIF, visible=False))
            self.ships_left[ship].teleport(x, y)
            self.ships_left[ship].showturtle()
            x += 45

    def redraw_ships_left(self, current_num_ships_left):
        for ship in range(self.num_ships_left):
            self.ships_left[ship].hideturtle()
        for ship in range(current_num_ships_left):
            self.ships_left[ship].showturtle()

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
        return self.ship.position()
