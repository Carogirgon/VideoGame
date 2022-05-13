import os
import pygame
from .constants import *

class Brains(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, dir_images):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load( os.path.join(dir_images, 'brain.png'))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)
        self.vel_x = 0
        self.points = 1

    def update(self):
        self.rect.left -= self.vel_x 

    def set_vel_x(self, vel_x):
        self.vel_x = vel_x

    def stop(self):
        self.vel_x = 0