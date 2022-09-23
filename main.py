from frontier_hero.level import Level
import pygame

from frontier_hero.sprite import Sprite, LEFT, RIGHT, UP, DOWN
from frontier_hero.tile_cache import TileCache


TILE_SIZE = 16


def can_move(pos):
    return not sprite.is_moving() and not level.is_blocking(pos[0], pos[1])


if __name__ == "__main__":
    screen = pygame.display.set_mode((424, 320))

    MAP_CACHE = TileCache(TILE_SIZE, TILE_SIZE)
    SPRITE_CACHE = TileCache(TILE_SIZE, 24)

    clock = pygame.time.Clock()
    level = Level(MAP_CACHE, TILE_SIZE, TILE_SIZE, 'resources/midgaard.map')
    background = level.render()
    screen.blit(background, (0, 0))
    pygame.display.update()
    sprites = pygame.sprite.RenderUpdates()
    sprite = Sprite((2, 1), SPRITE_CACHE['fireas.png'])
    sprites.add(sprite)
    game_over = False
    while not game_over:
        warp = level.get_warp(int(sprite.pos[0]), int(sprite.pos[1]))
        if warp:
            sprite.pos = level.get_to(int(sprite.pos[0]), int(sprite.pos[1]))
            level = Level(MAP_CACHE, TILE_SIZE, TILE_SIZE, 'resources/' + warp)
            background = level.render()
            screen.blit(background, (0, 0))
            pygame.display.update()
        sprites.clear(screen, background)
        sprites.update()
        dirty = sprites.draw(screen)
        pygame.display.update(dirty)
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and can_move((int(sprite.pos[0]) - 1, int(sprite.pos[1]))):
            sprite.move(-TILE_SIZE, 0)
            sprite.direction = LEFT
        if keys[pygame.K_RIGHT] and can_move((int(sprite.pos[0]) + 1, int(sprite.pos[1]))):
            sprite.move(TILE_SIZE, 0)
            sprite.direction = RIGHT
        if keys[pygame.K_UP] and can_move((int(sprite.pos[0]), int(sprite.pos[1]) - 1)):
            sprite.move(0, -TILE_SIZE)
            sprite.direction = UP
        if keys[pygame.K_DOWN] and can_move((int(sprite.pos[0]), int(sprite.pos[1]) + 1)):
            sprite.move(0, TILE_SIZE)
            sprite.direction = DOWN
