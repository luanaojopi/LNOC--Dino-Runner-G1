import pygame
from dino_runner.components.obstacles.text import Text


class Score:
    def __init__(self):
        self.score = 0
        self.high_score = 0

    def update(self, game):
        self.score += 1
        if self.score % 100 == 0:
            game.game_speed += 2

        if self.score > self.high_score:
            self.high_score = self.score

    def draw(self, screen):
        score_text = Text(f"Score {self.score}", (1000, 50))
        score_text.draw(screen)

    def reset(self):
        self.score = 0

       