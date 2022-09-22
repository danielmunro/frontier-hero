from frontier_hero.level import Level
import pygame

from frontier_hero.tile_cache import TileCache


if __name__ == "__main__":
    screen = pygame.display.set_mode((424, 320))

    MAP_TILE_WIDTH = 16
    MAP_TILE_HEIGHT = 16
    MAP_CACHE = TileCache(MAP_TILE_WIDTH, MAP_TILE_HEIGHT)

    clock = pygame.time.Clock()
    level = Level(MAP_CACHE, MAP_TILE_WIDTH, MAP_TILE_HEIGHT, 'resources/midgaard.map')
    background = level.render()
    overlays = pygame.sprite.RenderUpdates()
    screen.blit(background, (0, 0))
    game_over = False
    while not game_over:
        overlays.draw(screen)
        pygame.display.flip()
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                pressed_key = event.key
