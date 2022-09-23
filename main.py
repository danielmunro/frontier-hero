from frontier_hero.level import Level
import pygame

from frontier_hero.sprite import Sprite
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
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    sprite.move(-16, 0)
                elif event.key == pygame.K_RIGHT:
                    sprite.move(16, 0)
                elif event.key == pygame.K_UP:
                    sprite.move(0, -16)
                elif event.key == pygame.K_DOWN:
                    sprite.move(0, 16)
