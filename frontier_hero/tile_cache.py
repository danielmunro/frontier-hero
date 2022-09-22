import math

import pygame


class TileCache:
    """Load the tilesets lazily into global cache"""

    def __init__(self,  width=16, height=None):
        self.width = width
        self.height = height or width
        self.cache = {}

    def __getitem__(self, filename):
        """Return a table of tiles, load it from disk if needed."""

        key = (filename, self.width, self.height)
        try:
            return self.cache[key]
        except KeyError:
            tile_table = self._load_tile_table(filename, self.width,
                                               self.height)
            self.cache[key] = tile_table
            return tile_table

    @staticmethod
    def _load_tile_table(filename, width, height):
        """Load an image and split it into tiles."""

        image = pygame.image.load("resources/" + filename).convert()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_x in range(0, math.floor(image_width / width)):
            line = []
            tile_table.append(line)
            for tile_y in range(0, math.floor(image_height / height)):
                rect = (tile_x*width, tile_y*height, width, height)
                line.append(image.subsurface(rect))
        return tile_table
