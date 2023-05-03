import pygame


class Text:
    def __init__(self, text, position, size=22):
        self.font = pygame.font.Font('freesansbold.ttf', size)
        self.text = text
        self.color = (0, 0, 0)
        self.position = position

    def draw(self, screen):
        text = self.font.render(self.text, True, self.color)
        text_rect = text.get_rect()
        text_rect.center = self.position
        screen.blit(text, text_rect)
