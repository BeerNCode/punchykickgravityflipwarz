import pygame, sys, json
from game import Game

GAME_NAME = "Punchy-Kick Gravity-Flip Warz"

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

CONTROLS = [
    {"up": pygame.K_UP,"down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "space": pygame.K_SPACE},
    {"up": pygame.K_w,"down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "space": pygame.K_e},
    {"up": pygame.K_t,"down": pygame.K_g, "left": pygame.K_f, "right": pygame.K_h, "space": pygame.K_y},
    {"up": pygame.K_i,"down": pygame.K_k, "left": pygame.K_j, "right": pygame.K_l, "space": pygame.K_o}
]

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption(GAME_NAME)
    screen =  pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    game = Game(screen)
    game.run()

    pygame.quit()
    sys.exit(0)