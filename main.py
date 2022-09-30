import pygame
import random
import os
from pygame import mixer

# Initialise pygame
mixer.init()
pygame.init()

"""
    CONSTANTS
"""
#sounds
jump_fx = pygame.mixer.Sound('assets/sfx/jump.mp3')
jump_fx.set_volume(0.5)

# game window dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# frame rate
FPS = 60

# Colours 
WHITE = (255,255, 255)
BLACK = (0, 0, 0)
PANEL = (153, 217, 234)

# Platform constant
MAX_PLATFORMS = 10
PLATFORM_HEIGHT = 10
PLATFORM_MIN_WIDTH = 40
PLATFORM_MAX_WIDTH = 70
PLATFORM_MIN_HEIGHT_DIFF = 80
PLATFORM_MAX_HEIGHT_DIFF = 120

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('HHH')

# Speed
HORIZONTAL_SPEED = 5
VERTICAL_SPEED = 5
GRAVITY = 1

#game variables
SCROLL_THRESH = 200
MAX_PLATFORMS = 10
scroll = 0
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0

"""
    VARIABLES
"""
# set frame rate 
clock = pygame.time.Clock()


# load music and sounds

# load images
bg_image = pygame.image.load('assets/gfx/bg.png').convert_alpha()
platform_image = pygame.image.load('assets/gfx/wood.png').convert_alpha()
player_image = pygame.image.load('assets/gfx/player.png').convert_alpha()

"""
    PLATFORM
"""
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, PLATFORM_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# game variables

# Create platform group
platform_group = pygame.sprite.Group()

# Create temporary platforms
for p in range(MAX_PLATFORMS):
    p_w = random.randint(PLATFORM_MIN_WIDTH, PLATFORM_MAX_WIDTH)
    p_x = random.randint(0, SCREEN_WIDTH - p_w)
    p_y = p * random.randint(PLATFORM_MIN_HEIGHT_DIFF, PLATFORM_MAX_HEIGHT_DIFF)
    new_platform = Platform(p_x, p_y, p_w)
    platform_group.add(new_platform)
    
"""
    PLAYER
"""
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pygame.transform.scale(player_image, (45, 45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):
        #reset movement variables
        dx = 0
        dy = 0
        scroll = 0

        #process input
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx -= HORIZONTAL_SPEED
            self.flip = True
        if key[pygame.K_RIGHT]:
            dx += HORIZONTAL_SPEED
            self.flip = False

        #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #check for collision with platforms
        for platform in platform_group:
            #collision in the y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if above platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20
                        jump_fx.play()

        #check if player hit top of screen
        if self.rect.top + dy <= SCROLL_THRESH:
            dy = -self.rect.top
            #if player is jumping
            if self.vel_y < 0:
                scroll = -dy

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy + scroll

		#update mask
        self.mask = pygame.mask.from_surface(self.image)

        return scroll

        def draw(self):
            screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))

"""
    GAME
"""
run = True
while run:

    clock.tick(FPS)

    # draw background
    screen.blit(bg_image, (0,0))

    # draw sprites
    platform_group.draw(screen)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # update display window
    pygame.display.update()
    
pygame.quit()
