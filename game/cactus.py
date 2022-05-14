import os
import pygame
from .constants import *

class Cactus(pygame.sprite.Sprite):

    def __init__(self, left, bottom, dir_images):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join(dir_images, 'cactus.png'))
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.bottom = bottom
        self.mask = pygame.mask.from_surface(self.image)
        self.vel_x = SPEED
        #self.rect_top = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 1) 

    def update(self): 
        self.rect.left -= self.vel_x
        #self.rect_top.x = self.rect.x

    def set_vel_x(self, vel_x):
        self.vel_x = vel_x

    def stop(self): 
        self.vel_x = 0 