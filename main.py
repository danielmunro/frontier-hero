from frontier_hero.constants import SCREEN_WIDTH, TILE_SIZE, SCREEN_HEIGHT, RESOURCES_DIR, TICKS, Y_OFFSET, \
    MOB_Y_TILE_SIZE
from frontier_hero.level import Level
import pygame

from frontier_hero.player import Player
from frontier_hero.sprite import MobSprite, LEFT, RIGHT, UP, DOWN, ChestSprite
from frontier_hero.tile_cache import TileCache


def evaluate_direction_key(new_pos, move_amount, direction_moving):
    if can_move(new_pos):
        move_player(move_amount, new_pos, direction_moving)
    elif not player_sprite.is_moving():
        player_sprite.direction = direction_moving


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
           (SCREEN_HEIGHT / 2) - Y_OFFSET - (player_sprite.pos[1] * TILE_SIZE)


if __name__ == "__main__":
    pygame.init()
    font = pygame.font.Font('freesansbold.ttf', 24)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    tile_cache = TileCache(TILE_SIZE, TILE_SIZE)
    player_sprite_cache = TileCache(TILE_SIZE, MOB_Y_TILE_SIZE)
    clock = pygame.time.Clock()
    level = Level(tile_cache, TILE_SIZE, TILE_SIZE, RESOURCES_DIR + 'midgaard/town.map')
    background, foreground, sprites = level.render()
    player_sprite = MobSprite((19, 8), player_sprite_cache['fireas.png'], True)
    player = Player(player_sprite)
    sprites.append(player_sprite)
    offset_x, offset_y = get_offset()
    screen.blit(background, (offset_x, offset_y))
    dialog = None
    game_over = False
    while not game_over:
        # redraw screen
        screen.fill((0, 0, 0))
        screen.blit(background, (offset_x, offset_y))
        offset_change = (0, 0)
        for sprite in sprites:
            result = sprite.update(level, sprites)
            screen.blit(
                sprite.image,
                ((sprite.pos[0] * TILE_SIZE) + offset_x - sprite.to_amount[0],
                 (sprite.pos[1] * TILE_SIZE) - sprite.to_amount[1] + sprite.offset_y() + offset_y))
            if isinstance(sprite, MobSprite) and sprite.is_player_sprite and result is not None:
                offset_change = result
        screen.blit(player_sprite.image, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(foreground, (offset_x, offset_y))

        if offset_change != (0, 0):
            offset_x = offset_x + offset_change[0]
            offset_y = offset_y + offset_change[1]

        if dialog:
            y = ((SCREEN_HEIGHT / 3) * 2) + 1
            rect = pygame.Rect(0, y, SCREEN_WIDTH, SCREEN_HEIGHT / 3)
            pygame.draw.rect(
                screen,
                (0, 0, 255),
                rect,
            )
            text = font.render(dialog, True, (255, 255, 255), (0, 0, 255))
            rect = text.get_rect()
            rect.topleft = (0, y)
            screen.blit(text, rect)

        pygame.display.update()
        clock.tick(TICKS)

        # pygame events
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if dialog:
                    dialog = None
                    for sprite in sprites:
                        if isinstance(sprite, MobSprite):
                            sprite.engaged = False
                else:
                    focus = player.get_focus_point()
                    mob = next((s for s in sprites if isinstance(s, MobSprite) and s.pos == focus), None)
                    if mob:
                        dialog = "hello world"
                        mob.engaged = True
                    chest = next((s for s in sprites if isinstance(s, ChestSprite) and s.pos == focus), None)
                    if chest and chest.closed is True:
                        chest.closed = False
            if event.type == pygame.QUIT:
                game_over = True

        # did player step on a warp?
        warp = level.get_warp(int(player_sprite.pos[0]), int(player_sprite.pos[1]))
        if not player_sprite.is_moving() and warp:
            player_sprite.pos = level.get_to(int(player_sprite.pos[0]), int(player_sprite.pos[1]))
            level = Level(tile_cache, TILE_SIZE, TILE_SIZE, RESOURCES_DIR + warp)
            background, foreground, sprites = level.render()
            sprites.append(player_sprite)
            offset_x, offset_y = get_offset()

        # evaluate movement
        keys = pygame.key.get_pressed()
        direction = player_sprite.direction
        if keys[pygame.K_LEFT]:
            evaluate_direction_key(
                (player_sprite.pos[0] - 1, player_sprite.pos[1]),
                (-TILE_SIZE, 0),
                LEFT,
            )
        elif keys[pygame.K_RIGHT]:
            evaluate_direction_key(
                (player_sprite.pos[0] + 1, player_sprite.pos[1]),
                (TILE_SIZE, 0),
                RIGHT,
            )
        elif keys[pygame.K_UP]:
            evaluate_direction_key(
                (player_sprite.pos[0], player_sprite.pos[1] - 1),
                (0, -TILE_SIZE),
                UP,
            )
        elif keys[pygame.K_DOWN]:
            evaluate_direction_key(
                (player_sprite.pos[0], player_sprite.pos[1] + 1),
                (0, TILE_SIZE),
                DOWN,
            )

        if direction != player_sprite.direction:
            next(player_sprite.animation)
