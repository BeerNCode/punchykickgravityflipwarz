import logging, pygame, os
from punchykickgravityflipwarz.sprite_sheet import SpriteSheet
from punchykickgravityflipwarz.entity import Entity

logger = logging.getLogger(__name__)

class ItemType(Entity): # A pickupable item in the world 
    def __init__(self, world):
        super().__init__(0, 0, 32, 32)
        self.name = "Unknown"
        self.item_size = 16
        self.world = world

    def action(self, player):
        logger.debug(f"Player [{player.name}] used a [{self.name}].")

class Grenades(ItemType):
    def __init__(self, world):
        super().__init__(world)
        self.name = "Grenades"
        self.item_size = 16
        self.grenades_sheet = SpriteSheet(os.path.join('punchykickgravityflipwarz', 'resources', "grenade.png"))
        self.explosion_sheet = SpriteSheet(os.path.join('punchykickgravityflipwarz', 'resources', "explosion.png"))
        self.max_time_out = 10
        self.time_out = 0
        self.add_sprite("default", self.grenades_sheet, (0, 0, self.item_size, self.item_size))
        self.set_sprite("default")
        self.update_animation()

    def action(self, player):
        if self.time_out != 0:
            return (False, [])

        super().action(player)
        self.time_out = self.max_time_out

        grenade = Grenade(self.world, player.rect.x, player.rect.y, self.explosion_sheet)
        grenade.add_sprite("default", self.grenades_sheet, (0, 0, self.item_size, self.item_size))
        grenade.set_sprite("default")
        grenade.update_animation()

        if player.direction == 0:
            grenade.vel_x = -5
        else:
            grenade.vel_x = 5

        grenade.vel_y = -6

        return (False, [grenade]) # returns whether its used up, and any items needed to be created.

    def update(self):
        if self.time_out > 0:
            self.time_out -= 1

class Item(Entity): # got to be an entity to be rendered

    def __init__(self, world, x, y, w, h):
        super().__init__(x, y, w, h)
        self.world = world
        self.vel_x = 0
        self.vel_y = 0
        self.direction = 0
        self.timer = 100
        self.fixed = False

    def update(self):
        if not self.fixed:
            # left/right
            self.rect.x += self.vel_x
            tile_hit_list = pygame.sprite.spritecollide(self, self.world.tiles, False)
            for tile in tile_hit_list:
                if self.vel_x > 0:
                    self.rect.right = tile.rect.left
                elif self.vel_x < 0:
                    self.rect.left = tile.rect.right
                self.vel_x = 0

            # up/down movement  
            if self.vel_y == 0:
                self.vel_y = 1
            else:
                self.vel_y += .35

            self.rect.y += self.vel_y
            tile_hit_list = pygame.sprite.spritecollide(self, self.world.tiles, False)
            for tile in tile_hit_list:
                self.vel_x *= 0.95
                if abs(self.vel_x) < 0.01:
                    self.vel_x = 0

                if self.vel_y > 0:
                    self.rect.bottom = tile.rect.top
                    self.vel_y = -self.vel_y
                    if self.vel_y < 0.01:
                        self.vel_y = 0

                elif self.vel_y < 0:
                    self.rect.top = tile.rect.bottom
                    self.vel_y = 0

        super().update_animation()

class Grenade(Item):
    def __init__(self, world, x, y, explosion_sheet):
        super().__init__(world, x, y, 16, 16)
        self.timer = 100
        self.explosion_sheet = explosion_sheet

    def update(self):
        super().update()
        self.timer -= 1
        if self.timer <= 0:
            offset = 8-96/2.0
            explosion = Explosion(self.world, self.rect.x+offset, self.rect.y+offset)
            explosion.add_sprites("default", self.explosion_sheet, (0, 0, 96, 96), 6, (0, 96))
            explosion.set_sprite("default")
            explosion.update_animation()
            return (True, [explosion])
        return (False, [])

class Explosion(Item):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 96, 96)
        self.frame = 6
        self.fixed = True

    def update(self):
        super().update()
        self.frame -= 1
        if self.frame <= 0: 
            for tile in self.world.tiles:
                quadrance = self.get_quadrance_to(tile)
                if quadrance < 100*100:
                    tile.health -= 100
                    tile.hit = True;
                elif quadrance < 200*200: 
                    tile.health -= 50
                    tile.hit = True;
                elif quadrance < 400*400: 
                    tile.health -= 25
                    tile.hit = True;
            return (True, [])
        else: 
            return (False, [])
            
class Gun(ItemType):
    def __init__(self, world):
        super().__init__(world)
        self.name = "Gun"
        self.item_size = 16
        self.grenades_sheet = SpriteSheet(os.path.join('punchykickgravityflipwarz', 'resources', "grenade.png"))
        self.max_time_out = 5
        self.time_out = 0

    def action(self, player):
        if self.time_out != 0:
            return (False, [])

        super().action(player)
        self.time_out = self.max_time_out

        bullet = Bullet(self.world, player.rect.x, player.rect.y, self.explosion_sheet)
        bullet.add_sprite("default", self.grenades_sheet, (0, 0, self.item_size, self.item_size))
        bullet.set_sprite("default")
        bullet.update_animation()

        if player.direction == 0:
            bullet.vel_x = -16
        else:
            bullet.vel_x = 16

        return (False, [bullet]) # returns whether its used up, and any items needed to be created.

    def update(self):
        if self.time_out > 0:
            self.time_out -= 1

class Bullet(Item):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 16, 16)

    def update(self):
        super().update()
        self.timer -= 1
        if self.timer <= 0:
            offset = 8-96/2.0
            explosion = Explosion(self.world, self.rect.x+offset, self.rect.y+offset)
            explosion.add_sprites("default", self.explosion_sheet, (0, 0, 96, 96), 6, (0, 96))
            explosion.set_sprite("default")
            explosion.update_animation()
            return (True, [explosion])
        return (False, [])
