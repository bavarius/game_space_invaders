from turtle import Turtle
from ship import Ship

ALIGNMENT = 'center'
FONT1 = ('Courier', 18, 'normal')
FONT2 = ('Courier', 48, 'normal')

try:
    score = int(open('highestScore.txt', 'r').read())
except FileNotFoundError:
    score = open('highestScore.txt', 'w').write(str(0))
except ValueError:
    score = 0


class Scoreboard(Turtle):
    def __init__(self, lives, screen):
        super().__init__(visible=False)
        self.hideturtle()
        self.color('white')
        self.penup()
        self.highScore = score
        self.lives = lives
        self.score = 0
        self.window_width = screen.window_width()
        self.window_height = screen.window_height()
        self.update_score()

    def update_score(self):
        self.clear()
        self.color('white')
        self.goto(x=0, y=self.window_height / 2 - 40)
        self.write(f"Score: {self.score} High Score: {self.highScore}",
                   align=ALIGNMENT, font=FONT1)

    def increase_score(self, increment):
        self.score += increment
        if self.score > self.highScore:
            self.highScore = self.score
        self.update_score()

    def game_over(self):
        self.home()
        self.write("Game over!", align='center', font=FONT2)

    def decrease_lives(self) -> bool:
        game_over = False
        self.lives -= 1
        if self.lives <= 0:
            self.game_over()
            game_over = True

        return game_over

    def get_current_num_lives(self):
        return self.lives

    def store_highscore(self):
        open('highestScore.txt', 'w').write(str(self.highScore))
