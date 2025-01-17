import pygame

SCORE_POS_Y = 15

try:
    score = int(open('highestScore.txt', 'r').read())
except FileNotFoundError:
    score = open('highestScore.txt', 'w').write(str(0))
except ValueError:
    score = 0


class Scoreboard():
    def __init__(self, lives, font, font_game_over):
        """Initialize the scoreboard with the given number of lives and the fonts used"""
        self.screen = pygame.display.get_surface()
        self.lives = lives
        self.score = 0
        self.highScore = score
        self.font = font
        self.font_game_over = font_game_over
        self.update_score()

    def update_score(self):
        """Update the score on the screen."""
        screen = pygame.display.get_surface()
        score = self.font.render(f"Score: {self.score} High Score: {self.highScore}",
                                 True, (255, 255, 255))
        screen.blit(score, score.get_rect(
            center=(self.screen.get_width() / 2, SCORE_POS_Y)))

    def increase_score(self, increment):
        """Increase the score by the given increment and update the score."""
        self.score += increment
        if self.score > self.highScore:
            self.highScore = self.score
        self.update_score()

    def game_over(self):
        """Display the game over text on the screen."""
        screen = pygame.display.get_surface()
        game_over_text = self.font_game_over.render("GAME OVER!",
                                                    True, (255, 255, 255))
        screen.blit(game_over_text, game_over_text.get_rect(
            center=screen.get_rect().center))
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
