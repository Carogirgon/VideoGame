import os
import sys
import random
import pygame
from .constants import *
from .brains import Brains
from .cactus import Cactus
from .zombie import Zombie
from .platform import Platform

class Cowboy_zombie:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WIDHT, HEIGHT))
        self.title = pygame.display.set_caption(TITLE)
        self.background = pygame.transform.scale(pygame.image.load(os.path.join('game/image/desert.png')),(WIDHT, HEIGHT))
        self.music = pygame.mixer.music.load('game/sounds/intro.wav')
        self.music = pygame.mixer.music.set_volume(0.3)
        self.music = pygame.mixer.music.play(-1)
        self.running = True
        self.zombie = True
        self.vel_y = 0
        self.clock = pygame.time.Clock()
        self.font = pygame.font.match_font(FONT)
        self.dir = os.path.dirname(__file__)
        self.dir_sounds = os.path.join(self.dir, 'sounds')
        self.dir_images = os.path.join(self.dir, 'image')

    def start(self):
        self.menu()
        self.new_game()

    def new_game(self):
        self.score = 0
        self.level = 0
        self.zombie = True
        self.generate_elements()
        self.run_game()

    def generate_elements(self):
        self.platform = Platform()
        self.zombie = Zombie(100, self.platform.rect.top - 200, self.dir_images)
        
        self.sprites = pygame.sprite.Group()
        self.cactus = pygame.sprite.Group() 
        self.brains = pygame.sprite.Group()

        self.sprites.add(self.platform)
        self.sprites.add(self.zombie)

        self.generate_cactus()

    def generate_cactus(self):

        last_posicion = WIDHT + 100

        if not len(self.cactus) > 0:

            for c in range(0, MAX_CACTUS):

                left = random.randrange(last_posicion + 200 ,last_posicion + 400 )
                cactus = Cactus(left, self.platform.rect.top, self.dir_images)

                last_posicion = cactus.rect.right
                self.sprites.add(cactus)
                self.cactus.add(cactus)

            self.level += 1         
            self.generate_brains()

    def generate_brains(self):
        last_position = WIDHT + 100

        for b in range(MAX_BRAINS):
            pos_x = random.randrange(last_position + 180, last_position + 300)
            brain = Brains(pos_x, 100, self.dir_images)

            last_position = brain.rect.right

            self.sprites.add(brain)
            self.brains.add(brain)

    def run_game(self):
        while True:
            self.clock.tick(FPS)
            self.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            key = pygame.key.get_pressed() #ejecutar el metodo jump

            if key[pygame.K_SPACE]:
                self.zombie.jump()

            if key[pygame.K_r] and not self.zombie:
                self.new() 

            self.surface.blit(self.background, (0, 0)) 
            self.draw_text()
            self.sprites.draw(self.surface)
            pygame.display.flip()

    def update(self):

        if self.zombie:
            if not self.zombie:
                return

            cactus = self.zombie.collide_with(self.cactus)
            if cactus:
                if self.zombie.collide_bottom(cactus):
                    self.zombie.skid(cactus)
                else:
                    self.stop()

            brain = self.zombie.collide_with(self.brains)
            if brain:
                self.score += 1
                brain.kill()

                sound = pygame.mixer.Sound(os.path.join(self.dir_sounds,'coin.wav'))
                sound.play() #sonido de moneda 

            self.sprites.update() # todos los elementos en la lista se actualizan

            self.zombie.validate_platform(self.platform) #detener la caida del personaje 
            
            self.update_elements(self.cactus)
            self.update_elements(self.brains)
            self.generate_cactus() # segeneran ordas de enemigos

    def update_elements(self, elements):
        for element in elements:
            if not element.rect.right > 0:
                element.kill()

    def stop(self):

        sound = pygame.mixer.Sound(os.path.join(self.dir_sounds,'lose.wav'))
        sound.play() #sonido de colision

        self.zombie.stop() #para detener al jugador
        self.stop_elements(self.cactus)

        self.zombie = False

    def stop_elements(self, elements):

        for element in elements:
            element.stop()

    def score_format(self):
        return 'Score : {}'.format(self.score)

    def level_format(self):
        return 'Level : {}'.format(self.level)

    def draw_text(self):
        self.display_text(self.score_format(), 30, BLACK, WIDHT // 2, 30)
        self.display_text(self.level_format(), 30, BLACK, 70, TEXT_POSTY)

        if not self.zombie:
            self.display_text('Perdiste', 40, WHITE, WIDHT // 2, HEIGHT // 2)
            self.display_text('Presiona r para comenzar de nuevo', 30, WHITE, WIDHT // 2, 100)

    def display_text(self, text, size, color, pos_x, pos_y): 
        font = pygame.font.Font(self.font, size)

        text = font.render(text, True, color)
        rect = text.get_rect()
        rect.midtop = (pos_x, pos_y)

        self.surface.blit(text,rect)

    def menu(self):
        self.main = pygame.transform.scale(pygame.image.load(os.path.join('game/image/intro.png')),(WIDHT, HEIGHT))
        self.surface.blit(self.main, (0, 0))
        self.display_text('Presiona ENTER para iniciar', 30, BLACK, WIDHT // 2, 460)

        pygame.display.flip()

        self.wait()

    def wait(self):
        wait = True

        while wait:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
                    self.running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYUP:
                    wait = False

    
