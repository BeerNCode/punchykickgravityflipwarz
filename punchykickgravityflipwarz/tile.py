import pygame
import punchykickgravityflipwarz.colours as colours
from punchykickgravityflipwarz.entity import Entity
import punchykickgravityflipwarz.game
from random import randint

TILE_SIZE = 16

class Tile(Entity):

    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, TILE_SIZE, TILE_SIZE), 1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 0
        self.hit = False

    def tile_type(self, tile_value):
        if tile_value < 0.03:
            self.image.fill(colours.BLUE)
            self.health = 100
        elif tile_value < 0.1:
            self.image.fill(colours.GREEN)
            self.health = 200
        elif tile_value < 1.0:
            self.image.fill(colours.BROWN)
            self.health = 300


    