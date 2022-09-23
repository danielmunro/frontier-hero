from frontier_hero.level import Level
import pygame

from frontier_hero.sprite import Sprite, LEFT, RIGHT, UP, DOWN
from frontier_hero.tile_cache import TileCache


if __name__ == "__main__":
    screen = pygame.display.set_mode((424, 320))

    MAP_TILE_WIDTH = 16
    MAP_TILE_HEIGHT = 16
    MAP_CACHE = TileCache(MAP_TILE_WIDTH, MAP_TILE_HEIGHT)
    SPRITE_CACHE = TileCache(16, 24)

    clock = pygame.time.Clock()
    level = Level(MAP_CACHE, MAP_TILE_WIDTH, MAP_TILE_HEIGHT, 'resources/midgaard.map')
    background = level.render()
    screen.blit(background, (0, 0))
    pygame.display.update()
    sprites = pygame.sprite.RenderUpdates()
    sprite = Sprite((2, 1), SPRITE_CACHE['fireas.png'])
    sprites.add(sprite)
    game_over = False
    while not game_over:
        sprites.clear(screen, background)
        sprites.update()
        dirty = sprites.draw(screen)
        pygame.display.update(dirty)
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not sprite.is_moving() and not level.is_blocking(int(sprite.pos[0] - 1), int(sprite.pos[1])):
            sprite.move(-16, 0)
            sprite.direction = LEFT
        if keys[pygame.K_RIGHT] and not sprite.is_moving() and not level.is_blocking(int(sprite.pos[0] + 1), int(sprite.pos[1])):
            sprite.move(16, 0)
            sprite.direction = RIGHT
        if keys[pygame.K_UP] and not sprite.is_moving() and not level.is_blocking(int(sprite.pos[0]), int(sprite.pos[1] - 1)):
            sprite.move(0, -16)
            sprite.direction = UP
        if keys[pygame.K_DOWN] and not sprite.is_moving() and not level.is_blocking(int(sprite.pos[0]), int(sprite.pos[1] + 1)):
            sprite.move(0, 16)
            sprite.direction = DOWN
