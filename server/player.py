import os
import logging
import json
import threading
import pygame
import colours
import random
import sprite_sheet
import math
from entity import Entity
from vector import Vector

logger = logging.getLogger(__name__)

TILE_SIZE = 32
PLAYER_JUMP = 10
PLAYER_SPEED = 5
PLAYER_RADIUS = 15
PLAYER_DIAMETER = 2 * PLAYER_RADIUS

class Player(Entity):

    def __init__(self, name, controls, sprite_sheet_file_name):
        super().__init__()
        logger.debug(f"Creating player [{name}].")
        self.name = name
        self.controls = controls
        self.vel_x = 0
        self.vel_y = 0
        self.direction = 0

        logger.debug(os.getcwd())

        sheet = sprite_sheet.spritesheet(os.path.join('server', 'resources', sprite_sheet_file_name))
        super().add_sprite("stood_right", sheet, (0, 0, TILE_SIZE, TILE_SIZE))
        super().add_sprite("stood_left", sheet, (3*TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SIZE))
        super().add_sprites("walking_right", sheet, (TILE_SIZE, 0, TILE_SIZE, TILE_SIZE), 3, (TILE_SIZE, 0))
        super().add_sprites("walking_left", sheet, (2*TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SIZE), 3, (-TILE_SIZE, 0))
        super().set_sprite("stood_right")
        super().show()

    def capture_inputs(self):
        keys = pygame.key.get_pressed()
        if self.controls.joystick is not None:
            joystick = self.controls.joystick
            hats = joystick.get_hat(0)
            self.key_up = hats[1]==1
            self.key_down = hats[1]==-1
            self.key_left = hats[0]==-1
            self.key_right = hats[0]==1
            if (joystick.get_numbuttons()>2):
                self.key_space = joystick.get_button( 1 )==1
            else:
                self.key_space = keys[self.controls.getKeys()["space"]]
        elif self.controls.network is not None:
            self.key_up = self.controls.network["state"]["up"]
            self.key_down = self.controls.network["state"]["down"]
            self.key_left = self.controls.network["state"]["left"]
            self.key_right = self.controls.network["state"]["right"]
            self.key_space = self.controls.network["state"]["a"]
        else:
            self.key_up = keys[self.controls.keys["up"]]
            self.key_down = keys[self.controls.keys["down"]]
            self.key_left = keys[self.controls.keys["left"]]
            self.key_right = keys[self.controls.keys["right"]]
            self.key_space = keys[self.controls.keys["space"]]

    def update(self, world):
        self.capture_inputs()

        # Left/right        
        movingHorizontally = False
        if self.key_left:
            self.vel_x = -PLAYER_SPEED
            super().set_sprite("walking_left")
            self.direction = 0
            movingHorizontally = True
        elif self.key_right:
            super().set_sprite("walking_right")
            self.direction = 1
            movingHorizontally = True
            self.vel_x = PLAYER_SPEED
        else:
            self.vel_x = 0

        self.rect.x += self.vel_x
 
        block_hit_list = pygame.sprite.spritecollide(self, world.tiles, False)
        for block in block_hit_list:
            if self.vel_x > 0:
                self.rect.right = block.rect.left
            elif self.vel_x < 0:
                self.rect.left = block.rect.right

        tile_hit_list = pygame.sprite.spritecollide(self, world.tiles, False)
        if len(tile_hit_list) > 0:
            logger.debug("hit")
            self.rect.x -= self.vel_x

        if not movingHorizontally:
            if self.direction == 0:
                super().set_sprite("stood_left")
            elif self.direction == 1:
                super().set_sprite("stood_right")

        # jump
        if self.key_up:
            self.rect.y += 2
            tile_hit_list = pygame.sprite.spritecollide(self, world.tiles, False)
            self.rect.y -= 2
 
            if len(tile_hit_list) > 0:
                self.vel_y = -PLAYER_JUMP

        # gravity        
        if self.vel_y == 0:
            self.vel_y = 1
        else:
            self.vel_y += .35
 
        self.rect.y += self.vel_y

        block_hit_list = pygame.sprite.spritecollide(self, world.tiles, False)
        for block in block_hit_list:
            if self.vel_y > 0:
                self.rect.bottom = block.rect.top
            elif self.vel_y < 0:
                self.rect.top = block.rect.bottom
            self.vel_y = 0

    def show(self, screen):
        super().show()