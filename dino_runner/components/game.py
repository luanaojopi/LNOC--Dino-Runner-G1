import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacleManager import ObstacleManager
from dino_runner.components.obstacles.score import Score
from dino_runner.components.obstacles.text import Text
from dino_runner.components.power_ups.cloud import Cloud
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.constants import BG, DINO_START, HAMMER_TYPE, ICON, RESET, SCREEN_HEIGHT, SCREEN_WIDTH, SHIELD_TYPE, TITLE, FPS


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.score = Score()
        self.death_count = 0
        self.power_up_manager = PowerUpManager()
        self.cloud = Cloud()

    def run(self):
        # Game loop: events - update - draw
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.quit()

    def play (self):
        # Game loop: events - update - draw
        self.reset_game()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def reset_game(self):
        self.playing = True
        self.game_speed = 20
        self.obstacle_manager.reset()
        self.score.reset()
        self.power_up_manager.reset()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self.game_speed, self.player, self.on_death)
        self.score.update(self)
        self.power_up_manager.update(self.game_speed, self.score.score, self.player)
        self.cloud.update(self.game_speed)
       
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.player.draw_power_up(self.screen)
        self.cloud.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()
        
    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def on_death(self):
        is_invincible = False
        if self.player.type == SHIELD_TYPE:
            is_invincible = True
        elif self.player.type == HAMMER_TYPE:
            for obstacle in self.obstacle_manager.obstacles:
                if obstacle.rect.colliderect(self.player.rect):
                    self.obstacle_manager.obstacles.remove(obstacle)
                return
        if not is_invincible:
            pygame.time.delay(500)
            self.playing = False
            self.death_count += 1

    def show_menu(self):
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        self.screen.fill((255, 255, 255))
        if self.death_count == 0:
            Text("Press any key to start.", (center_x, center_y)).draw(self.screen)
            self.screen.blit(DINO_START, (center_x - 49, center_y - 101))
            pygame.display.update()
            self.handle_menu_events()
        else:
            Text(f"Deaths {self.death_count}", (1000, 50)).draw(self.screen)
            Text("Press 'R' to restart.", (center_x, center_y + 50)).draw(self.screen)
            Text(f"Score {self.score.score}", (center_x, center_y + 100)).draw(self.screen)
            Text(f"High Score: {self.score.high_score}", (center_x, center_y + 150)).draw(self.screen)
            self.screen.blit(RESET, (center_x - 49, center_y - 70))
            pygame.display.update()
            self.handle_menu_events()
    
    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.play()
