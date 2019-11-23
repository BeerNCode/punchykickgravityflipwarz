import pygame
import logging
from pygame import Rect

logger = logging.getLogger(__name__)

class Entity(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h):
        super().__init__()
        self.rect = Rect(x, y, w, h)
        self.sprites = {}
        self.sprite_index = 0
        self.animation_delay = 2
        self.animation_index = 0

    def add_sprite(self, sprite_id, sheet, rectangle):
        sprite = sheet.image_at(rectangle)
        sprite.set_colorkey((0, 0, 0))
        self.sprites[sprite_id] = [sprite]

    def get_quadrance_to(self, other):
        dx = self.rect.centerx - other.rect.centerx
        dy = self.rect.centery - other.rect.centery
        return dx*dx + dy*dy

    def add_sprites(self, sprite_id, sheet, rectangle, amount, offset):
        sprites = []
        for i in range(amount):
            r = (rectangle[0]+offset[0]*i, rectangle[1]+offset[1]*i,rectangle[2],rectangle[3])
            sprite = sheet.image_at(r)
            sprite.set_colorkey((0, 0, 0))
            sprites.append(sprite)
        self.sprites[sprite_id] = sprites

    def set_sprite(self, sprite_id):
        self.images = self.sprites[sprite_id]

    def update_animation(self):
        try:
            self.animation_index += 1
            if self.animation_index >= self.animation_delay:
                self.sprite_index += 1
                self.animation_index = 0

            if self.sprite_index >= len(self.images):
                self.sprite_index = 0
            self.image = self.images[self.sprite_index]

        except Exception as e:
            logger.error("Something went wrong displaying the sprite.")
            logger.debug(f"[{self.sprite_index}] but got [{len(self.images)}]")
            logger.exception(e)
            self.sprite_index = 0
            self.animation_index = 00