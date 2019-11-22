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

PLAYER_SPEED = 3
PLAYER_RADIUS = 15
PLAYER_DIAMETER = 2 * PLAYER_RADIUS

class Player(Entity):

    def __init__(self, name, controls):
        super().__init__()
        logger.debug(f"Creating player [{name}].")
        self.name = name
        self.controls = controls
        self.pos = Vector(0, 0)
        self.direction = 0

        tile_size = 32
        
        logger.debug(os.getcwd())

        sheet = sprite_sheet.spritesheet(os.path.join('server', 'resources','player.png'))
        super().add_sprite("stood_right", sheet, (0, 0, tile_size, tile_size))
        super().add_sprite("stood_left", sheet, (0, 0, tile_size, tile_size))
        super().add_sprites("walking_right", sheet, (tile_size, tile_size, tile_size, tile_size), 3, (tile_size, 0))
        super().add_sprites("walking_left", sheet, (tile_size, tile_size, tile_size, tile_size), 3, (tile_size, 0))

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

    def update(self):
        self.capture_inputs()
        
        speed = PLAYER_SPEED

        if self.pos.y <= 200:
            dy = 0
            self.pos.y = 200
        else:
            dy = 10

        self.pos.y += dy

        dx = 0
        movingHorizontally = False
        if self.key_left:
            dx = -speed
            super().set_sprite("walking_left")
            self.direction = 0
            movingHorizontally = True
        elif self.key_right:
            dx = speed
            super().set_sprite("walking_right")
            self.direction = 1
            movingHorizontally = True

        self.pos.x += dx

        if not movingHorizontally:
            if self.direction == 0:
                super().set_sprite("stood_left")
            elif self.direction == 1:
                super().set_sprite("stood_right")
        
    def show(self, screen):
        super().show()