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
        Text(f"Score {self.score}", (1000, 50)).draw(screen)
        Text(f"High Score {self.high_score}", (1000, 75)).draw(screen)

    def reset(self):
        self.score = 0

       