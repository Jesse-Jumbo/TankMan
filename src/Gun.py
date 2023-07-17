from os import path

import pygame
from mlgame.view.view_model import (create_asset_init_data,
                                    create_image_view_data)

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
        self.rot_speed = 45

        self.used_frame = 0
        self.last_turn_frame = self.used_frame
        self.act_cd = kwargs["act_cd"]

        self.is_alive = True
        self.is_turn_left = False
        self.is_turn_right = False

        if self.id == 1:
            self.pivot_offset = pygame.Vector2(-8, 0)
        else:
            self.pivot_offset = pygame.Vector2(8, 0)

    def update(self, gun_pos):
        self.used_frame += 1
        self.rotate()

        if not self.act_cd:
            self.is_turn_right = False
            self.is_turn_left = False
        elif self.used_frame - self.last_turn_frame > self.act_cd:
            self.is_turn_right = False
            self.is_turn_left = False

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

    def turn_left(self):
        if self.is_turn_left:
            return

        self.rot += self.rot_speed
        self.last_turn_frame = self.used_frame

        self.is_turn_left = True
        self.is_turn_right = False

    def turn_right(self):
        if self.is_turn_right:
            return

        self.rot -= self.rot_speed
        self.last_turn_frame = self.used_frame

        self.is_turn_left = False
        self.is_turn_right = True

    def get_rot(self):
        if self.id == 2:
            return (self.rot + 180) % 360
        return self.rot

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
