import sys
from configparser import ConfigParser
from pygame import Surface

from frontier_hero.constants import TILE_SIZE, MOB_Y_TILE_SIZE
from frontier_hero.sprite import MobSprite, Sprite, ChestSprite
from frontier_hero.tile_cache import TileCache


class Level:
    def __init__(self, cache: TileCache, tile_width, tile_height, filename):
        self.cache = cache
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.key = {}
        self.filename = filename
        parser = ConfigParser()
        parser.read(filename)
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")
        self.objects = parser.get("level", "objects").split("\n")
        self.nice_edge = {}
        self.line = {}
        for section in parser.sections():
            desc = dict(parser.items(section))
            self.key[section] = desc
            if "nice_edge" in desc:
                self.nice_edge[desc["nice_edge"]] = section
            elif "line" in desc:
                self.line[section] = True
        self.width = len(self.map[0])
        self.height = len(self.map)
        self.big_images = {}

    def get_tile(self, x, y):
        """Tell what's at the specified position of the map."""

        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def get_object(self, x, y):
        """Tell what's at the specified position of the map."""

        try:
            char = self.objects[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def get_bool(self, x, y, name):
        """Tell if the specified flag is set for position on the map."""

        value = self.get_tile(x, y).get(name)
        return value in (True, 1, 'true', 'yes', 'True', 'Yes', '1', 'on', 'On')

    def get_warp(self, x, y):
        return self.get_object(x, y).get('warp')

    def get_to(self, x, y):
        to = self.get_object(x, y).get('to').split(',')
        return int(to[0]), int(to[1])

    def is_object_blocking(self, x, y):
        return self.get_object(x, y).get('block')

    def is_blocking(self, x, y):
        """Is this place blocking movement?"""

        if not 0 <= x < self.width or not 0 <= y < self.height:
            return True
        return self.get_bool(x, y, 'block') or self.is_object_blocking(x, y)

    def render(self):
        tiles = self.cache[self.tileset]
        background = Surface((self.width * self.tile_width, self.height * self.tile_height)).convert_alpha()
        foreground = Surface((self.width * self.tile_width, self.height * self.tile_height)).convert_alpha()
        sprites = []
        self._draw(tiles, background, foreground, sprites, self.map)
        self._do_nice_edges(tiles, background, foreground)
        for map_y, line in enumerate(self.objects):
            for map_x, c in enumerate(line):
                if c in self.line:
                    to = self.key[c]
                    try:
                        image = None
                        if self.objects[map_y + 1][map_x] == c and self.objects[map_y][map_x + 1] == c:
                            image = self.get_image(to['tl'], tiles)
                        elif self.objects[map_y - 1][map_x] == c and self.objects[map_y][map_x + 1] == c:
                            image = self.get_image(to['bl'], tiles)
                        elif self.objects[map_y][map_x - 1] == c and self.objects[map_y - 1][map_x] == c:
                            image = self.get_image(to['br'], tiles)
                        elif self.objects[map_y + 1][map_x] == c and self.objects[map_y][map_x - 1] == c:
                            image = self.get_image(to['tr'], tiles)
                        elif self.objects[map_y + 1][map_x] == c and self.objects[map_y - 1][map_x] != c:
                            image = self.get_image(to['t'], tiles)
                        elif self.objects[map_y - 1][map_x] == c and self.objects[map_y + 1][map_x] != c:
                            image = self.get_image(to['b'], tiles)
                        elif self.objects[map_y][map_x + 1] == c and self.objects[map_y][map_x - 1] != c:
                            image = self.get_image(to['r'], tiles)
                        elif self.objects[map_y][map_x - 1] == c and self.objects[map_y][map_x + 1] != c:
                            image = self.get_image(to['l'], tiles)
                        elif self.objects[map_y - 1][map_x] == c or self.objects[map_y + 1][map_x] == c:
                            image = self.get_image(to['v'], tiles)
                        elif self.objects[map_y][map_x - 1] == c or self.objects[map_y][map_x + 1] == c:
                            image = self.get_image(to['h'], tiles)
                        if image:
                            self._add_to_layer(image, foreground, background, map_x, map_y)
                    except IndexError:
                        pass
        self._draw(tiles, background, foreground, sprites, self.objects)
        return background, foreground, sprites

    @staticmethod
    def get_image(to, tiles):
        t = to.split(',')
        t = int(t[0]), int(t[1])
        return tiles[t[0]][t[1]]

    def _do_nice_edges(self, tiles, background, foreground):
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                if c in self.nice_edge:
                    to = self.key[self.nice_edge[c]]
                    try:
                        image = None
                        if self.map[map_y - 1][map_x] == self.nice_edge[c] and self.map[map_y - 1][map_x + 1] == self.nice_edge[c] and self.map[map_y][map_x + 1] == self.nice_edge[c]:
                            image = self.get_image(to['tlcorner'], tiles)
                        elif self.map[map_y - 1][map_x] == self.nice_edge[c] and self.map[map_y - 1][map_x - 1] == self.nice_edge[c] and self.map[map_y][map_x - 1] == self.nice_edge[c]:
                            image = self.get_image(to['trcorner'], tiles)
                        elif self.map[map_y + 1][map_x] == self.nice_edge[c] and self.map[map_y + 1][map_x + 1] == self.nice_edge[c] and self.map[map_y][map_x + 1] == self.nice_edge[c]:
                            image = self.get_image(to['blcorner'], tiles)
                        elif self.map[map_y + 1][map_x] == self.nice_edge[c] and self.map[map_y + 1][map_x - 1] == self.nice_edge[c] and self.map[map_y][map_x - 1] == self.nice_edge[c]:
                            image = self.get_image(to['brcorner'], tiles)
                        elif self.map[map_y + 1][map_x - 1] == self.nice_edge[c] and self.map[map_y + 1][map_x] == c and self.map[map_y][map_x - 1] == c:
                            image = self.get_image(to['tr'], tiles)
                        elif self.map[map_y - 1][map_x + 1] == self.nice_edge[c] and self.map[map_y - 1][map_x] == c and self.map[map_y][map_x + 1] == c:
                            image = self.get_image(to['bl'], tiles)
                        elif self.map[map_y + 1][map_x + 1] == self.nice_edge[c] and self.map[map_y + 1][map_x] == c and self.map[map_y][map_x + 1] == c:
                            image = self.get_image(to['tl'], tiles)
                        elif self.map[map_y - 1][map_x - 1] == self.nice_edge[c] and self.map[map_y - 1][map_x] == c and self.map[map_y][map_x - 1] == c:
                            image = self.get_image(to['br'], tiles)
                        elif self.map[map_y + 1][map_x] == self.nice_edge[c]:
                            image = self.get_image(to['t'], tiles)
                        elif self.map[map_y - 1][map_x] == self.nice_edge[c]:
                            image = self.get_image(to['b'], tiles)
                        elif self.map[map_y][map_x - 1] == self.nice_edge[c]:
                            image = self.get_image(to['r'], tiles)
                        elif self.map[map_y][map_x + 1] == self.nice_edge[c]:
                            image = self.get_image(to['l'], tiles)
                        if image:
                            self._add_to_layer(image, foreground, background, map_x, map_y)
                    except IndexError:
                        pass

    def _draw(self, tiles, background, foreground, sprites, layer):
        for map_y, line in enumerate(layer):
            for map_x, c in enumerate(line):
                image = None
                if 'tile' in self.key[c]:
                    tile = self.key[c]['tile'].split(',')
                    tile = int(tile[0]), int(tile[1])
                    image = tiles[tile[0]][tile[1]]
                    self._add_to_layer(image, foreground, background, map_x, map_y)
                elif 'tile_from' in self.key[c] and 'tile_to' in self.key[c]:
                    name = self.key[c]['name']
                    if name in self.big_images:
                        image = self.big_images[name]
                    else:
                        tile_from = self.key[c]['tile_from'].split(',')
                        tile_from = int(tile_from[0]), int(tile_from[1])
                        tile_to = self.key[c]['tile_to'].split(',')
                        tile_to = int(tile_to[0]), int(tile_to[1])
                        try:
                            frame_count = int(self.key[c]['frames'])
                        except KeyError:
                            frame_count = 1
                        width = int((tile_to[0] - tile_from[0]) / frame_count)
                        height = tile_to[1] - tile_from[1]
                        frames = []
                        for frame in range(frame_count):
                            image = Surface((width * self.tile_width, height * self.tile_height)).convert_alpha()
                            for y in range(height):
                                for x in range(width):
                                    image.blit(tiles[tile_from[0] + x + (frame * width)][tile_from[1] + y],
                                               (x * self.tile_width, y * self.tile_height))
                            self.big_images[name] = image
                            if frame_count > 1:
                                frames.append(image)
                        if frame_count > 1:
                            sprites.append(Sprite((map_x, map_y), frames))
                    self._add_to_layer(image, foreground, background, map_x, map_y)
                elif 'mob' in self.key[c]:
                    tileset = self.key[c]['tileset']
                    sprites.append(MobSprite(pos=(map_x, map_y), frames=TileCache(TILE_SIZE, MOB_Y_TILE_SIZE)[tileset]))
                elif 'chest' in self.key[c]:
                    objects = self.cache['objects.png']
                    sprites.append(ChestSprite(pos=(map_x, map_y), frames=[objects[0][0], objects[1][0]], item=int(self.key[c]['item'])))

    def _add_to_layer(self, image, foreground, background, x, y):
        in_foreground = self.get_object(x, y).get('foreground')
        if in_foreground:
            foreground.blit(image, (x * self.tile_width, y * self.tile_height))
        else:
            background.blit(image, (x * self.tile_width, y * self.tile_height))
