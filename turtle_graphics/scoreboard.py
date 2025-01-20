from turtle import Turtle

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
        """Initialize the scoreboard with the given number of lives and the fonts used"""
        super().__init__(visible=False)
        self.hideturtle()
        self.color('white')
        self.penup()
        self.lives = lives
        self.score = 0
        self.highScore = score
        self.window_width = screen.window_width()
        self.window_height = screen.window_height()
        self.update_score()

    def update_score(self):
        """Update the score on the screen."""
        self.clear()
        self.color('white')
        self.goto(x=0, y=self.window_height / 2 - 40)
        self.write(f"Score: {self.score} High Score: {self.highScore}",
                   align=ALIGNMENT, font=FONT1)

    def increase_score(self, increment):
        """Increase the score by the given increment and update the score."""
        self.score += increment
        if self.score > self.highScore:
            self.highScore = self.score
        self.update_score()

    def game_over(self):
        """Display the game over text on the screen."""
        self.home()
        self.color('yellow')
        self.write("Game over!", align='center', font=FONT2)
        self.store_highscore()

    def decrease_lives_and_check_if_game_over(self, ship) -> bool:
        """Decrease the number of lives and check if the game is over."""
        game_over = False
        self.lives -= 1
        ship.decrease_lives()
        if self.lives <= 0:
            self.game_over()
            game_over = True

        return game_over

    def store_highscore(self):
        """Store the highscore in a file."""
        open('highestScore.txt', 'w').write(str(self.highScore))
