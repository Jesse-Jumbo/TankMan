from os import path

import pygame
from mlgame.view.view_model import create_asset_init_data, create_image_view_data

from .env import IMAGE_DIR, WINDOW_HEIGHT, WINDOW_WIDTH


class Station(pygame.sprite.Sprite):
    def __init__(self, construction, **kwargs):
        super().__init__()
        self.id = construction["_id"]
        self.rect = pygame.Rect(construction["_init_pos"], construction["_init_size"])
        self.power = kwargs["capacity"]
        self.angle = 0
        if self.rect.x >= WINDOW_WIDTH // 2 and self.rect.y < (WINDOW_HEIGHT - 100) // 2:
            self.quadrant = 1
        elif self.rect.x < WINDOW_WIDTH // 2 and self.rect.y < (WINDOW_HEIGHT - 100) // 2:
            self.quadrant = 2
        elif self.rect.x < WINDOW_WIDTH // 2 and self.rect.y >= (WINDOW_HEIGHT - 100) // 2:
            self.quadrant = 3
        else:
            self.quadrant = 4

        self.spawn_cd = kwargs["spawn_cd"]
        self.cooldown = 0
        self.is_alive = True

    def update(self):
        if not self.is_alive:
            self.cooldown -= 1
            if self.cooldown <= 0:
                self.is_alive = True

    def collect(self):
        self.is_alive = False
        self.cooldown = self.spawn_cd

    def get_data_from_obj_to_game(self):
        if 5 == self.id:
            info = {"id": "oil", "x": self.rect.x, "y": self.rect.y, "power": self.power if self.is_alive else 0}
        else:
            info = {"id": "bullets", "x": self.rect.x, "y": self.rect.y, "power": self.power if self.is_alive else 0}
        return info

    def get_obj_progress_data(self):
        if not self.is_alive:
            return []
        if 5 == self.id:
            return create_image_view_data(f"oil", self.rect.x, self.rect.y
                                          , self.rect.width, self.rect.height, self.angle)
        else:
            return create_image_view_data(f"bullets", self.rect.x, self.rect.y
                                          , self.rect.width, self.rect.height, self.angle)

    def get_obj_init_data(self):
        bullets_id = "bullets"
        oil_id = "oil"
        bullets_url = f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/{bullets_id}.svg"
        oil_url = f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/{oil_id}.svg"
        image_init_data = [create_asset_init_data(bullets_id, self.rect.width, self.rect.height,
                                                  path.join(IMAGE_DIR, f"{bullets_id}.png"), bullets_url)
                           , create_asset_init_data(oil_id, self.rect.width, self.rect.height,
                                                    path.join(IMAGE_DIR, f"{oil_id}.png"), oil_url)]
        return image_init_data
