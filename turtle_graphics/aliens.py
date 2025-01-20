from turtle import Turtle, register_shape
from random import randint, choice
from enum import Enum

ALIENS_PER_ROW = 11
NUM_ROWS = 5
X_POS_COL0 = -78
ALIEN1_GIF = 'resources/alien1.gif'
ALIEN2_GIF = 'resources/alien2.gif'
ALIEN3_GIF = 'resources/alien3.gif'
MYSTERY_GIF = 'resources/mystery.gif'
TO_RIGHT = 0
TO_LEFT = 180
VERTICAL_SPACE = 45
HORIZONTAL_SPACE = 45
INITIAL_SPEED = 0.5
MAX_SPEED = 5
MYSTERY_SPEED = 3
MYSTERY_APPEARANCE_PROBABILITY = 1000
MYSTERY_POINTS = [100, 200, 500, 750, 1000]
DISTANCE_SHOT_COLLISION = 30.0
DISTANCE_SHIP_COLLISION = 25.0
register_shape(ALIEN1_GIF)
register_shape(ALIEN2_GIF)
register_shape(ALIEN3_GIF)
register_shape(MYSTERY_GIF)


class MysteryState(Enum):
    HIDDEN = 0
    MOVING_LEFT = 1
    MOVING_RIGHT = 2


class Aliens(Turtle):
    def __init__(self, width):
        """Initialize the aliens."""
        self.screen_width = width
        self.alien_kinds = [
            # row0 (bottom row)
            dict(pic=ALIEN1_GIF, points=10,
                 y_pos=VERTICAL_SPACE * 2),  # row0
            dict(pic=ALIEN1_GIF, points=10,
                 y_pos=VERTICAL_SPACE * 3),  # row1
            dict(pic=ALIEN2_GIF, points=20,
                 y_pos=VERTICAL_SPACE * 4),  # row2
            dict(pic=ALIEN2_GIF, points=20,
                 y_pos=VERTICAL_SPACE * 5),  # row3
            dict(pic=ALIEN3_GIF, points=30,
                 y_pos=VERTICAL_SPACE * 6),  # row4
        ]
        self.stage_number = 0
        self.speed = INITIAL_SPEED
        self.moving_direction = TO_LEFT
        self.num_aliens_on_screen = NUM_ROWS * ALIENS_PER_ROW
        # Create array of aliens: Each alien is a turtle object.
        self.aliens = [[Turtle(self.alien_kinds[row]['pic'])
                        for _ in range(ALIENS_PER_ROW)] for row in range(NUM_ROWS)]
        # adjust turtle properties
        for row in range(NUM_ROWS):
            x_pos = X_POS_COL0
            for col in range(ALIENS_PER_ROW):
                self.aliens[row][col].penup()
                self.aliens[row][col].setheading(self.moving_direction)
                self.aliens[row][col].speed('slowest')
                self.aliens[row][col].teleport(
                    x_pos, self.alien_kinds[row]['y_pos'])
                x_pos += HORIZONTAL_SPACE
        # create mystery object
        self.mystery = Turtle(MYSTERY_GIF)
        self.mystery.hideturtle()
        self.mystery.penup()
        self.mystery.speed('fast')
        self.mystery_state = MysteryState.HIDDEN

    def reset(self):
        """Reset object positions, states and speed."""
        for row in range(NUM_ROWS):
            x_pos = X_POS_COL0
            for col in range(ALIENS_PER_ROW):
                self.aliens[row][col].setheading(self.moving_direction)
                self.aliens[row][col].teleport(
                    x_pos, self.alien_kinds[row]['y_pos'])
                self.aliens[row][col].showturtle()
                x_pos += HORIZONTAL_SPACE
        self.mystery.setx(self.screen_width / 2 + 30)
        self.mystery_state = MysteryState.HIDDEN
        self.num_aliens_on_screen = NUM_ROWS * ALIENS_PER_ROW
        self.speed = INITIAL_SPEED  # reset speed

    def change_direction(self, direction):
        """Change moving direction of all aliens"""
        for col in range(ALIENS_PER_ROW):
            for row in range(NUM_ROWS):
                self.aliens[row][col].setheading(direction)

        self.moving_direction = direction

    def detect_collision_with_wall(self) -> bool:
        """Let the array of aliens change direction when hitting the wall."""
        if self.moving_direction == TO_LEFT:
            for col in range(ALIENS_PER_ROW):
                for row in range(NUM_ROWS):
                    if self.aliens[row][col].isvisible() == True:
                        if self.aliens[row][col].xcor() <= -378.0:
                            return True
                        else:
                            return False
        elif self.moving_direction == TO_RIGHT:
            for col in range(ALIENS_PER_ROW - 1, -1, -1):
                for row in range(NUM_ROWS):
                    if self.aliens[row][col].isvisible() == True:
                        if self.aliens[row][col].xcor() >= 371.0:
                            return True
                        else:
                            return False

        return False

    def detect_collision_with_ship_or_bottomline(self, pos) -> bool:
        """Detect if an alien hits the ship or the bottom line."""
        for row in range(NUM_ROWS):
            for col in range(ALIENS_PER_ROW):
                if self.aliens[row][col].isvisible() == True:
                    if self.aliens[row][col].distance(pos) < DISTANCE_SHIP_COLLISION:
                        return True

        return False

    def detect_hit_by_shot_and_get_points(self, shots) -> int:
        """Detect if an alien is hit by a shot and return the points."""
        shots_from_ship = shots.get_ship_shot_buffer()
        for row in range(NUM_ROWS):
            for col in range(ALIENS_PER_ROW):
                for shot in shots_from_ship:
                    if shot.isvisible() == True:
                        if self.aliens[row][col].isvisible() == True:
                            if self.aliens[row][col].distance(shot) < DISTANCE_SHOT_COLLISION:
                                shot.sety(410)  # move shot out of sight
                                shot.hideturtle()  # hide shot
                                self.aliens[row][col].hideturtle()
                                self.num_aliens_on_screen -= 1
                                return self.alien_kinds[row]['points']

                        if self.mystery_state != MysteryState.HIDDEN:
                            if self.mystery.distance(shot) < DISTANCE_SHOT_COLLISION:
                                shot.sety(410)  # move shot out of sight
                                shot.hideturtle()  # hide shot
                                self.mystery.hideturtle()
                                self.mystery_state = MysteryState.HIDDEN
                                return choice(MYSTERY_POINTS)

        self.control_speed()

        return 0

    def get_random_alien_position(self):
        """Return the position of a random alien that is visible."""
        while True:
            row = randint(0, NUM_ROWS - 1)
            col = randint(0, ALIENS_PER_ROW - 1)
            if self.aliens[row][col].isvisible() == True:
                return self.aliens[row][col].position()

    def get_mystery_position(self):
        """Return the mystery's position."""
        return self.mystery.position()

    def control_mystery(self):
        """Control the mystery's appearance and movement."""
        if self.mystery_state == MysteryState.HIDDEN:
            if self.num_aliens_on_screen < NUM_ROWS * ALIENS_PER_ROW - 10 and randint(0, MYSTERY_APPEARANCE_PROBABILITY) == 0:
                self.mystery.teleport(420, VERTICAL_SPACE * 7)
                self.mystery.setheading(TO_LEFT)
                self.mystery_state = MysteryState.MOVING_LEFT
                self.mystery.showturtle()
        elif self.mystery_state == MysteryState.MOVING_LEFT:
            self.mystery.forward(MYSTERY_SPEED)
            if self.mystery.xcor() <= -385:
                self.mystery.setheading(TO_RIGHT)
                self.mystery_state = MysteryState.MOVING_RIGHT
        else:
            self.mystery.forward(MYSTERY_SPEED)
            if self.mystery.xcor() >= 400:
                self.mystery.hideturtle()
                self.mystery_state = MysteryState.HIDDEN

    def move_down_one_row(self):
        """Move all aliens down one row."""
        for col in range(ALIENS_PER_ROW):
            for row in range(NUM_ROWS):
                self.aliens[row][col].sety(
                    self.aliens[row][col].ycor() - VERTICAL_SPACE)

    def move_all(self):
        """Move all aliens and the mystery."""
        for col in range(ALIENS_PER_ROW):
            for row in range(NUM_ROWS):
                self.aliens[row][col].forward(self.speed)

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

    def control_speed(self):
        """Control the speed of the aliens."""
        if self.num_aliens_on_screen == 1:
            self.speed = MAX_SPEED + self.stage_number
        elif self.num_aliens_on_screen == 3:
            self.speed = MAX_SPEED + self.stage_number - 0.625
        elif self.num_aliens_on_screen == 5:
            self.speed = MAX_SPEED + self.stage_number - 1.25
        elif self.num_aliens_on_screen == 12:
            self.speed = MAX_SPEED + self.stage_number - 2.5
        elif self.num_aliens_on_screen >= 25:
            self.speed = MAX_SPEED + self.stage_number - 4

    def get_num_on_screen(self):
        """Return the number of aliens on the screen."""
        return self.num_aliens_on_screen

    def get_mystery_state(self):
        """Return the mystery state (visibility and moving direction)."""
        return self.mystery_state
