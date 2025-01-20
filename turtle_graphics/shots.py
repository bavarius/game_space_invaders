from turtle import Turtle
import time

NUM_MAX_SHOTS_SHIP = 7  # shots on screen at a time
NUM_MAX_SHOTS_ALIENS = 10  # alien shots on screen at a time
NUM_MAX_SHOTS_MYSTERY = 18  # mystery shots on screen at a time
HEADING_NORTH = 90
HEADING_SOUTH = 270
SHIP_SHOT_SPEED = 5
ALIEN_SHOT_SPEED = 2.0
ALIEN_SHOT_INTERVAL = 0.5
MYSTERY_SHOT_INTERVAL = 0.6
DISTANCE_SHOT_SHIP_COLLISION = 20


class Shots(Turtle):
    def __init__(self):
        super().__init__(visible=False)
        self.ship_shot_buffer = []
        self.alien_shot_buffer = []
        self.mystery_shot_buffer = []
        self.create_shot_buffers()
        self.init_ship_shot_buffer()
        self.init_alien_shot_buffer()
        self.init_mystery_shot_buffer()
        self.time = time.time()
        self.time_mystery_shots = time.time()

    def create_shot_buffers(self):
        for _ in range(NUM_MAX_SHOTS_SHIP):
            self.ship_shot_buffer.append(Turtle(shape='square', visible=False))
        for _ in range(NUM_MAX_SHOTS_ALIENS):
            self.alien_shot_buffer.append(
                Turtle(shape='square', visible=False))
        for _ in range(NUM_MAX_SHOTS_MYSTERY):  # mystery shots
            self.mystery_shot_buffer.append(
                Turtle(shape='square', visible=False))

    def init_ship_shot_buffer(self):
        for i in range(len(self.ship_shot_buffer)):
            self.ship_shot_buffer[i].hideturtle()
            self.ship_shot_buffer[i].shapesize(
                stretch_wid=0.1, stretch_len=0.6)
            self.ship_shot_buffer[i].penup()
            self.ship_shot_buffer[i].color('white')
            self.ship_shot_buffer[i].setheading(HEADING_NORTH)
            self.ship_shot_buffer[i].speed('normal')
            self.ship_shot_buffer[i].goto(0, 410)

    def init_alien_shot_buffer(self):
        for i in range(len(self.alien_shot_buffer)):
            self.alien_shot_buffer[i].hideturtle()
            self.alien_shot_buffer[i].shapesize(
                stretch_wid=0.1, stretch_len=0.6)
            self.alien_shot_buffer[i].penup()
            self.alien_shot_buffer[i].color('white')
            self.alien_shot_buffer[i].setheading(HEADING_SOUTH)
            self.alien_shot_buffer[i].speed('slowest')

    def init_mystery_shot_buffer(self):
        for i in range(len(self.mystery_shot_buffer)):
            self.mystery_shot_buffer[i].hideturtle()
            self.mystery_shot_buffer[i].shapesize(
                stretch_wid=0.1, stretch_len=0.6)
            self.mystery_shot_buffer[i].penup()
            self.mystery_shot_buffer[i].color('white')
            self.mystery_shot_buffer[i].setheading(HEADING_SOUTH)
            self.mystery_shot_buffer[i].speed('slowest')

    def reset(self):
        """Reset the shot buffers."""
        for i in range(NUM_MAX_SHOTS_SHIP):
            self.ship_shot_buffer[i].hideturtle()
        for i in range(NUM_MAX_SHOTS_ALIENS):
            self.alien_shot_buffer[i].hideturtle()
        for i in range(NUM_MAX_SHOTS_MYSTERY):
            self.mystery_shot_buffer[i].hideturtle()

    def find_free_shot_ship(self):
        """Find the 1st free buffer slot in the ship's shot buffer."""
        for i in range(NUM_MAX_SHOTS_SHIP):
            if self.ship_shot_buffer[i].isvisible() == False:
                # return index of free slot
                return i

        return NUM_MAX_SHOTS_SHIP  # not found - return invalid index

    def find_free_shot_alien(self):
        """Find the 1st free buffer slot in the alien's shot buffer."""
        for i in range(NUM_MAX_SHOTS_ALIENS):
            if self.alien_shot_buffer[i].isvisible() == False:
                # return index of free slot
                return i

        return NUM_MAX_SHOTS_ALIENS

    def find_free_shot_mystery(self):
        """Find the 1st free buffer slot in the mystery's shot buffer."""
        for i in range(NUM_MAX_SHOTS_MYSTERY):
            if self.mystery_shot_buffer[i].isvisible() == False:
                # return index of free slot
                return i

        return NUM_MAX_SHOTS_MYSTERY

    def shoot_from_ship(self, pos):
        """
        Fires a shot from the ship if there is an available slot in the shot buffer.

        Args:
            pos (tuple): A tuple containing the x and y coordinates where the shot should be fired from.
        """
        i = self.find_free_shot_ship()
        if i < NUM_MAX_SHOTS_SHIP:
            self.ship_shot_buffer[i].teleport(pos[0], pos[1])
            self.ship_shot_buffer[i].showturtle()

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
                self.alien_shot_buffer[i].teleport(pos[0], pos[1])
                self.alien_shot_buffer[i].showturtle()

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
                self.mystery_shot_buffer[i].teleport(pos[0], pos[1])
                self.mystery_shot_buffer[i].showturtle()

    def move(self):
        """Move the shots on the screen."""
        for i in range(NUM_MAX_SHOTS_SHIP):
            if self.ship_shot_buffer[i].isvisible() == True:
                self.ship_shot_buffer[i].forward(SHIP_SHOT_SPEED)

        for i in range(NUM_MAX_SHOTS_ALIENS):
            if self.alien_shot_buffer[i].isvisible() == True:
                self.alien_shot_buffer[i].forward(ALIEN_SHOT_SPEED)

        for i in range(NUM_MAX_SHOTS_MYSTERY):
            if self.mystery_shot_buffer[i].isvisible() == True:
                self.mystery_shot_buffer[i].forward(ALIEN_SHOT_SPEED)

    def detect_collision_with_ship(self, pos):
        """Check if a shot has hit the ship."""
        for shot in self.alien_shot_buffer:
            if shot.isvisible() == True and shot.distance(pos) < DISTANCE_SHOT_SHIP_COLLISION:
                return True
        for shot in self.mystery_shot_buffer:
            if shot.isvisible() == True and shot.distance(pos) < DISTANCE_SHOT_SHIP_COLLISION:
                return True

        return False

    def housekeeping(self, screen_height):
        """Shot buffer handling
        Creating a turtle object for every shot is avoided.
        Shots are prepared for re-use when they run out of sight.
        """
        for shot_s in self.ship_shot_buffer:
            if shot_s.isvisible() == True and shot_s.ycor() > screen_height / 2:
                shot_s.hideturtle()
        for shot in self.alien_shot_buffer:
            if shot.isvisible() == True and shot.ycor() < screen_height / -2:
                shot.hideturtle()
        for shot in self.mystery_shot_buffer:
            if shot.isvisible() == True and shot.ycor() < screen_height / -2:
                shot.hideturtle()

    def get_ship_shot_buffer(self):
        return self.ship_shot_buffer
