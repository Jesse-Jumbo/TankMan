from os import path

import pygame
from mlgame.view.view_model import create_asset_init_data, create_image_view_data

from .env import IMAGE_DIR, WALL_LIVE


class Wall(pygame.sprite.Sprite):
    def __init__(self, construction, **kwargs):
        super().__init__()
        self.id = construction["_id"]
        self.no = 0
        self.rect = pygame.Rect(construction["_init_pos"], construction["_init_size"])
        self.angle = 0
        self.is_alive = True
        self.lives = WALL_LIVE

    def update(self, *args, **kwargs) -> None:
        if self.lives <= 0:
            self.kill()

    def collide_with_bullets(self):
        if self.lives > 0:
            self.lives -= 1

    def get_data_from_obj_to_game(self):
        info = {"id": f"wall_{self.lives}", "x": self.rect.x, "y": self.rect.y, "lives": self.lives}
        return info

    def get_obj_progress_data(self):
        return create_image_view_data(f"wall_{self.lives}", self.rect.x, self.rect.y
                                      , self.rect.width, self.rect.height, self.angle)

    def get_obj_init_data(self):
        image_init_data = []
        for i in range(1, self.lives+1):
            image_init_data.append(create_asset_init_data(f"wall_{i}", self.rect.width, self.rect.height,
                                                          path.join(IMAGE_DIR, f"wall_{min(i,3)}.png"),
                                                          f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/wall_{min(i,3)}.png"))
        return image_init_data
