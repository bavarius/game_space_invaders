from turtle import Turtle, register_shape
from random import randint
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
INITIAL_SPEED = 1
MAX_SPEED = 40
MYSTERY_SPEED = 15
MYSTERY_POINTS = 100
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
    alien_kinds = [
        # row0 (bottom row)
        dict(pic=ALIEN1_GIF, points=10, y_pos=VERTICAL_SPACE * 2),  # row0
        dict(pic=ALIEN1_GIF, points=10, y_pos=VERTICAL_SPACE * 3),  # row1
        dict(pic=ALIEN2_GIF, points=20, y_pos=VERTICAL_SPACE * 4),  # row2
        dict(pic=ALIEN2_GIF, points=20, y_pos=VERTICAL_SPACE * 5),  # row3
        dict(pic=ALIEN3_GIF, points=30, y_pos=VERTICAL_SPACE * 6),  # row4
    ]

    def __init__(self):
        self.stage_number = 0
        self.moving_direction = TO_LEFT
        self.num_aliens_on_screen = NUM_ROWS * ALIENS_PER_ROW
        self.speed = INITIAL_SPEED
        # Create array of aliens: Each alien is a turtle object.
        self.turtle = [[Turtle(self.alien_kinds[row]['pic'])
                        for _ in range(ALIENS_PER_ROW)] for row in range(NUM_ROWS)]
        # adjust turtle properties
        for row in range(NUM_ROWS):
            x_pos = X_POS_COL0
            for col in range(ALIENS_PER_ROW):
                self.turtle[row][col].penup()
                self.turtle[row][col].setheading(self.moving_direction)
                self.turtle[row][col].speed('slowest')
                self.turtle[row][col].teleport(
                    x_pos, self.alien_kinds[row]['y_pos'])
                x_pos += HORIZONTAL_SPACE
        # create mystery object
        self.mystery = Turtle(MYSTERY_GIF)
        self.mystery.hideturtle()
        self.mystery.penup()
        self.mystery.speed('fast')
        self.mystery_state = MysteryState.HIDDEN

    def reset(self):
        for row in range(NUM_ROWS):
            x_pos = X_POS_COL0
            for col in range(ALIENS_PER_ROW):
                self.turtle[row][col].setheading(self.moving_direction)
                self.turtle[row][col].teleport(
                    x_pos, self.alien_kinds[row]['y_pos'])
                self.turtle[row][col].showturtle()
                x_pos += HORIZONTAL_SPACE
        self.num_aliens_on_screen = NUM_ROWS * ALIENS_PER_ROW
        self.speed = INITIAL_SPEED  # reset speed

    def change_direction(self, direction):
        """Change moving direction of all aliens"""
        for col in range(ALIENS_PER_ROW):
            for row in range(NUM_ROWS):
                self.turtle[row][col].setheading(direction)

        self.moving_direction = direction

    def detect_collision_with_wall(self) -> bool:
        """Let the array of aliens change direction when hitting the wall."""
        if self.moving_direction == TO_LEFT:
            for col in range(ALIENS_PER_ROW):
                for row in range(NUM_ROWS):
                    if self.turtle[row][col].isvisible() == True:
                        if self.turtle[row][col].xcor() <= -378.0:
                            return True
                        else:
                            return False
        elif self.moving_direction == TO_RIGHT:
            for col in range(ALIENS_PER_ROW - 1, -1, -1):
                for row in range(NUM_ROWS):
                    if self.turtle[row][col].isvisible() == True:
                        if self.turtle[row][col].xcor() >= 371.0:
                            return True
                        else:
                            return False

        return False

    def detect_collision_with_ship(self, t):
        for row in range(NUM_ROWS):
            for col in range(ALIENS_PER_ROW):
                if self.turtle[row][col].isvisible() == True:
                    if self.turtle[row][col].distance(t) < DISTANCE_SHIP_COLLISION:
                        return True

        return False

    def detect_collision_with_shot(self, t) -> int:
        for row in range(NUM_ROWS):
            for col in range(ALIENS_PER_ROW):
                if self.turtle[row][col].isvisible() == True:
                    if self.turtle[row][col].distance(t) < DISTANCE_SHOT_COLLISION:
                        t.sety(410)  # move shot out of sight
                        t.hideturtle()  # hide shot
                        self.turtle[row][col].hideturtle()
                        self.num_aliens_on_screen -= 1
                        if self.num_aliens_on_screen <= 5 or self.num_aliens_on_screen % ALIENS_PER_ROW == 0:
                            self.speed = MAX_SPEED + self.stage_number - \
                                ((MAX_SPEED - 1) * self.num_aliens_on_screen /
                                 (NUM_ROWS * ALIENS_PER_ROW) - 1)
                        return self.alien_kinds[row]['points']
        if self.mystery_state != MysteryState.HIDDEN:
            if self.mystery.distance(t) < DISTANCE_SHOT_COLLISION:
                t.sety(410)  # move shot out of sight
                t.hideturtle()  # hide shot
                self.mystery.hideturtle()
                self.mystery_state = MysteryState.HIDDEN
                return MYSTERY_POINTS

        return 0

    def get_random_alien_position(self):
        while True:
            row = randint(0, NUM_ROWS - 1)
            col = randint(0, ALIENS_PER_ROW - 1)
            if self.turtle[row][col].isvisible() == True:
                return self.turtle[row][col].position()

    def get_mystery_position(self):
        return self.mystery.position()

    def control_mystery(self):
        if self.mystery_state == MysteryState.HIDDEN:
            if randint(0, 100) == 0:
                self.mystery.teleport(420, VERTICAL_SPACE * 7)
                self.mystery.setheading(TO_LEFT)
                self.mystery.showturtle()
                self.mystery_state = MysteryState.MOVING_LEFT
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
        for col in range(ALIENS_PER_ROW):
            for row in range(NUM_ROWS):
                self.turtle[row][col].sety(
                    self.turtle[row][col].ycor() - VERTICAL_SPACE)

    def move_all(self):
        for col in range(ALIENS_PER_ROW):
            for row in range(NUM_ROWS):
                self.turtle[row][col].forward(self.speed)

    def move(self):
        if self.detect_collision_with_wall():
            if self.moving_direction == TO_LEFT:
                self.change_direction(TO_RIGHT)
            else:
                self.change_direction(TO_LEFT)
                self.move_down_one_row()

        self.control_mystery()
        self.move_all()

    def get_num_on_screen(self):
        return self.num_aliens_on_screen
