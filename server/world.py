from PIL import Image
import pygame
import colours, os
import sprite_sheet, logging
from entity import Entity
from vector import Vector
from random import randint

imageFile = os.path.join("server", "resources", "world.png")

logger = logging.getLogger(__name__)

TILE_SIZE = 8

tile_sprites = sprite_sheet.spritesheet(os.path.join('server', 'resources', "tiles.png"))

class World:
    
    def __init__(self):
        self.tiles = pygame.sprite.Group()
        self.scale = 8

        for x in range(0, 200):
            tile = Tile(randint(0, 128) * TILE_SIZE, randint(0, 128)*TILE_SIZE)
            self.tiles.add(tile)

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

    def show(self, screen):
        self.tiles.draw(screen)

    def get_index(self, x, y, width):
        return y * width + x

class Tile(Entity):

    def __init__(self, x, y):
        super().__init__()
        
        self.image = pygame.Surface([8, 8])
        self.image.fill(colours.RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
