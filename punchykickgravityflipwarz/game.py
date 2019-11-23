GAME_SPEED = 60
CLIENT_TIMEOUT = 1000
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1024

import pygame, threading, logging
from random import randint
import punchykickgravityflipwarz.colours
from punchykickgravityflipwarz.item import *
from punchykickgravityflipwarz.controls import Controls
from punchykickgravityflipwarz.player import Player
from punchykickgravityflipwarz.world import World

CONTROLS = [
    {"up": pygame.K_UP,"down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "space": pygame.K_SPACE},
    {"up": pygame.K_w,"down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "space": pygame.K_e},
    {"up": pygame.K_t,"down": pygame.K_g, "left": pygame.K_f, "right": pygame.K_h, "space": pygame.K_y},
    {"up": pygame.K_i,"down": pygame.K_k, "left": pygame.K_j, "right": pygame.K_l, "space": pygame.K_o}
]

screen_colour = (randint(0,255),randint(0,255),randint(0,255))

logger = logging.getLogger(__name__)

sprite_sheets = {
}

class Game:
   
    def __init__(self, screen):
        self.screen = screen
        self.players = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.item_types = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.start_ticks=pygame.time.get_ticks()
        self.running = True
        self.world = World(self)
        
        self.gravity_timer = 300

        self.players.add(Player("Bob", Controls(keys=CONTROLS[0]), "player.png", self))
        self.players.add(Player("Dave", Controls(keys=CONTROLS[1]), "player_2.png", self))
        
        self.background_surface = pygame.image.load(os.path.join('punchykickgravityflipwarz', 'resources', "sky.png"))

    def run(self):
        while self.running:
            pygame.event.pump()
            self.update_events()
            
            self.players.update()
            
            #self.gravity()
            
            # Sort out item logic
            all_new_items = []
            finished_items = []
            for item in self.items:
                item_finished, new_items = item.update()
                if item_finished: finished_items.append(item)
                for new_item in new_items: all_new_items.append(new_item)
            for item in all_new_items: self.items.add(item)
            for item in finished_items: self.items.remove(item)

            self.world.update()
            self.draw()
            
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

    def draw(self):
        #self.screen.blit(self.background_surface, (0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill((143, 242, 234))
        self.world.draw(self.screen)
        self.players.draw(self.screen)
        self.item_types.draw(self.screen)
        self.items.draw(self.screen)

    def gravity(self):
        self.gravity_timer -= 1
        if self.gravity_timer == 0:
            self.gravity_timer = randint(10,200)
            g = float(randint(-100,100))/100
            for p in self.players:
                p.gravity = g
        
    def update_timer(self):
        seconds=(pygame.time.get_ticks()-self.start_ticks)/1000 
        if seconds>10000: 
            self.running = False