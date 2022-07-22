from os import path

from .env import IMAGE_DIR
from mlgame.view.view_model import create_asset_init_data
from .GameFramework.Props import Props


class TankWall(Props):
    def __init__(self, construction, **kwargs):
        super().__init__(construction, **kwargs)
        self.lives = 5

    def update(self, *args, **kwargs) -> None:
        if self.lives <= 0:
            self.kill()

    def collide_with_bullets(self):
        if self.lives > 0:
            self.lives -= 1

    def get_xy_pos(self):
        return self.rect.x, self.rect.y

    def get_info(self):
        info = {"id": f"wall_{self.lives}", "x": self.rect.x, "y": self.rect.y, "lives": self.lives}
        return info

    def get_image_data(self):
        if self.lives > 0:
            image_data = {"id": f"wall_{self.lives}", "x": self.rect.x, "y": self.rect.y,
                          "width": self.rect.width, "height": self.rect.height, "angle": 0}
            return image_data

    def get_image_init_data(self):
        img_data = {}
        for i in range(1, 6):
            img_data[f"wall_{i}"] = f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/wall_{i}.png"
        image_init_data = []
        for id, url in img_data.items():
            image_init_data.append(create_asset_init_data(id, self.rect.width, self.rect.height,
                                                          path.join(IMAGE_DIR, f"{id}.png"), url))
        return image_init_data

