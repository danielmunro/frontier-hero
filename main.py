from frontier_hero.level import Level
from fractions import Fraction
import pygame

from frontier_hero.sprite import Sprite, LEFT, RIGHT, UP, DOWN
from frontier_hero.tile_cache import TileCache


TILE_SIZE = 16
TICKS = 50
RESOURCES_DIR = 'resources/'
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 256


def can_move(pos):
    return not player_sprite.is_moving() and not level.is_blocking(int(pos[0]), int(pos[1]))


if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    map_cache = TileCache(TILE_SIZE, TILE_SIZE)
    player_sprite_cache = TileCache(TILE_SIZE, 24)

    clock = pygame.time.Clock()
    level = Level(map_cache, TILE_SIZE, TILE_SIZE, RESOURCES_DIR + 'midgaard.map')
    background = level.render()
    player_sprite = Sprite((4, 5), player_sprite_cache['fireas.png'])
    offset_x = 192
    offset_y = 56
    screen.blit(background, (offset_x, offset_y))
    game_over = False
    while not game_over:
        warp = level.get_warp(int(player_sprite.pos[0]), int(player_sprite.pos[1]))
        if warp:
            player_sprite.pos = level.get_to(int(player_sprite.pos[0]), int(player_sprite.pos[1]))
            level = Level(map_cache, TILE_SIZE, TILE_SIZE, RESOURCES_DIR + warp)
            background = level.render()
        screen.fill((0, 0, 0))
        if player_sprite.to_amount != (0, 0):
            player_sprite.update()
            dx = 0
            dy = 0
            if player_sprite.to_amount[0] > 0:
                dx = -1
            elif player_sprite.to_amount[0] < 0:
                dx = 1
            elif player_sprite.to_amount[1] > 0:
                dy = -1
            elif player_sprite.to_amount[1] < 0:
                dy = 1
            player_sprite.to_amount = (player_sprite.to_amount[0] + dx, player_sprite.to_amount[1] + dy)
            offset_x = offset_x + dx
            offset_y = offset_y + dy
        screen.blit(background, (offset_x, offset_y))
        screen.blit(player_sprite.image, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        pygame.display.update()
        clock.tick(TICKS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        keys = pygame.key.get_pressed()
        direction = player_sprite.direction
        if keys[pygame.K_LEFT] and can_move((player_sprite.pos[0] - 1, player_sprite.pos[1])):
            player_sprite.to_amount = (-TILE_SIZE, 0)
            player_sprite.pos = (player_sprite.pos[0] - 1, player_sprite.pos[1])
            direction = player_sprite.direction
            player_sprite.direction = LEFT
        if keys[pygame.K_RIGHT] and can_move((player_sprite.pos[0] + 1, player_sprite.pos[1])):
            player_sprite.to_amount = (TILE_SIZE, 0)
            player_sprite.pos = (player_sprite.pos[0] + 1, player_sprite.pos[1])
            direction = player_sprite.direction
            player_sprite.direction = RIGHT
        if keys[pygame.K_UP] and can_move((player_sprite.pos[0], player_sprite.pos[1] - 1)):
            player_sprite.to_amount = (0, -TILE_SIZE)
            player_sprite.pos = (player_sprite.pos[0], player_sprite.pos[1] - 1)
            direction = player_sprite.direction
            player_sprite.direction = UP
        if keys[pygame.K_DOWN] and can_move((player_sprite.pos[0], player_sprite.pos[1] + 1)):
            player_sprite.to_amount = (0, TILE_SIZE)
            player_sprite.pos = (player_sprite.pos[0], player_sprite.pos[1] + 1)
            direction = player_sprite.direction
            player_sprite.direction = DOWN
        if direction != player_sprite.direction:
            next(player_sprite.animation)
