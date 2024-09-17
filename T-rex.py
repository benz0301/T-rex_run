import pygame
import os
import random

pygame.init()

# Global Constants
screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode ((screen_width,screen_height))

running = [pygame.image.load("Assets\Dino\DinoRun1.png"), pygame.image.load("Assets\Dino\DinoRun2.png")]
jumping = [pygame.image.load("Assets\Dino\DinoJump.png")]
ducking = [pygame.image.load("Assets\Dino\DinoDuck1.png"),pygame.image.load("Assets\Dino\DinoDuck2.png")]

small_cactus = [pygame.image.load("Assets\Cactus\SmallCactus1.png"),pygame.image.load("Assets\Cactus\SmallCactus2.png"),pygame.image.load("Assets\Cactus\SmallCactus3.png")]
large_cactus = [pygame.image.load("Assets\Cactus\LargeCactus1.png"),pygame.image.load("Assets\Cactus\LargeCactus2.png"),pygame.image.load("Assets\Cactus\LargeCactus3.png")]

bird = [pygame.image.load("Assets\Bird\Bird1.png"),pygame.image.load("Assets\Bird\Bird2.png")]

cloud = [pygame.image.load("Assets\other\Cloud.png")]

bg = [pygame.image.load("Assets\other\Track.png")]

class Dinosaur:
    x_pos = 80
    y_pos = 310
    y_pos_duck = 340
    JUMP_vel = 8.5
    
    def __init__(self):
        self.duck_img = ducking
        self.run_img = running
        self.jump_img = jumping
        
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        
        self.step_index  = 0
        self.jump_vel = self.JUMP_vel
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
        
    def update(self, userinput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
            
        if self.step_index >= 10:
            self.step_index = 0
            
        if userinput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userinput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userinput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
    
    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos_duck
        self.step_index += 1
    
    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
        self.step_index += 1
        
        
    def jump(self):
        self.image = self.jump_img[0]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_vel:
            self.dino_jump = False
            self.jump_vel = self.JUMP_vel

    def draw(self,screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


        


def main():
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()

    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        screen.fill((255,255,255))
        userinput = pygame.key.get_pressed()
        
        player.draw(screen)
        player.update(userinput)
        
        
        clock.tick(30)
        pygame.display.update()





main()