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