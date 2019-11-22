import pygame
import threading
import logging
import colours
from controls import Controls
from player import Player

CONTROLS = [
    {"up": pygame.K_UP,"down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "space": pygame.K_SPACE},
    {"up": pygame.K_w,"down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "space": pygame.K_e},
    {"up": pygame.K_t,"down": pygame.K_g, "left": pygame.K_f, "right": pygame.K_h, "space": pygame.K_y},
    {"up": pygame.K_i,"down": pygame.K_k, "left": pygame.K_j, "right": pygame.K_l, "space": pygame.K_o}
]

GAME_SPEED = 60
CLIENT_TIMEOUT = 1000
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

logger = logging.getLogger(__name__)

class Game:
   
    def __init__(self, screen):
        self.screen = screen
        self.players = []
        self.clock = pygame.time.Clock()
        self.start_ticks=pygame.time.get_ticks()
        self.running = True

        self.players.append(Player("Bob", Controls(keys=CONTROLS[0])))

    def run(self):
        while self.running:
            pygame.event.pump()
            self.update_events()
            
            for player in self.players:
                player.update()

            self.render()
            
            self.update_timer()
            pygame.display.flip()
            self.clock.tick(GAME_SPEED)

    def update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Ending the game.")
                self.running = False

            if event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH = event.w
                SCREEN_HEIGHT = event.h
                logger.info(f"Resizing the window to {SCREEN_WIDTH}x{SCREEN_HEIGHT}.")
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    def render(self):
        self.screen.fill(colours.LIGHT_GREY)
        player_sprites = pygame.sprite.Group()

        #self.world.show(self.screen)
       
        for player in self.players:
            player.show(self.screen)
            player_sprites.add(player)

        player_sprites.draw(self.screen)

    def update_timer(self):
        seconds=(pygame.time.get_ticks()-self.start_ticks)/1000 
        if seconds>10000: 
            self.running = False