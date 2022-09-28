from frontier_hero.sprite import LEFT, RIGHT, UP, DOWN


class Player:
    def __init__(self, sprite):
        self.state = {}
        self.chests = {}
        self.items = []
        self.sprite = sprite

    def get_focus_point(self):
        if self.sprite.direction == LEFT:
            return self.sprite.pos[0] - 1, self.sprite.pos[1]
        elif self.sprite.direction == RIGHT:
            return self.sprite.pos[0] + 1, self.sprite.pos[1]
        elif self.sprite.direction == UP:
            return self.sprite.pos[0], self.sprite.pos[1] - 1
        elif self.sprite.direction == DOWN:
            return self.sprite.pos[0], self.sprite.pos[1] + 1

    def is_chest_closed(self, level, pos):
        if level not in self.chests:
            self.chests[level] = {}

        return pos not in self.chests[level]

    def open_chest(self, level, pos):
        self.chests[level][pos] = True
