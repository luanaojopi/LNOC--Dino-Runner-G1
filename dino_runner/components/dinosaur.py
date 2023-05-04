import pygame
from pygame.sprite import Sprite
from dino_runner.components.obstacles.text import Text

from dino_runner.utils.constants import DEFAULT_TYPE, DUCKING, DUCKING_HAMMER, DUCKING_SHIELD, HAMMER_TYPE, JUMPING, JUMPING_HAMMER, JUMPING_SHIELD, RUNNING, RUNNING_HAMMER, RUNNING_SHIELD, SHIELD_TYPE

JUMP_VELOCITY = 8.5
DINO_RUNNING = "running"
DINO_JUMPING = "jumping"
DINO_DUCKING = "ducking"

DUCKING_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER}
JUMPING_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}
RUNNING_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}

class Dinosaur(Sprite):
    POS_X = 80
    POS_Y = 310
    POS_Y_DUCK = 340

    def __init__(self):
        self.type = DEFAULT_TYPE
        self.update_image (RUNNING_IMG[self.type][0])
        
        self.step = 0  
        self.action = DINO_RUNNING
        self.jump_velocity = JUMP_VELOCITY      

    def update(self,user_input):
        if self.action == DINO_RUNNING:
            self.run()
        elif self.action == DINO_JUMPING:
            self.jump()
        elif self.action == DINO_DUCKING:
            self.duck()

        if self.action != DINO_JUMPING:
            if user_input[pygame.K_UP]:
                self.action = DINO_JUMPING
            elif user_input[pygame.K_DOWN]:
                self.action = DINO_DUCKING
            else:
                self.action = DINO_RUNNING

        if self.step >= 10:
           self.step = 0                                              

    def draw (self, screen):
        screen.blit(self.image,(self.rect.x, self.rect.y))
         
    def jump(self):
         pos_y = self.rect.y - self.jump_velocity * 4
         self.update_image (JUMPING_IMG[self.type], pos_y = pos_y)
         self.jump_velocity -= 0.8
         if self.jump_velocity < -JUMP_VELOCITY:
            self.rect.y = self.POS_Y
            self.action = DINO_RUNNING
            self.jump_velocity = JUMP_VELOCITY

    def run(self):
        self.update_image(RUNNING_IMG[self.type][self.step // 5])
        self.step += 1
        self.rect.y = self.POS_Y
    
    def duck(self):
        self.update_image(DUCKING_IMG[self.type][self.step // 5])
        self.step += 1
        self.rect.y = self.POS_Y_DUCK
      
    def update_image(self, image: pygame.Surface, pos_x = None, pos_y = None):
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = pos_x or self.POS_X
        self.rect.y = pos_y or self.POS_Y

    def on_pick_power_up(self, power_up):
        print("PowerUp")
        print(power_up.type)
        self.type = power_up.type
        self.power_up_time_up = power_up.start_time + (power_up.duration * 1000) #conversion de segundos a ticks

    def draw_power_up(self, screen):
        if self.type != DEFAULT_TYPE:
            time_to_show = round(
                (self.power_up_time_up - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                Text(f"{self.type.capitalize()} enabled for {time_to_show} seconds. ", (600, 50)).draw(screen)
            else:
                self.type = DEFAULT_TYPE
                self.power_up_time_up = 0