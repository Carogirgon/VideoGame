import pygame
from .constants import *

class Platform(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface( (WIDHT, 30) )
        self.image.fill(BROWN_LIGHT)
        self.image.set_colorkey(BROWN_LIGHT)

        self.rect = self.image.get_rect()
        self.rect.x = 0 
        self.rect.y = HEIGHT - 50