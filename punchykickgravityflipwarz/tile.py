import pygame
import punchykickgravityflipwarz.colours as colours
from punchykickgravityflipwarz.entity import Entity

TILE_SIZE = 16

class Tile(Entity):

    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill(colours.RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.damage = 0

    def tile_type(self, tile_value):
        if tile_value < 0.03:
            self.image.fill(colours.BLUE)
        elif tile_value < 0.1:
            self.image.fill(colours.BROWN)
        elif tile_value < 1.0:
            self.image.fill(colours.GREEN)


    