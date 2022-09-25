SPRITE_WIDTH = 32
SPRITE_HEIGHT = 48
DOWN = 0
LEFT = 1
RIGHT = 2
UP = 3
TICKS_PER_ANIM = 4


class Sprite:
    def __init__(self, pos=(0, 0), frames=None):
        self.frames = frames
        self.animation = self.start_animation()
        self.image = frames[0]
        self.rect = self.image.get_rect()
        self.pos = pos
        self.ticks = 0

    def update(self):
        self.ticks = self.ticks + 1
        if self.ticks > TICKS_PER_ANIM:
            next(self.animation)
            self.ticks = 0

    def start_animation(self):
        while True:
            for frame in self.frames:
                self.image = frame
                yield


class MobSprite:
    def __init__(self, pos=(0, 0), frames=None):
        self.frames = frames
        self.animation = self.start_animation()
        self.direction = DOWN
        self.image = frames[self.direction][0]
        self.rect = self.image.get_rect()
        self.to_amount = (0.0, 0.0)
        self.pos = pos
        self.ticks = 0

    def update(self):
        self.ticks = self.ticks + 1
        if self.ticks > TICKS_PER_ANIM:
            next(self.animation)
            self.ticks = 0

    def is_moving(self):
        return self.to_amount != (0, 0)

    def start_animation(self):
        while True:
            for frame in self.frames:
                self.image = frame[self.direction]
                yield
