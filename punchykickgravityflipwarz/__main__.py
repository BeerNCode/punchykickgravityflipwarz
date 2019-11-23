import pygame, sys, json, logging, os

from punchykickgravityflipwarz.game import Game

GAME_NAME = "Punchy-Kick Gravity-Flip Warz"

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000
FORMAT = '%(asctime)-15s  %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    pygame.init()
    pygame.display.set_caption(GAME_NAME)
    screen =  pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    game = Game(screen)
    game.run()

    pygame.quit()
    sys.exit(0)