from .env import WALL_IMG_PATH_LIST
from .Prop import Prop


class Obstacle(Prop):
    def __init__(self, no: int, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self._no = no
        self.lives = 5

    def update(self, *args, **kwargs) -> None:
        if self.lives <= 0:
            self.kill()

    def collide_with_bullets(self):
        if self.lives > 0:
            self.lives -= 1

    def get_pos_xy(self):
        return self.rect.x, self.rect.y
