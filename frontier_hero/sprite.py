import pygame

SPRITE_WIDTH = 32
SPRITE_HEIGHT = 48


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), frames=None):
        super(Sprite, self).__init__()
        self.frames = frames
        self.animation = self.stand_animation()
        self.image = frames[0][0]
        self.rect = self.image.get_rect()
        self.pos = pos

    def _get_pos(self):
        """Check the current position of the sprite on the map."""

        return (self.rect.midbottom[0] / SPRITE_WIDTH) + (SPRITE_WIDTH / 2), self.rect.midbottom[1] / SPRITE_HEIGHT

    def _set_pos(self, pos):
        """Set the position and depth of the sprite on the map."""
        self.rect.midbottom = (pos[0] * SPRITE_WIDTH) - (SPRITE_WIDTH / 2), pos[1] * SPRITE_HEIGHT
        self.depth = self.rect.midbottom[1]

    pos = property(_get_pos, _set_pos)

    def move(self, dx, dy):
        """Change the position of the sprite on screen."""

        self.rect.move_ip(dx, dy)
        self.depth = self.rect.midbottom[1]

    def stand_animation(self):
        while True:
            for frame in self.frames:
                self.image = frame[0]
                yield None
                yield None

    def update(self, *args):
        next(self.animation)
