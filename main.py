from frontier_hero.level import Level
import pygame

from frontier_hero.sprite import MobSprite, LEFT, RIGHT, UP, DOWN
from frontier_hero.tile_cache import TileCache


def can_move(pos):
    return not player_sprite.is_moving() \
           and not level.is_blocking(int(pos[0]), int(pos[1])) \
           and not next((x for x in sprites if x.pos == pos), None)


def move_player(to_amount, to_pos, player_direction):
    player_sprite.to_amount = to_amount
    player_sprite.pos = to_pos
    player_sprite.direction = player_direction
    print(player_sprite.pos)


def get_offset():
    return (SCREEN_WIDTH / 2) - (player_sprite.pos[0] * TILE_SIZE),\
           (SCREEN_HEIGHT / 2) + 8 - (player_sprite.pos[1] * TILE_SIZE)


if __name__ == "__main__":
    TILE_SIZE = 16
    TICKS = 50
    RESOURCES_DIR = 'resources/'
    SCREEN_WIDTH = 512
    SCREEN_HEIGHT = 256

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    map_cache = TileCache(TILE_SIZE, TILE_SIZE)
    player_sprite_cache = TileCache(TILE_SIZE, 24)

    clock = pygame.time.Clock()
    level = Level(map_cache, TILE_SIZE, TILE_SIZE, RESOURCES_DIR + 'midgaard/town.map')
    background, foreground, sprites = level.render()
    player_sprite = MobSprite((25, 10), player_sprite_cache['fireas.png'], True)
    sprites.append(player_sprite)
    offset_x, offset_y = get_offset()
    screen.blit(background, (offset_x, offset_y))
    game_over = False
    while not game_over:
        # redraw screen
        screen.fill((0, 0, 0))
        screen.blit(background, (offset_x, offset_y))
        for sprite in sprites:
            result = sprite.update(level)
            if isinstance(sprite, MobSprite) and sprite.is_player_sprite and result is not None:
                offset_x = offset_x + result[0]
                offset_y = offset_y + result[1]
            screen.blit(
                sprite.image,
                ((sprite.pos[0] * TILE_SIZE) + offset_x - sprite.to_amount[0],
                 (sprite.pos[1] * TILE_SIZE) - sprite.to_amount[1] + sprite.offset_y() + offset_y))
        screen.blit(player_sprite.image, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(foreground, (offset_x, offset_y))

        pygame.display.update()
        clock.tick(TICKS)

        # pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # did player step on a warp?
        warp = level.get_warp(int(player_sprite.pos[0]), int(player_sprite.pos[1]))
        if not player_sprite.is_moving() and warp:
            player_sprite.pos = level.get_to(int(player_sprite.pos[0]), int(player_sprite.pos[1]))
            level = Level(map_cache, TILE_SIZE, TILE_SIZE, RESOURCES_DIR + warp)
            background, foreground, sprites = level.render()
            sprites.append(player_sprite)
            offset_x, offset_y = get_offset()

        # evaluate movement
        keys = pygame.key.get_pressed()
        direction = player_sprite.direction
        if keys[pygame.K_LEFT] and can_move((player_sprite.pos[0] - 1, player_sprite.pos[1])):
            move_player((-TILE_SIZE, 0), (player_sprite.pos[0] - 1, player_sprite.pos[1]), LEFT)
        if keys[pygame.K_RIGHT] and can_move((player_sprite.pos[0] + 1, player_sprite.pos[1])):
            move_player((TILE_SIZE, 0), (player_sprite.pos[0] + 1, player_sprite.pos[1]), RIGHT)
        if keys[pygame.K_UP] and can_move((player_sprite.pos[0], player_sprite.pos[1] - 1)):
            move_player((0, -TILE_SIZE), (player_sprite.pos[0], player_sprite.pos[1] - 1), UP)
        if keys[pygame.K_DOWN] and can_move((player_sprite.pos[0], player_sprite.pos[1] + 1)):
            move_player((0, TILE_SIZE), (player_sprite.pos[0], player_sprite.pos[1] + 1), DOWN)

        # change animation when direction changes
        if direction != player_sprite.direction:
            next(player_sprite.animation)
