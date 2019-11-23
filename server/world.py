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
WIDTH = 1024
HEIGHT = 768

tile_sprites = sprite_sheet.spritesheet(os.path.join('server', 'resources', "block.jpg"))

class World:
    
    def __init__(self):
        self.tiles = pygame.sprite.Group()
        self.scale = 8

<<<<<<< HEAD
        num = randint(0,10)
        for y in range(0, 50):
            num = num + randint(-10,15)
            num2 = randint(0,128)
            num3 = randint(5,30)
            for x in range(0,randint(5,20)):
                for z in range(0,num3):
                    tile = Tile((num + x) * TILE_SIZE, (128 - num2) * TILE_SIZE + z)
                    self.tiles.add(tile)

        for x in range(0,WIDTH):
            for y in range(0,10):    
                tile = Tile(x, HEIGHT-y)
                self.tiles.add(tile)
=======
        for x in range(0, 200):
            tile = Tile(x * TILE_SIZE, 300)
            self.tiles.add(tile)
>>>>>>> ba116fc6cc5348ea55b7ab632069056e93253efa

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
