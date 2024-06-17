from os import path

import pygame
from mlgame.view.view_model import create_asset_init_data, create_image_view_data

from .env import IMAGE_DIR


class Unbreakable_Wall(pygame.sprite.Sprite):
    def __init__(self, construction, **kwargs):
        super().__init__()
        self.id = construction["_id"]
        self.no = 0
        self.rect = pygame.Rect(construction["_init_pos"], construction["_init_size"])
        self.angle = 0
        self.is_alive = True
        self.lives = -1

    def update(self, *args, **kwargs) -> None:
        pass

    def collide_with_bullets(self):
        pass

    def get_data_from_obj_to_game(self):
        info = {"id": f"wall_unbreak", "x": self.rect.x, "y": self.rect.y, "lives": self.lives}
        return info

    def get_obj_progress_data(self):
        return create_image_view_data(f"wall_unbreak", self.rect.x, self.rect.y
                                      , self.rect.width, self.rect.height, self.angle)

    def get_obj_init_data(self):
        image_init_data = []
        image_init_data.append(create_asset_init_data(f"wall_unbreak", self.rect.width, self.rect.height,
                                                        path.join(IMAGE_DIR, f"wall_unbreak.png"),
                                                        f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/wall_unbreak.png"))
        return image_init_data
