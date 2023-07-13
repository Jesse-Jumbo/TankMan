from os import path

import pygame
from mlgame.view.view_model import (create_asset_init_data,
                                    create_image_view_data,
                                    create_rect_view_data)

from .env import IMAGE_DIR


class Gun(pygame.sprite.Sprite):
    def __init__(self, id, pos, size, **kwargs):
        super().__init__()
        self.id = id
        self.rect = pygame.Rect(pos, size)
        self.origin_size = (self.rect.width, self.rect.height)
        self.draw_pos = self.rect.topleft
        self.surface = pygame.Surface(self.origin_size)
        self.rot = 0

        self.is_alive = True

        if self.id == 1:
            self.pivot_offset = pygame.Vector2(-8, 0)
        else:
            self.pivot_offset = pygame.Vector2(8, 0)

    def update(self, gun_pos, rot):
        self.rot = rot
        self.rotate()

        self.rect.center = gun_pos + self.pivot_offset.rotate(-self.rot)
        self.draw_pos = self.rect.topleft

    def rotate(self):
        self.rot = self.rot % 360
        self.angle = 3.14 / 180 * self.rot
        new_sur = pygame.transform.rotate(self.surface, self.rot)
        origin_center = self.rect.center
        self.rect = new_sur.get_rect()
        self.rect.center = origin_center
        self.draw_pos = self.rect.topleft

    def get_obj_progress_data(self) -> dict:
        if not self.is_alive:
            return {}
        image_data = create_image_view_data(
            f"{self.id}P_gun", *self.draw_pos, *self.origin_size, self.angle
        )
        return image_data

    def get_obj_init_data(self) -> list:
        img_data = {
            "1P_gun": "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/1P_gun.svg",
            "2P_gun": "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/2P_gun.svg",
        }
        image_init_data = []
        for id, url in img_data.items():
            image_init_data.append(
                create_asset_init_data(
                    id,
                    self.origin_size[0],
                    self.origin_size[1],
                    path.join(IMAGE_DIR, f"{id}.png"),
                    url,
                )
            )
        return image_init_data
