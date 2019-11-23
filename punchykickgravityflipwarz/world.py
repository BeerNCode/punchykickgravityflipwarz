import pygame, os, logging, math
from PIL import Image
from random import randint
from random import random
from pygame import Surface
import math

from punchykickgravityflipwarz.game import SCREEN_WIDTH, SCREEN_HEIGHT
import punchykickgravityflipwarz.colours
from punchykickgravityflipwarz.sprite_sheet import SpriteSheet
from punchykickgravityflipwarz.entity import Entity
from punchykickgravityflipwarz.vector import Vector
from punchykickgravityflipwarz.tile import Tile

import noise 
import numpy as np

imageFile = os.path.join("punchykickgravityflipwarz", "resources", "world.png")

logger = logging.getLogger(__name__)

TILE_SIZE = 16

SCALE = 10.0
OCTAVES = 10
PERSISTANCE = 0.35
LACUNARITY = 2.0

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

tile_sprites = SpriteSheet(os.path.join('punchykickgravityflipwarz', 'resources', "block.jpg"))

class World:
    
    def __init__(self, game):
        self.game = game
        self.tiles = pygame.sprite.Group()
        self.scale = 8

        self.noisy_world = np.zeros((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.noisy_world = self.generate_noise((SCREEN_WIDTH, SCREEN_HEIGHT), SCALE, OCTAVES, PERSISTANCE, LACUNARITY)
        for i in range(0, int(math.floor(SCREEN_WIDTH/TILE_SIZE))):
            for j in range(0, int(math.floor(SCREEN_HEIGHT/TILE_SIZE))):
                threshold = 1/(0.3*math.pow(j,2) + 1) - 0.1
                if (self.noisy_world[i][j] > threshold):
                    tile = Tile(i * TILE_SIZE, j * TILE_SIZE)
                    tile.tile_type(self.noisy_world[i][j])
                    self.tiles.add(tile)

        self.redraw()

    def redraw(self):
        self.surface = Surface(SCREEN_SIZE).convert()
        self.surface.set_colorkey((0, 0, 0))
        self.tiles.draw(self.surface)

    def update(self):
        needs_redraw = False
        for tile in self.tiles:
            if tile.hit:
                health_colour = max(min(int(tile.health),255),0)
                tile.image.fill((255,health_colour,health_colour))
                needs_redraw = True 
                if tile.health <= 0:
                    self.tiles.remove(tile)

        if needs_redraw:
            self.redraw()

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))

    def get_index(self, x, y, width):
        return y * width + x

    def generate_noise(self, shape, scale, octaves, persistance, lacunarity):
        offset_x = randint(0,1000)
        offset_y = randint(0,1000)
        for i in range (SCREEN_WIDTH):
            for j in range (SCREEN_HEIGHT):
                self.noisy_world[i][j] = noise.pnoise2(i/scale + offset_x, j/scale + offset_y, octaves=octaves, 
                                    persistence=PERSISTANCE, 
                                    lacunarity=LACUNARITY, 
                                    repeatx=SCREEN_WIDTH, 
                                    repeaty=SCREEN_HEIGHT, 
                                    base=0)
                #print(self.noisy_world[i][j])
        return self.noisy_world



