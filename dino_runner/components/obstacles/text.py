import pygame

class Text:
    def __init__(self):
        pass
    def draw(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 22)
        text = font.render(f"Score {self.score}", True, (0,0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        screen.blit(text, text_rect)
