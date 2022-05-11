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
        self.rect_top = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 1) 

    def update(self): #Animacion para que el obstculo de mueva
        self.rect.left -= self.vel_x

        self.rect_top.x = self.rect.x #para que rect se mantenga en la parte superior

    def stop(self): #detener el movimiento del obstaculo
        self.vel_x = 0 


