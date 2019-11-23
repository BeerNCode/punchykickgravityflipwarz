import os, logging, json, threading, pygame, random, math

import punchykickgravityflipwarz.colours
from punchykickgravityflipwarz.sprite_sheet import SpriteSheet
from punchykickgravityflipwarz.entity import Entity
from punchykickgravityflipwarz.vector import Vector
from punchykickgravityflipwarz.item import *

logger = logging.getLogger(__name__)

TILE_SIZE = 32
PLAYER_JUMP_SPEED = 10
PLAYER_SPEED = 5
PLAYER_RADIUS = 15
PLAYER_DIAMETER = 2 * PLAYER_RADIUS

class Player(Entity):

    def __init__(self, name, controls, sprite_sheet_file_name, game):
        super().__init__(0, 0, TILE_SIZE, TILE_SIZE)
        logger.debug(f"Creating player [{name}].")
        self.name = name
        self.controls = controls
        self.vel_x = 0
        self.vel_y = 0
        self.direction = 0
        self.game = game
        self.item_type = Grenades(self.game.world)

        # Setup the sprites/animation.
        sheet = SpriteSheet(os.path.join('punchykickgravityflipwarz', 'resources', sprite_sheet_file_name))
        super().add_sprite("stood_right", sheet, (0, 0, TILE_SIZE, TILE_SIZE))
        super().add_sprite("stood_left", sheet, (3*TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SIZE))
        super().add_sprites("walking_right", sheet, (TILE_SIZE, 0, TILE_SIZE, TILE_SIZE), 3, (TILE_SIZE, 0))
        super().add_sprites("walking_left", sheet, (2*TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SIZE), 3, (-TILE_SIZE, 0))
        super().set_sprite("stood_right")
        super().update_animation()

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

        # items
        if self.item_type is not None:
            self.item_type.update()
            if self.key_space:
                item_finished, items = self.item_type.action(self)
                if item_finished:
                    self.item_type = None
                for item in items:
                    self.game.items.add(item)

        # Left/right movement       
        if self.key_left:
            self.vel_x = -PLAYER_SPEED
            super().set_sprite("walking_left")
            self.direction = 0
        elif self.key_right:
            super().set_sprite("walking_right")
            self.direction = 1
            self.vel_x = PLAYER_SPEED
        else:
            self.vel_x = 0
            if self.direction == 0:
                super().set_sprite("stood_left")
            elif self.direction == 1:
                super().set_sprite("stood_right")

        self.rect.x += self.vel_x
 
        tile_hit_list = pygame.sprite.spritecollide(self, self.game.world.tiles, False)
        for tile in tile_hit_list:
            if self.vel_x > 0:
                self.rect.right = tile.rect.left
            elif self.vel_x < 0:
                self.rect.left = tile.rect.right

        # up/down movement
        if self.game.world.gravity < 0:
            sign = -1
        else:
            sign = 1
        
        if self.vel_y == 0:
            self.vel_y = 1 * sign
        else:
            self.vel_y += self.game.world.gravity

        if self.key_up:
            self.rect.y += sign*2
            tile_hit_list = pygame.sprite.spritecollide(self, self.game.world.tiles, False)
            self.rect.y -= sign*2
                
            if len(tile_hit_list) > 0:
                self.vel_y = -1 * sign * PLAYER_JUMP_SPEED

        self.rect.y += self.vel_y

        tile_hit_list = pygame.sprite.spritecollide(self, self.game.world.tiles, False)
        for tile in tile_hit_list:
            if self.vel_y > 0:
                self.rect.bottom = tile.rect.top
            elif self.vel_y < 0:
                self.rect.top = tile.rect.bottom
            self.vel_y = 0

        super().update_animation()

    def show(self, screen):
        super().show()