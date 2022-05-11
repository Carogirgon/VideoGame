from game import Cowboy_zombie

def main():
    cowboy_zombie_game = Cowboy_zombie()
    cowboy_zombie_game.start()

if __name__ == '__main__':
    main()



#pygame.mixer.music.load('game/sounds/intro.wav')
#pygame.mixer.music.set_volume(1.0) #float 0.0 - 1.0
#pygame.mixer.music.play(-1, 0.2 ) # cuanta veces, en que momento comenzar
#pygame.mixer.music.rewind() #para reiniciar la cancion
#pygame.mixer.music.pause() #pausar la cancion
#pygame.mixer.music.stop() #detener la cancion
#pygame.mixer.music.fadeout(5000) #detiene la cancion paulatinamente
