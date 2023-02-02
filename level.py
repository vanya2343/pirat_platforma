import pygame
from tile import *
from settings import tile_size,screen_width
from player import *

class Level:
    def __init__(self,level_data,screen):
        self.display_surface = screen
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0
    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        self.player.update()
        self.horizontal_movement_collosion()
        self.vertical_movement_collosion()
        self.player.draw(self.display_surface)
    def setup_level(self,layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index,row in enumerate(layout):
            for col_index,col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == "X":
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)
                if col == "P":
                    player = Player((x, y))
                    self.player.add(player)
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x  < screen_width/6 and direction_x < 0:
            self.world_shift = 3
            player.speed = 0
        elif player_x > screen_width-screen_width/6 and direction_x > 0:
            self.world_shift = -3
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 3
    def horizontal_movement_collosion(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        if (player.rect.left < self.current_x or player.direction.x >= 0) and player.on_left:
            player.on_left = False
        if (player.rect.right < self.current_x or player.direction.x <= 0) and player.on_right:
            player.on_right = False
    def vertical_movement_collosion(self):
        player = self.player.sprite
        player.appli_gravity()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceilig = True
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceilig = False