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
        self.music = pygame.mixer.music.set_volume(0.1)
        self.music = pygame.mixer.music.play(-1)
        self.running = True
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
        self.vel_x = SPEED
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
            self.vel_x += 1       
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

            key = pygame.key.get_pressed()

            if key[pygame.K_SPACE]:
                self.zombie.jump()

            if key[pygame.K_x] and not self.zombie.zombie:
                self.new_game() 

            self.surface.blit(self.background, (0, 0))
            self.draw_text()
            self.sprites.draw(self.surface)
            pygame.display.flip()

    def update(self):

        if self.zombie.lives > 0:

            cactus = self.zombie.collide_with(self.cactus)
            if cactus:
                self.zombie.hit(cactus)
                self.zombie.lives -= 1
                if self.zombie.lives == 0:
                    self.stop()

            brain = self.zombie.collide_with(self.brains)
            if brain:
                self.increment_score(brain.points)
                brain.kill()
                pygame.mixer.Sound(os.path.join(self.dir_sounds,'bite.wav')).play() 

            self.sprites.update()
            self.zombie.validate_platform(self.platform) 
            self.update_elements(self.cactus)
            self.update_elements(self.brains)
            self.generate_cactus()

    def update_elements(self, elements):
        for element in elements:
            element.set_vel_x(self.vel_x)

            if not element.rect.right > 0:
                element.kill()

    def stop(self):
        self.vel_x = 0
        self.zombie.stop()
        self.zombie.zombie = False
        self.stop_elements(self.cactus)
        pygame.mixer.Sound(os.path.join(self.dir_sounds, 'lose.wav')).play()

    def stop_elements(self, elements):
        for element in elements:
            element.stop()
            
    def next_level(self):
        self.level += 0
        self.vel_x += 1

    def increment_score(self, points=1):
        self.score += points

    def zombie_lives(self):
        return 'lives : {}'.format(self.zombie.lives)

    def score_format(self):
        return 'Score : {}'.format(self.score)

    def level_format(self):
        return 'Level : {}'.format(self.level)

    def draw_text(self):
        self.display_text(self.score_format(), 30, BLACK, WIDHT // 2, 30)
        self.display_text(self.level_format(), 30, BLACK, 70, TEXT_POSTY)
        self.display_text(self.zombie_lives(), 30, BLACK, 800, 30)

        if not self.zombie.zombie:
            self.display_text('PERDISTE!', 40, BLACK, WIDHT // 2, HEIGHT // 2)
            self.display_text('Presiona x para comenzar de nuevo', 30, BLACK, WIDHT // 2, 200)

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

