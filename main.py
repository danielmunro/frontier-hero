from frontier_hero.level import Level
import pygame

from frontier_hero.sprite import Sprite, LEFT, RIGHT, UP, DOWN
from frontier_hero.tile_cache import TileCache


TILE_SIZE = 16
TICKS = 30


def can_move(pos):
    return not player_sprite.is_moving() and not level.is_blocking(int(pos[0]), int(pos[1]))


if __name__ == "__main__":
    screen = pygame.display.set_mode((424, 320))

    map_cache = TileCache(TILE_SIZE, TILE_SIZE)
    player_sprite_cache = TileCache(TILE_SIZE, 24)

    clock = pygame.time.Clock()
    level = Level(map_cache, TILE_SIZE, TILE_SIZE, 'resources/midgaard.map')
    background = level.render()
    screen.blit(background, (0, 0))
    pygame.display.update()
    sprites = pygame.sprite.RenderUpdates()
    player_sprite = Sprite((4, 5), player_sprite_cache['fireas.png'])
    sprites.add(player_sprite)
    game_over = False
    while not game_over:
        warp = level.get_warp(int(player_sprite.pos[0]), int(player_sprite.pos[1]))
        if warp:
            player_sprite.pos = level.get_to(int(player_sprite.pos[0]), int(player_sprite.pos[1]))
            level = Level(map_cache, TILE_SIZE, TILE_SIZE, 'resources/' + warp)
            background = level.render()
            screen.blit(background, (0, 0))
            pygame.display.update()
        sprites.clear(screen, background)
        sprites.update()
        dirty = sprites.draw(screen)
        pygame.display.update(dirty)
        clock.tick(TICKS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and can_move((player_sprite.pos[0] - 1, player_sprite.pos[1])):
            player_sprite.move(-TILE_SIZE, 0)
            player_sprite.direction = LEFT
        if keys[pygame.K_RIGHT] and can_move((player_sprite.pos[0] + 1, player_sprite.pos[1])):
            player_sprite.move(TILE_SIZE, 0)
            player_sprite.direction = RIGHT
        if keys[pygame.K_UP] and can_move((player_sprite.pos[0], player_sprite.pos[1] - 1)):
            player_sprite.move(0, -TILE_SIZE)
            player_sprite.direction = UP
        if keys[pygame.K_DOWN] and can_move((player_sprite.pos[0], player_sprite.pos[1] + 1)):
            player_sprite.move(0, TILE_SIZE)
            player_sprite.direction = DOWN
