import pygame
import random

class Minion(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, y, sprite_sheet, direction, scale):
        pygame.sprite.Sprite.__init__(self)
        # Movement
        self.direction = direction # Can be -1 or 1
        self.flip = True if self.direction == -1 else False

        # Animation
        self.animation_list = []
        self.frame_index = 0
        self.last_update_time = pygame.time.get_ticks()
        self.ANIMATIONS = 4

        # Load image animation
        for animation_index in range(1, self.ANIMATIONS + 1):
            image = sprite_sheet.get_image(animation_index, 32, 32, scale, (0, 0, 0))
            image = pygame.transform.flip(image, flip_x = self.flip, flip_y = False)
            image.set_colorkey((0, 0, 0))
            self.animation_list.append(image)

        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = 0 if self.direction == 1 else SCREEN_WIDTH
        self.rect.y = y
    
    def update(self, scroll = 0, SCREEN_WIDTH = 400):
        ANIMATION_COOLDOWN = 50

        self.image = self.animation_list[self.frame_index]
        if (pygame.time.get_ticks() - self.last_update_time) > ANIMATION_COOLDOWN:
            self.last_update_time = pygame.time.get_ticks()
            self.frame_index = (self.frame_index + 1) % self.ANIMATIONS
        
        # move object
        self.rect.x += self.direction * 2
        self.rect.y += scroll

        # isOffScreen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
