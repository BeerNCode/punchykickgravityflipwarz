import pygame, os, logging, math
from PIL import Image
from random import randint
from pygame import Surface

import punchykickgravityflipwarz.colours
from punchykickgravityflipwarz.sprite_sheet import SpriteSheet
from punchykickgravityflipwarz.entity import Entity
from punchykickgravityflipwarz.vector import Vector
from punchykickgravityflipwarz.tile import Tile

imageFile = os.path.join("punchykickgravityflipwarz", "resources", "world.png")

logger = logging.getLogger(__name__)

TILE_SIZE = 16
WIDTH = 1024
HEIGHT = 768

tile_sprites = SpriteSheet(os.path.join('punchykickgravityflipwarz', 'resources', "block.jpg"))

class World:
    
    def __init__(self):
        self.tiles = pygame.sprite.Group()
        self.scale = 8

        if True: # random world
            for i in range(0, 50):
                platform_x = randint(0, (WIDTH / TILE_SIZE))
                platform_y = randint(0, HEIGHT / TILE_SIZE)
                platform_width = randint(5,15)
                for x in range(0, platform_width):
                    tile = Tile((platform_x + x) * TILE_SIZE, platform_y * TILE_SIZE)
                    self.tiles.add(tile)
        else:
            for x in range(0,10):    
                tile = Tile(x * TILE_SIZE, HEIGHT - 6 * TILE_SIZE)
                self.tiles.add(tile)

        for x in range(0, int(math.floor(WIDTH / TILE_SIZE))):
            tile = Tile(x * TILE_SIZE, HEIGHT - 2 * TILE_SIZE)
            self.tiles.add(tile)

        self.surface = Surface((WIDTH, HEIGHT))
        self.tiles.draw(self.surface)

    def get_world(self, screen):
        img = Image.open(imageFile)
        rgb_im = img.convert('RGB')

        width = rgb_im.size[1]

        for i in range (0,rgb_im.size[0]-1):
            for j in range (0,rgb_im.size[1]-1):
                if (rgb_im.getpixel((i,j)) == (0,0,0)):
                    #index = self.get_index(i, j, width)
                    #self.tiles[index] = 1
                    #scale = 4
                    pygame.draw.rect(screen, colours.BLACK, [i*self.scale, j*self.scale, self.scale, self.scale], 0)
                else:
                    #self.tiles[index] = 0
                    pygame.draw.rect(screen, colours.WHITE, [i*self.scale, j*self.scale, self.scale, self.scale], 0)

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))

    def get_index(self, x, y, width):
        return y * width + x


