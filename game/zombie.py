import os
import pygame
from .constants import *

class Zombie(pygame.sprite.Sprite):

    def __init__(self, left, bottom, dir_images):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load( os.path.join(dir_images, 'zombie.png'))
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.bottom = bottom
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y = self.rect.bottom 
        self.vel_y = 0
        self.can_jump = False 
        self.zombie = True

    def collide_with(self, sprites): #colision entre obstaculos
        objects = pygame.sprite.spritecollide(self, sprites, False, pygame.sprite.collide_mask)
        if objects:
            return objects[0]

    def collide_bottom(self, cactus):
        return self.rect.colliderect(cactus.rect_top)

    def skid(self, cactus):
        self.pos_y = cactus.rect.top
        self.vel_y = 0
        self.can_jump = True
    
    def validate_platform(self, platform): #para detener la caida del personaje
        result = pygame.sprite.collide_rect(self, platform)
        if result:
            self.vel_y = 0 
            self.pos_y = platform.rect.top
            self.can_jump = True

    def jump(self): #implementar salto
        if self.can_jump:
            self.vel_y = -23
            self.can_jump = False 
            self.zombie = True 

    def update_pos(self):
        self.vel_y += ZOMBIE_GRAV # gravedad
        self.pos_y += self.vel_y + 0.5 * ZOMBIE_GRAV

    def update(self):
        if self.zombie:
            self.update_pos()

            self.rect.bottom = self.pos_y #actualizacion

    def stop(self):
        self.zombie = False

