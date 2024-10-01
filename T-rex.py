import pygame
import os
import random

pygame.init()
pygame.mixer.init()

# Globale constanten
screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))
player_name = "Player"  # standaart naam
game_muted = False  # geluid is niet muted bij start

# geluiden
jump_sound = pygame.mixer.Sound("Assets\Audio\jump.mp3")
collision_sound = pygame.mixer.Sound("Assets\Audio\death.mp3")

# Afbeeldingen van de dino in verschillende posities
running = [pygame.image.load("Assets/Dino/DinoRun1.png"), pygame.image.load("Assets/Dino/DinoRun2.png")]
jumping = [pygame.image.load("Assets/Dino/DinoJump.png")]
ducking = [pygame.image.load("Assets/Dino/DinoDuck1.png"), pygame.image.load("Assets/Dino/DinoDuck2.png")]

# Afbeeldingen van obstakels
small_cactus = [pygame.image.load("Assets/Cactus/SmallCactus1.png"), pygame.image.load("Assets/Cactus/SmallCactus2.png"), pygame.image.load("Assets/Cactus/SmallCactus3.png")]
large_cactus = [pygame.image.load("Assets/Cactus/LargeCactus1.png"), pygame.image.load("Assets/Cactus/LargeCactus2.png"), pygame.image.load("Assets/Cactus/LargeCactus3.png")]

bird = [pygame.image.load("Assets/Bird/Bird1.png"), pygame.image.load("Assets/Bird/Bird2.png")]

cloud = pygame.image.load("Assets/other/Cloud.png")  # Afbeelding van wolken
bg = pygame.image.load("Assets/other/Track.png")  # Achtergrondafbeelding (de grond)

# geluid waneer je iets aanraakt
def play_jump_sound():
    jump_sound_effect = jump_sound
    jump_sound_effect.play()

# om collision sound te spelen
def play_collision_sound():
    collision_sound_effect = collision_sound
    collision_sound_effect.play()
    
# Dinosaur klasse die de speler bestuurt
class Dinosaur:
    x_pos = 80  # De x-positie van de dino
    y_pos = 310  # De normale y-positie van de dino als hij rent
    y_pos_duck = 340  # De y-positie als de dino bukt
    JUMP_vel = 8.5  # De snelheid waarmee de dino springt

    def __init__(self):
        # Afbeeldingen voor rennen, bukken en springen
        self.duck_img = ducking
        self.run_img = running
        self.jump_img = jumping

        # Statussen van de dino (rennen, bukken, springen)
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0  # Telt de stappen van de dino voor de animatie
        self.jump_vel = self.JUMP_vel  # Stelt de sprongsnelheid in
        self.image = self.run_img[0]  # Begint met de eerste afbeelding voor het rennen
        self.dino_rect = self.image.get_rect()  # Creëer de rechthoek om de dino voor botsingsdetectie
        self.dino_rect.x = self.x_pos  # Zet de x-positie
        self.dino_rect.y = self.y_pos  # Zet de y-positie

    # Functie om de dino te updaten (rennen, bukken of springen afhankelijk van de invoer)
    def update(self, userinput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0  # Reset de stapindex voor animatie

        # Controleer of de speler de juiste toetsen indrukt (omhoog voor springen, omlaag voor bukken)
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

    # Functie voor bukken
    def duck(self):
        self.image = self.duck_img[self.step_index // 5]  # Verander afbeelding voor bukken
        self.dino_rect = self.image.get_rect()  # Update de dino-rechthoek
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos_duck  # Pas de y-positie aan voor bukken
        self.step_index += 1

    # Functie voor rennen
    def run(self):
        self.image = self.run_img[self.step_index // 5]  # Verander afbeelding voor rennen
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos  # Normale y-positie voor rennen
        self.step_index += 1

    # Functie voor springen
    def jump(self):
        self.image = self.jump_img[0]  # Verander afbeelding voor springen
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4  # Verplaats de dino omhoog
            play_jump_sound()  # Play jump sound
            self.jump_vel -= 0.8  # Verlaag de snelheid bij elke sprong
        if self.jump_vel < -self.JUMP_vel:  # Als de dino zijn hoogste punt bereikt
            self.dino_jump = False  # Stop met springen
            self.jump_vel = self.JUMP_vel  # Reset de sprongsnelheid

    # Functie om de dino op het scherm te tekenen
    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


# Klasse voor wolken
class Cloud:
    def __init__(self):
        self.x = screen_width + random.randint(800, 1000)  # Startpositie van de wolk buiten het scherm
        self.y = random.randint(50, 100)  # Willekeurige y-positie voor variatie
        self.image = cloud
        self.width = self.image.get_width()  # Breedte van de wolk

    # Functie om de wolk te updaten (bewegen)
    def update(self):
        self.x -= game_speed  # Verplaats de wolk naar links
        if self.x < -self.width:  # Als de wolk buiten het scherm is
            self.x = screen_width + random.randint(2500, 3000)  # Reset positie buiten het scherm
            self.y = random.randint(50, 100)  # Nieuwe willekeurige y-positie

    # Functie om de wolk op het scherm te tekenen
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


# Klasse voor obstakels
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()  # Creëer de rechthoek om het obstakel
        self.rect.x = screen_width  # Zet het obstakel buiten het scherm

    # Functie om het obstakel te updaten (bewegen)
    def update(self):
        self.rect.x -= game_speed  # Verplaats het obstakel naar links
        if self.rect.x < -self.rect.width:  # Als het obstakel buiten het scherm is
            obstacles.pop()  # Verwijder het obstakel uit de lijst

    # Functie om het obstakel op het scherm te tekenen
    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)


# Kleine cactus klasse (subklasse van Obstacle)
class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)  # Kies willekeurig een type cactus
        super().__init__(image, self.type)
        self.rect.y = 325  # Zet de y-positie van de kleine cactus


# Grote cactus klasse (subklasse van Obstacle)
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)  # Kies willekeurig een type cactus
        super().__init__(image, self.type)
        self.rect.y = 300  # Zet de y-positie van de grote cactus


# Vogel klasse (subklasse van Obstacle)
class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250  # Zet de y-positie van de vogel
        self.index = 0  # Animatie-index voor de vleugelbeweging

    # Functie om de vogel op het scherm te tekenen met animatie
    def draw(self, screen):
        if self.index >= 9:
            self.index = 0  # Reset de index als de animatiecyclus compleet is
        screen.blit(self.image[self.index // 5], self.rect)  # Wissel tussen vleugelposities
        self.index += 1

# functie voor geluid
def toggle_mute():
    global game_muted
    game_muted = not game_muted
    if game_muted:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
# Klasse voor een knop die gebruikt kan worden in het menu
class Button:
    def __init__(self, text, width, height, pos, font_size, bg_color, text_color):
        self.text = text  # Tekst op de knop
        self.width = width  # Breedte van de knop
        self.height = height  # Hoogte van de knop
        self.pos = pos  # Positie op het scherm
        self.font = pygame.font.Font('freesansbold.ttf', font_size)  # Lettertype en grootte van de tekst
        self.bg_color = bg_color  # Achtergrondkleur van de knop
        self.text_color = text_color  # Tekstkleur
        self.rect = pygame.Rect(pos[0], pos[1], width, height)  # De rechthoek van de knop
        self.text_surf = self.font.render(self.text, True, text_color)  # Render de tekst
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)  # Positioneer de tekst binnen de knop

    # Functie om de knop te tekenen
    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)  # Teken de knop
        screen.blit(self.text_surf, self.text_rect)  # Plaats de tekst bovenop de knop

    # Controleer of de knop is aangeklikt
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)  # Retourneer True als de muisklik binnen de rechthoek valt


# Hoofdfunctie die het spel start
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()  # Regelt de framesnelheid
    player = Dinosaur()  # Maak een spelerobject (dino)
    cloud = Cloud()  # Maak een wolkenobject
    game_speed = 14  # Start snelheid van het spel
    x_pos_bg = 0  # De x-positie van de achtergrond
    y_pos_bg = 380  # De y-positie van de achtergrond
    points = 0  # Score van de speler
    font = pygame.font.Font('freesansbold.ttf', 20)  # Lettertype voor de score
    obstacles = []  # Lijst van obstakels in het spel
    death_count = 0  # Aantal keren dat de speler doodgaat

    # Functie om de score te berekenen en weer te geven
    def score():
        global points, game_speed
        points += 1  # Verhoog de score
        if points % 100 == 0:
            game_speed += 1  # Verhoog de snelheid na elke 100 punten

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render("Points: " + str(points), True, (0, 0, 0))  # Render de scoretekst
        name_text = font.render(f"player: {player_name}",True, (0,0,0))
        textRect = text.get_rect()
        nameRect = name_text.get_rect()
        nameRect.center = (100, 40)
        textRect.center = (1000, 40)  # Plaats de score rechtsboven in het scherm
        screen.blit(text, textRect)
        screen.blit(name_text, nameRect)

    # Functie om de achtergrond te bewegen
    def background():
        global x_pos_bg, y_pos_bg
        image_width = bg.get_width()  # Breedte van de achtergrondafbeelding
        screen.blit(bg, (x_pos_bg, y_pos_bg))  # Teken de achtergrond
        screen.blit(bg, (image_width + x_pos_bg, y_pos_bg))  # Teken de tweede helft van de achtergrond
        if x_pos_bg <= -image_width:
            screen.blit(bg, (image_width + x_pos_bg, y_pos_bg))  # Reset de achtergrondpositie
            x_pos_bg = 0
        x_pos_bg -= game_speed  # Verplaats de achtergrond naar links

    # De hoofdgame-lus
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Als de speler het venster sluit
                run = False

        screen.fill((255, 255, 255))  # Vul het scherm met witte kleur
        userinput = pygame.key.get_pressed()  # Haal de toetsenbordinvoer op

        player.draw(screen)  # Teken de speler (dino) op het scherm
        player.update(userinput)  # Update de positie en actie van de speler

        # Maak nieuwe obstakels als er geen zijn
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(small_cactus))  # Voeg een kleine cactus toe
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(large_cactus))  # Voeg een grote cactus toe
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(bird))  # Voeg een vogel toe

        # Update en teken elk obstakel
        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):  # Controleer op botsing
                play_collision_sound() 
                pygame.time.delay(2000)  # Pauzeer het spel
                death_count += 1  # Verhoog het aantal keer dat de speler doodgaat
                menu(death_count)  # Ga terug naar het menu

        background()  # Beweeg de achtergrond

        cloud.draw(screen)  # Teken en update de wolken
        cloud.update()

        score()  # Toon de score

        clock.tick(30)  # Beperk de framesnelheid tot 30 FPS
        pygame.display.update()  # Update het scherm

#Options menu 
def options_menu():
    global player_name, game_muted
    death_count = 0
    run = True
    input_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)

    mute_button_text = "Unmute" if game_muted else "Mute"
    mute_button = Button(mute_button_text, 150, 50, (screen_width // 2 - 75, screen_height // 2 + 50), 30, (0, 0, 200), (255, 255, 255))
    menu_button = Button("Return ",150,50,(screen_width // 2 - 75, screen_height // 2 + 100), 30, (0, 0, 200), (255, 255, 255))
    while run:
        screen.fill((255, 255, 255))

        # Display instructions
        font = pygame.font.Font('freesansbold.ttf', 30)
        name_label = font.render("Enter Player Name:", True, (0, 0, 0))
        name_label_rect = name_label.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        screen.blit(name_label, name_label_rect)

        # Handle name input
        txt_surface = font.render(text, True, (0, 0, 0))
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        mute_button.draw(screen)
        menu_button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False

                if mute_button.is_clicked(event.pos):
                    toggle_mute()
                    mute_button_text = "Unmute" if game_muted else "Mute"
                    mute_button = Button(mute_button_text, 150, 50, (screen_width // 2 - 75, screen_height // 2 + 50), 30, (0, 0, 200), (255, 255, 255))

                if menu_button.is_clicked(event.pos):
                    player_name = text
                    text = ''
                    menu(death_count)
                    
                    
                    
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        player_name = text
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode


# Menu-functie die verschijnt aan het begin of na het verliezen
def menu(death_count):
    global points
    run = True
    quit_button = Button("Quit", 150, 50, (screen_width // 2 - 75, screen_height // 2 + 200), 30, (200, 0, 0), (255, 255, 255))
    option_button = Button("Options", 150, 50, (screen_width // 2 - 75, screen_height // 2 + 150), 30, (0, 0, 200), (255, 255, 255))

    while run:
        screen.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)
        title_font = pygame.font.Font('freesansbold.ttf', 50)
        title_text = title_font.render("T-Rex Runner Game", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 200))

        if death_count == 0:
            screen.blit(title_text, title_rect)
            text = font.render("Press Space-Bar to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press Space-Bar to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            score_rect = score.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
            screen.blit(score, score_rect)

        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)
        screen.blit(running[0], (screen_width // 2 - 20, screen_height // 2 - 140))

        quit_button.draw(screen)
        option_button.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.is_clicked(event.pos):
                    pygame.quit()
                    exit()
                if option_button.is_clicked(event.pos):
                    options_menu()

menu(death_count=0)  # Start het menu bij het begin van het spel
