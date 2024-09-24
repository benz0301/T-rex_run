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

cloud = pygame.image.load("Assets\other\Cloud.png")

bg = pygame.image.load("Assets\other\Track.png")

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

class Cloud:
    def __init__(self):
        self.x = screen_width + random.randint(800, 1000)
        self.y  =random.randint(50, 100)
        self.image = cloud
        self.width = self.image.get_width()
        
    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = screen_width + random.randint(2500, 3000)
            self.y = random.randint(50, 100)
        
    def draw(self,screen):
        screen.blit(self.image, (self.x, self.y))
        
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width
        
    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
        
    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle) :
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0
        
    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index//5], self.rect)
        self.index += 1
        
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf' , 20)
    obstacles = []
    death_count = 0
    
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0 :
            game_speed += 1
            
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        screen.blit(text, textRect)
        
    def background():
        global x_pos_bg, y_pos_bg
        image_width = bg.get_width()
        screen.blit(bg, (x_pos_bg, y_pos_bg))
        screen.blit(bg, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            screen.blit(bg, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        screen.fill((255,255,255))
        userinput = pygame.key.get_pressed()
        
        player.draw(screen)
        player.update(userinput)
        
        if len(obstacles) == 0:    # hoe je een random obstakel inspawned
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(small_cactus))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(large_cactus))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(bird))
                
        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect): #collision detection 
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)
                
            
            
        background()
        
        cloud.draw(screen)
        cloud.update()
        
        score()
        
        
        clock.tick(30)
        pygame.display.update()




def menu(death_count):
    global points
    run = True
    while run:
        screen.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf' , 30)
        
        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (screen_width // 2, screen_height // 2 +50)
            screen.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (screen_width // 2, screen_height // 2)
        screen.blit(text, textRect)
        screen.blit(running[0], (screen_width // 2 - 20, screen_height // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

menu(death_count=0)