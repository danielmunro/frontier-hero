from random import choice

DOWN = 0
LEFT = 1
RIGHT = 2
UP = 3
TICKS_PER_ANIM = 4
TICKS_PER_MOVE = 30


class Sprite:
    def __init__(self, pos=(0, 0), frames=None):
        self.frames = frames
        self.animation = self.start_animation()
        self.image = next(self.animation)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.ticks = 0
        self.to_amount = (0, 0)

    def update(self, level):
        self.ticks = self.ticks + 1
        if self.ticks > TICKS_PER_ANIM:
            next(self.animation)
            self.ticks = 0

    def start_animation(self):
        while True:
            for frame in self.frames:
                self.image = frame
                yield self.image

    def offset_y(self):
        return 0


class MobSprite(Sprite):
    def __init__(self, pos=(0, 0), frames=None, is_player_sprite=False):
        self.direction = DOWN
        self.is_player_sprite = is_player_sprite
        super().__init__(pos, frames)

    def update(self, level):
        self.ticks = self.ticks + 1
        if self.to_amount == (0, 0):
            if not self.is_player_sprite and self.ticks > TICKS_PER_MOVE:
                new_pos = choice(
                    list(
                        filter(lambda x: not level.is_blocking(x[0], x[1]) and not level.is_object_blocking(x[0], x[1]), [
                            (self.pos[0] - 1, self.pos[1]),
                            (self.pos[0] + 1, self.pos[1]),
                            (self.pos[0], self.pos[1] - 1),
                            (self.pos[0], self.pos[1] + 1),
                        ])))
                self.to_amount = (-(self.pos[0] - new_pos[0]) * 16, -(self.pos[1] - new_pos[1]) * 16)
                if self.to_amount == (-16, 0):
                    self.direction = LEFT
                elif self.to_amount == (16, 0):
                    self.direction = RIGHT
                elif self.to_amount == (0, -16):
                    self.direction = UP
                elif self.to_amount == (0, 16):
                    self.direction = DOWN
                self.pos = new_pos
        else:
            dx = 0
            dy = 0
            if self.to_amount[0] > 0:
                dx = -1
            elif self.to_amount[0] < 0:
                dx = 1
            elif self.to_amount[1] > 0:
                dy = -1
            elif self.to_amount[1] < 0:
                dy = 1
            self.to_amount = (self.to_amount[0] + dx, self.to_amount[1] + dy)
            if self.ticks > TICKS_PER_ANIM:
                next(self.animation)
                self.ticks = 0
            return dx, dy

    def is_moving(self):
        return self.to_amount != (0, 0)

    def start_animation(self):
        while True:
            for frame in self.frames:
                self.image = frame[self.direction]
                yield self.image

    def offset_y(self):
        return -8
