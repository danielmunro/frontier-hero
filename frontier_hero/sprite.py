import pygame

SPRITE_WIDTH = 32
SPRITE_HEIGHT = 48
DOWN = 0
LEFT = 1
RIGHT = 2
UP = 3


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), frames=None):
        super(Sprite, self).__init__()
        self.frames = frames
        self.animation = self.stand_animation()
        self.direction = DOWN
        self.image = frames[self.direction][0]
        self.rect = self.image.get_rect()
        self.pos = pos

    def _get_pos(self):
        """Check the current position of the sprite on the map."""

        return self.rect.midleft[0] / 16, self.rect.midleft[1] / 16

    def _set_pos(self, pos):
        """Set the position and depth of the sprite on the map."""
        self.rect.midleft = pos[0] * 16, pos[1] * 16
        self.depth = self.rect.midleft[1]

    pos = property(_get_pos, _set_pos)

    def move(self, dx, dy):
        """Change the position of the sprite on screen."""

        self.rect.move_ip(dx, dy)
        self.depth = self.rect.midleft[1]

    def stand_animation(self):
        while True:
            for frame in self.frames:
                self.image = frame[self.direction]
                yield None
                yield None

    def update(self, *args):
        next(self.animation)
