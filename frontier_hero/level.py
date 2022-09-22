from configparser import ConfigParser
from pygame import Surface


class Level:
    def __init__(self, cache, tile_width, tile_height, filename):
        self.cache = cache
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.key = {}
        parser = ConfigParser()
        parser.read(filename)
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        self.width = len(self.map[0])
        self.height = len(self.map)

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

    def get_bool(self, x, y, name):
        """Tell if the specified flag is set for position on the map."""

        value = self.get_tile(x, y).get(name)
        return value in (True, 1, 'true', 'yes', 'True', 'Yes', '1', 'on', 'On')

    def is_blocking(self, x, y):
        """Is this place blocking movement?"""

        if not 0 <= x < self.width or not 0 <= y < self.height:
            return True
        return self.get_bool(x, y, 'block')

    def render(self):
        tiles = self.cache[self.tileset]
        image = Surface((self.width * self.tile_width, self.height * self.tile_height))
        self._draw(tiles, image, self.map)
        return image

    def _draw(self, tiles, image, layer):
        for map_y, line in enumerate(layer):
            for map_x, c in enumerate(line):
                tile = self.key[c]['tile'].split(',')
                tile = int(tile[0]), int(tile[1])
                tile_image = tiles[tile[0]][tile[1]]
                image.blit(tile_image,
                           (map_x * self.tile_width, map_y * self.tile_height))
