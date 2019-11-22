import pygame, sys, json
from game import Game

GAME_NAME = "Punchy-Kick Gravity-Flip Warz"

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768



if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption(GAME_NAME)
    screen =  pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    game = Game(screen)
    game.run()

    pygame.quit()
    sys.exit(0)