from .env import WALL_IMG_PATH_LIST
from .Prop import Prop


class Obstacle(Prop):
    def __init__(self, no: int, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self._no = no
        self.lives = 5
        self.img_path_list = WALL_IMG_PATH_LIST

    def update(self, *args, **kwargs) -> None:
        if self.lives <= 0:
            self.kill()

    def collide_with_bullets(self):
        if self.lives > 0:
            self.lives -= 1

    def get_pos_xy(self):
        return self.rect.x, self.rect.y

    def get_image_data(self):
        if self.lives > 0:
            super().get_image_data()
            self.image_data["_id"] = f"wall_{self.lives}"
            return self.image_data

    def get_image_init_data(self):
        super().get_image_init_data()
        c = 0
        for img_path in self.img_path_list:
            self.image_init_data["path"] = img_path
            self.image_init_data["_id"] = f"wall_{self._no}_{self.lives - c}"
            c += 1
        return self.image_init_data
