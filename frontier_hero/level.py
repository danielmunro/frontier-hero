from configparser import ConfigParser
from pygame import Surface

from frontier_hero.tile_cache import TileCache


class Level:
    def __init__(self, cache: TileCache, tile_width, tile_height, filename):
        self.cache = cache
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.key = {}
        parser = ConfigParser()
        parser.read(filename)
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")
        self.objects = parser.get("level", "objects").split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        self.width = len(self.map[0])
        self.height = len(self.map)
        self.big_sprites = {}

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
        self._draw(tiles, background, foreground, self.map)
        self._draw(tiles, background, foreground, self.objects)
        return background, foreground

    def _draw(self, tiles, background, foreground, layer):
        for map_y, line in enumerate(layer):
            for map_x, c in enumerate(line):
                image = None
                if 'tile' in self.key[c]:
                    tile = self.key[c]['tile'].split(',')
                    tile = int(tile[0]), int(tile[1])
                    image = tiles[tile[0]][tile[1]]
                elif 'tile_from' in self.key[c] and 'tile_to' in self.key[c]:
                    name = self.key[c]['name']
                    if name in self.big_sprites:
                        image = self.big_sprites[name]
                    else:
                        tile_from = self.key[c]['tile_from'].split(',')
                        tile_from = int(tile_from[0]), int(tile_from[1])
                        tile_to = self.key[c]['tile_to'].split(',')
                        tile_to = int(tile_to[0]), int(tile_to[1])
                        width = 1 + tile_to[0] - tile_from[0]
                        height = 1 + tile_to[1] - tile_from[1]
                        image = Surface((width * self.tile_width, height * self.tile_height)).convert_alpha()
                        for y in range(height):
                            for x in range(width):
                                image.blit(tiles[tile_from[0] + x][tile_from[1] + y], (x * self.tile_width, y * self.tile_height))
                        self.big_sprites[name] = image
                
                if image:
                    self._add_to_layer(image, foreground, background, map_x, map_y)

    def _add_to_layer(self, image, foreground, background, x, y):
        in_foreground = self.get_object(x, y).get('foreground')
        if in_foreground:
            foreground.blit(image, (x * self.tile_width, y * self.tile_height))
        else:
            background.blit(image, (x * self.tile_width, y * self.tile_height))
