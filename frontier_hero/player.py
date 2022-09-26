from frontier_hero.sprite import LEFT, RIGHT, UP, DOWN


class Player:
    def __init__(self, sprite):
        self.state = {}
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
