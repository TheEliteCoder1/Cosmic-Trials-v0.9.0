'''
Cosmic Trials Game:
Author: Raphael Julian
Version: 0.9.0
'''

import pygame
from pygame.locals import *
import random
import sys
import pygame_gui


pygame.font.init()
pygame.mixer.init()

# Window Assets
ICON = pygame.image.load("Assets/my_icon.png")
pygame.display.set_icon(ICON)
WIDTH, HEIGHT = 800, 620
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Trials")

# Game Background
bg = pygame.image.load("Assets/bg.png")
BG = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Player images
img1 = pygame.image.load("Assets/ship.png")
img = pygame.transform.scale(img1, (80, 100))
SPACE_SHIP = pygame.transform.rotate(img, 270)

# Game objects
img2 = pygame.image.load("Assets/rock1.png")
ROCK = pygame.transform.scale(img2, (60, 80))
img3 = pygame.image.load("Assets/water.png")
WATER = pygame.transform.scale(img3, (60, 80))
MAX_BULLETS = 3
SONG = pygame.mixer.music.load('Assets/song.mp3')
LOST_SONG = pygame.mixer.Sound('Assets/lost.wav')
menu_sounds = pygame.mixer.Sound('Assets/menu.wav')
SPARK = pygame.mixer.Sound('Assets/spark.wav')
gem = pygame.image.load('Assets/gem.png')

# Score increasers
GEM = pygame.transform.scale(gem, (90, 90))
coin = pygame.image.load('Assets/coin.png')
COIN = pygame.transform.scale(coin, (90, 90))
OBSTACLE_HIT = pygame.mixer.Sound('Assets/obstacle_hit.mp3')


class player(object):
    def __init__(self, x, y, image=SPACE_SHIP):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel = 3



class rock(object):
    def __init__(self, x, y, image=ROCK):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel = 3.4

class scoring(object):
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()


def gradientRect( WINDOW, left_colour, right_colour, target_rect ):
    colour_rect = pygame.Surface( ( 2, 2 ) )                                   
    pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 0,1 ) )            
    pygame.draw.line( colour_rect, right_colour, ( 1,0 ), ( 1,1 ) )           
    colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )
    WINDOW.blit( colour_rect, target_rect ) 

def lost(surface, score):
    pygame.mixer.music.stop()
    LOST_SONG.play()
    my_font = pygame.font.SysFont("consolas", 60, bold=True)
    lost = my_font.render("YOU LOST!", 1, (0,0,0))
    gradientRect(WINDOW, (255, 66, 89), (255, 46, 0), pygame.Rect( 0,0, 800, 620 ) )
    
    gradientRect(WINDOW, (166, 255, 0), (255, 232, 0), pygame.Rect( 215, 100, 400, 300 ) )
    
    my_font2 = pygame.font.SysFont("consolas", 30, bold=True)
    
    score = my_font2.render(f"Score: {score}", 1, (0,0,0))
    
    surface.blit(lost, (270, 120))
    surface.blit(score, (335, 210))

particles = []

def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf


def menu_f():
    pygame.init()
    pygame.display.set_caption('Cosmic Trials')
    my_container = pygame.Rect((50, 520), (500, 200))
    root = pygame_gui.UIManager((WIDTH, HEIGHT))
    start_block = pygame.Rect((215, 125), (385, 80))
    start_title = pygame.font.SysFont("segoe ui", 60, bold=True)
    start_title_render = start_title.render("Cosmic Trials", 1, (34, 0, 69))
    start_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 295), (100, 50)),text='PLAY',manager=root)
    clock = pygame.time.Clock()
    while True:     
        time_delta = clock.tick(120)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_btn:
                        menu_sounds.play()
                        pygame.time.delay(500)
                        game()


        root.process_events(event)

        root.update(time_delta)

        gradientRect(WINDOW, (255, 0, 236), (128, 0, 255), pygame.Rect( 0,0, WIDTH, HEIGHT ) )
        pygame.draw.rect(WINDOW, (235, 224, 247), start_block)
        WINDOW.blit(start_title_render, (225, 125))
        root.draw_ui(WINDOW)
        pygame.display.flip()
        pygame.display.update()

def part():
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        particle[1][1] += 0.15
        pygame.draw.circle(WINDOW, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))


        radius = particle[2] * 2
        WINDOW.blit(circle_surf(radius, (20, 20, 60)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)

        if particle[2] <= 0:
            particles.remove(particle)


def game():
    pygame.init()
    pygame.mixer.music.play(-1)
    Player = player(0, HEIGHT/2)
    SCORE = 0
    objects = []
    nice = []
    BGX = 0
    BGX2 = BG.get_width()
    FPS = 120
    WAVE = 0
    PLAYER_BULLETS = []
    MAX_BULLETS = 5
    CLOCK = pygame.time.Clock()
    pygame.time.set_timer(USEREVENT+2, 3000)
    pygame.time.set_timer(USEREVENT+3, 6000)
    pygame.time.set_timer(USEREVENT+4, 20000)
    pygame.time.set_timer(USEREVENT+5, 1500)
    change = 1.4
    BULLET_VEL = 5
    while True:
        time_delta = CLOCK.tick(FPS)

        # checking for collision between objects and player
        for o in objects:
            if o.rect.colliderect(Player.rect.x, Player.rect.y, Player.width, Player.height):
                Player.rect.y = Player.rect.y - 17
                lost(WINDOW, SCORE)
                pygame.display.update()
                pygame.time.delay(6000)
                menu_f()
            if o.rect.x < -64:
                objects.pop(objects.index(o))
            else:
                o.rect.x -= change

        for o in nice:
            if o.rect.x < -64:
                nice.pop(nice.index(o))
            else:
                o.rect.x -= change
            

        BGX -= change
        BGX2 -= change

        if BGX < BG.get_width() * -1:
            BGX = BG.get_width()

        if BGX2 < BG.get_width() * -1:
            BGX2 = BG.get_width()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            # random game elements generation queues with classes
            if event.type == USEREVENT+2:
                rand_item = random.randrange(1, 12)
                rand_obj = random.randrange(1, 7)
                for x in range(6):
                    if rand_item == 1:
                        objects.append(rock(WIDTH, 50))
                    if rand_item == 2:
                        objects.append(rock(WIDTH, 200))
                    if rand_item == 3:
                        objects.append(rock(WIDTH, 300, WATER))
                    if rand_item == 4:
                        objects.append(rock(WIDTH, 50, WATER))
                    if rand_item == 5:
                        objects.append(rock(WIDTH, 200))
                    if rand_item == 6:
                        objects.append(rock(WIDTH, 300, WATER))
                    if rand_item == 7:
                        objects.append(rock(WIDTH, 50))
                    if rand_item == 8:
                        objects.append(rock(WIDTH, 200))
                    if rand_item == 9:
                        objects.append(rock(WIDTH, 300, WATER))
                    if rand_item == 10:
                        objects.append(rock(WIDTH, 50, WATER))
                    if rand_item == 11:
                        objects.append(rock(WIDTH, 200))
                    if rand_item == 12:
                        objects.append(rock(WIDTH, 300, WATER))

                if rand_obj == 1:
                    nice.append(scoring(WIDTH, 150, COIN))
                if rand_obj == 2:
                    nice.append(scoring(WIDTH, 250, COIN))
                if rand_obj == 5:
                    nice.append(scoring(WIDTH, 400, GEM))

            if event.type == USEREVENT+3 and change <= 14.8:
                change += 0.5
                objects.append(rock(WIDTH, 300, WATER))
                for BULLET in PLAYER_BULLETS:
                    PLAYER_BULLETS.remove(BULLET)

            if event.type == USEREVENT+4:
                WAVE += 1


            # automatic shooting algorithim that fires objects based on userevent queues
            if event.type == USEREVENT+5:
                for o in objects:
                    if o.rect.x <= 550:
                        BULLET = pygame.Rect((Player.rect.x, Player.rect.y + Player.height//2 - 2, 20, 10))
                        PLAYER_BULLETS.append(BULLET)
                    
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and Player.rect.y > Player.vel:
            Player.rect.y -= Player.vel
        if keys[pygame.K_s] and Player.rect.y < (HEIGHT - 100) - Player.height - Player.vel:
            Player.rect.y += Player.vel
        if keys[pygame.K_d] and Player.rect.x < (WIDTH - 20) - Player.width - Player.vel:
            Player.rect.x += Player.vel
        if keys[pygame.K_a] and Player.rect.x > Player.vel:
            Player.rect.x -= Player.vel

        for BULLET in PLAYER_BULLETS:
            if BULLET.x != WIDTH:
                BULLET.x += BULLET_VEL

        for BULLET in PLAYER_BULLETS:
            for o in objects:
                if o.rect.colliderect(BULLET):
                    objects.remove(o)
                    SCORE += 5
        

        CLOCK.tick(FPS)
        FONT = pygame.font.SysFont("consolas", 30)
        current_fps = str(int(CLOCK.get_fps()))
        render_fps = FONT.render(
            f'FPS:{current_fps}', 1, pygame.Color("White"))
        font = pygame.font.SysFont("consolas", 30)
        score = SCORE
        render_score = font.render(f'SCORE:{score}', 1, pygame.Color("White"))
        font1 = pygame.font.SysFont("consolas", 30)
        wave = WAVE
        render_wave = font1.render(f'WAVE:{WAVE}', 1, pygame.Color("White"))
        WINDOW.blit(BG, (BGX, 0))
        WINDOW.blit(BG, (BGX2, 0))
        for BULLET in PLAYER_BULLETS:
            pygame.draw.rect(WINDOW, (255,255,255), BULLET)
        mx, my = pygame.mouse.get_pos()
        particles.append([[mx, my], [random.randint(0, 20) / 10 - 1, -5], random.randint(6, 11)])
        for particle in particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            particle[1][1] += 0.15
            pygame.draw.circle(WINDOW, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))


            radius = particle[2] * 2
            WINDOW.blit(circle_surf(radius, (20, 20, 60)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)
            if particle[2] <= 0:
                particles.remove(particle)


        WINDOW.blit(Player.image, (Player.rect.x, Player.rect.y))
        WINDOW.blit(render_fps, (20, 20))
        WINDOW.blit(render_score, (WIDTH - 150, 20))
        WINDOW.blit(render_wave, (WIDTH/2 - 50, 20))
        for o in objects:
            part()
            WINDOW.blit(o.image, (o.rect.x, o.rect.y))
        for i in nice:
            if i.rect.collidepoint((mx, my)) and i.image == GEM:
                SPARK.play()
                nice.remove(i)
                SCORE += 20
            elif i.rect.collidepoint((mx, my)) and i.image == COIN:
                SPARK.play()
                nice.remove(i)
                SCORE += 10
            else:
                part()
                WINDOW.blit(i.image, (i.rect.x, i.rect.y))
        pygame.display.update()

if __name__ == "__main__":
    menu_f()
