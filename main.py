from frontier_hero.level import Level
import pygame


def load_tile_table(filename, width, height):
    image = pygame.image.load(filename).convert()
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, round(image_width / width)):
        line = []
        tile_table.append(line)
        for tile_y in range(0, round(image_height / height)):
            rect = (tile_x * width, tile_y * height, width, height)
            line.append(image.subsurface(rect))
    return tile_table


if __name__ == "__main__":
    screen = pygame.display.set_mode((424, 320))

    MAP_TILE_WIDTH = 16
    MAP_TILE_HEIGHT = 16
    MAP_CACHE = {
        'basictiles.png': load_tile_table('resources/basictiles.png', MAP_TILE_WIDTH,
                                          MAP_TILE_HEIGHT),
    }

    level = Level(MAP_CACHE, MAP_TILE_WIDTH, MAP_TILE_HEIGHT, 'resources/midgaard.map')

    clock = pygame.time.Clock()

    background = level.render()
    overlays = pygame.sprite.RenderUpdates()
    screen.blit(background, (0, 0))
    overlays.draw(screen)
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
