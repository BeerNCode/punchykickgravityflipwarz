import pygame
import threading
import logging
import colours
   
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

    def run(self):

        while self.running:
            pygame.event.pump()
            self.update_events()
            
            for player in self.players:
                player.update(self.world)

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

    def update_timer(self):
        seconds=(pygame.time.get_ticks()-self.start_ticks)/1000 
        if seconds>10000: 
            self.running = False