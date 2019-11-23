import logging, pygame, os
from punchykickgravityflipwarz.sprite_sheet import SpriteSheet
from punchykickgravityflipwarz.entity import Entity

logger = logging.getLogger(__name__)

class ItemType(Entity): # A pickupable item in the world 
    def __init__(self, player, game):
        super().__init__(0, 0, 32, 32)
        self.name = "Unknown"
        self.item_size = 16
        self.game = game
        self.player = player

    def action(self):
        pass

class Grenades(ItemType):
    def __init__(self, player, game):
        super().__init__(player, game)
        self.name = "Grenades"
        self.item_size = 16
        self.grenades_sheet = SpriteSheet(os.path.join('punchykickgravityflipwarz', 'resources', "grenade.png"))
        self.explosion_sheet = SpriteSheet(os.path.join('punchykickgravityflipwarz', 'resources', "explosion.png"))
        self.max_time_out = 10
        self.time_out = 0
        self.add_sprite("default", self.grenades_sheet, (0, 0, self.item_size, self.item_size))
        self.set_sprite("default")
        self.update_animation()

    def action(self):
        if self.time_out != 0:
            return (False, [])

        super().action()
        self.time_out = self.max_time_out

        grenade = Grenade(self.game, self.player.rect.centerx, self.player.rect.centery, self.explosion_sheet)
        grenade.add_sprite("default", self.grenades_sheet, (0, 0, self.item_size, self.item_size))
        grenade.set_sprite("default")
        grenade.update_animation()

        if self.player.direction == 0:
            grenade.vel_x = -5
        else:
            grenade.vel_x = 5

        grenade.vel_y = -6

        return (False, [grenade]) # returns whether its used up, and any items needed to be created.

    def update(self):
        if self.time_out > 0:
            self.time_out -= 1

class Item(Entity): # got to be an entity to be rendered

    def __init__(self, player, game, x, y, w, h):
        super().__init__(x, y, w, h)
        self.player = player
        self.game = game
        self.vel_x = 0
        self.vel_y = 0
        self.direction = 0
        self.timer = 100
        self.fixed = False

    def update(self):
        if not self.fixed:
            # left/right
            self.rect.x += self.vel_x
            tile_hit_list = pygame.sprite.spritecollide(self, self.game.world.tiles, False)
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
            tile_hit_list = pygame.sprite.spritecollide(self, self.game.world.tiles, False)
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
    def __init__(self, player, game, x, y, explosion_sheet):
        super().__init__(player, game, x, y, 16, 16)
        self.timer = 100
        self.explosion_sheet = explosion_sheet

    def update(self):
        super().update()
        self.timer -= 1
        if self.timer <= 0:
            offset = 8-96/2.0
            explosion = Explosion(self.game, self.rect.x+offset, self.rect.y+offset)
            explosion.add_sprites("default", self.explosion_sheet, (0, 0, 96, 96), 6, (0, 96))
            explosion.set_sprite("default")
            explosion.update_animation()
            return (True, [explosion])
        return (False, [])

class Explosion(Item):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 96, 96)
        self.frame = 6
        self.fixed = True

    def update(self):
        super().update()
        self.frame -= 1
        if self.frame <= 0: 
            for tile in self.game.world.tiles:
                quadrance = self.get_quadrance_to(tile)
                if quadrance < 100*100:
                    tile.health -= 100
                    tile.hit = True
                elif quadrance < 200*200: 
                    tile.health -= 50
                    tile.hit = True
                elif quadrance < 400*400: 
                    tile.health -= 25
                    tile.hit = True
            return (True, [])
        else: 
            return (False, [])
            
class Gun(ItemType):
    def __init__(self, player, game):
        super().__init__(player, game)
        self.name = "Gun"
        self.item_size = 32
        self.gun_sheet = SpriteSheet(os.path.join('punchykickgravityflipwarz', 'resources', "gun.png"))
        self.bullet_sheet = SpriteSheet(os.path.join('punchykickgravityflipwarz', 'resources', "bullet.png"))
        self.max_time_out = 5
        self.time_out = 0
        self.add_sprite("left", self.gun_sheet, (0, 0, self.item_size, self.item_size),False)
        self.add_sprite("right", self.gun_sheet, (0, 0, self.item_size, self.item_size),True)
        self.set_sprite("left")
        self.update_animation()

    def action(self):
        if self.time_out != 0:
            return (False, [])

        super().action()
        self.time_out = self.max_time_out

        bullet = Bullet(self.player, self.game, self.player.rect.centerx, self.player.rect.centery)
        bullet.add_sprite("left", self.bullet_sheet, (0, 0, 8, 8),False)
        bullet.add_sprite("right", self.bullet_sheet, (0, 0, 8, 8),True)

        if self.player.direction == 0:
            bullet.set_sprite("left")
            bullet.vel_x = -30
        else:
            bullet.set_sprite("right")
            bullet.vel_x = 30

        bullet.update_animation()

        return (False, [bullet]) # returns whether its used up, and any items needed to be created.

    def update(self):
        if self.time_out > 0:
            self.time_out -= 1
        if self.player.direction == 0:
            self.set_sprite("left")
        else:
            self.set_sprite("right")
        
        super().update_animation()

class Bullet(Item):
    def __init__(self, player, game, x, y):
        super().__init__(player, game, x, y, 8, 8)
        self.time_delay = 18
    
    def update(self):
        super().update()
        self.time_delay -= 1
        if self.time_delay <= 0: return (True, []) 
        
        if self.rect.x < 0 or self.rect.x > 2000: return (True, []) 
        elif self.rect.y < 0 or self.rect.y > 2000: return (True, [])
        
        player_hit_list = pygame.sprite.spritecollide(self, self.game.players, False)
        for hit_player in player_hit_list:
            if hit_player is not self.player:
                hit_player.acc_x = self.vel_x
        
        return (False, [])
