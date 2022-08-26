import random
from os import path

from mlgame.view.view_model import create_asset_init_data

from .GameFramework.Station import Station
from .env import IMAGE_DIR, WINDOW_HEIGHT, WINDOW_WIDTH


class TankStation(Station):
    def __init__(self, construction, **kwargs):
        super().__init__(construction, **kwargs)
        if self.rect.x >= WINDOW_WIDTH // 2 and self.rect.y < (WINDOW_HEIGHT - 100) // 2:
            self.quadrant = 1
        elif self.rect.x < WINDOW_WIDTH // 2 and self.rect.y < (WINDOW_HEIGHT - 100) // 2:
            self.quadrant = 2
        elif self.rect.x < WINDOW_WIDTH // 2 and self.rect.y >= (WINDOW_HEIGHT - 100) // 2:
            self.quadrant = 3
        else:
            self.quadrant = 4

    def get_quadrant(self) -> int:
        return self.quadrant

    def set_quadrant(self, quadrant: int) -> None:
        self.quadrant = quadrant

    def get_info(self):
        if 5 == self._id:
            info = {"id": "oil", "x": self.rect.x, "y": self.rect.y, "power": self.power}
        else:
            info = {"id": "bullets", "x": self.rect.x, "y": self.rect.y, "power": self.power}
        return info

    def get_image_data(self):
        if 5 == self._id:
            image_data = {"id": f"oil", "x": self.rect.x, "y": self.rect.y, "width": self.rect.width,
                          "height": self.rect.height, "angle": 0}
        else:
            image_data = {"id": f"bullets", "x": self.rect.x, "y": self.rect.y, "width": self.rect.width,
                          "height": self.rect.height, "angle": 0}
        return image_data

    def get_image_init_data(self):
        bullets_id = "bullets"
        oil_id = "oil"
        bullets_url = f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/bullets.png"
        oil_url = f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/oil.png"
        image_init_data = [create_asset_init_data(bullets_id, self.rect.width, self.rect.height,
                                                  path.join(IMAGE_DIR, f"{bullets_id}.png"), bullets_url)
                           , create_asset_init_data(oil_id, self.rect.width, self.rect.height,
                                                    path.join(IMAGE_DIR, f"{oil_id}.png"), oil_url)]
        return image_init_data

    def change_pos(self, empty_pos: list):
        self.rect.topleft = random.choice(empty_pos)
        self.hit_rect.center = self.rect.center
