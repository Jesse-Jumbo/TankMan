import random
from os import path

import pygame
from mlgame.utils.enum import get_ai_name
from mlgame.view.view_model import create_image_view_data, create_asset_init_data

from src.Bullet import Bullet
from src.game_module.TiledMap import create_construction
from .env import IMAGE_DIR


Vec = pygame.math.Vector2


class Mob(pygame.sprite.Sprite):
    def __init__(self, construction: dict, **kwargs):
        """
        初始化怪物資料
        construction可直接由TiledMap打包地圖資訊後傳入
        :param construction:
        :param kwargs:
        """
        super().__init__()
        self.image_id = "mob"
        self.id = construction["_id"]
        self.no = construction["_no"]
        self.rect = pygame.Rect(construction["_init_pos"], construction["_init_size"])
        self.play_rect_area = kwargs["play_rect_area"]
        self.origin_xy = self.rect.topleft
        self.origin_center = self.rect.center
        self.angle = 0
        self.move_steps = 15
        self.used_frame = 0
        self.last_move_frame = 0
        self.last_shoot_frame = 0
        self.move_cd = 15
        self.shoot_cd = random.randint(120, 300)
        self.vel = Vec(0, 0)
        self.is_alive = True
        self.speed = 10
        self.bullets = pygame.sprite.Group()

    def update(self) -> None:
        """
        更新怪物資料
        :param command:
        :return:
        """
        self.used_frame += 1
        self.bullets.update()
        if self.used_frame - self.last_shoot_frame > self.shoot_cd:
            self.shoot()
        self.rect.center += self.vel
        if self.used_frame - self.last_move_frame > self.move_cd:
            if self.move_steps > 10:
                self.move_right()
            else:
                self.move_left()
            self.move_steps -= 1
            if self.move_steps <= 0:
                self.move_steps = 20
                self.move_down()
            self.last_move_frame = self.used_frame
        else:
            self.vel = Vec(0, 0)

    def reset(self) -> None:
        """
        Reset Mob center = origin_center
        :return:
        """
        self.rect.topleft = self.origin_xy

    def get_size(self) -> tuple:
        """
        :return: width, height
        """
        return self.rect.width, self.rect.height

    def get_data_from_obj_to_game(self) -> dict:
        """
        在遊戲主程式獲取遊戲資料給AI時被調用
        :return:
        """
        info = {"id": self.image_id
                , "x": self.rect.x
                , "y": self.rect.y
                }
        return info

    def get_obj_progress_data(self) -> dict or list:
        """
        使用view_model函式，建立符合mlgame物件更新資料格式的資料，在遊戲主程式更新畫面資訊時被調用
        :return:
        """
        progress_date_list = []
        for bullet in self.bullets:
            if isinstance(bullet, Bullet):
                progress_date_list.append(bullet.get_obj_progress_data())
        progress_date_list.append(create_image_view_data(self.image_id, *self.rect.topleft, self.rect.width, self.rect.height, self.angle))
        return progress_date_list

    def get_obj_init_data(self) -> dict or list:
        """
        使用view_model函式，建立符合mlgame物件初始資料格式的資料，在遊戲主程式初始畫面資訊時被調用
        :return:
        """
        image_init_data = create_asset_init_data(self.image_id, self.rect.width, self.rect.height
                                                 , path.join(IMAGE_DIR, f"mob.png"), "url")
        return image_init_data

    def get_info_to_game_result(self):
        info = {"id": self.image_id
                , "x": self.rect.x
                , "y": self.rect.y
                }
        return info

    def shoot(self):
        self.last_shoot_frame = self.used_frame
        _id = "mob"
        _no = random.randint(1, 6)
        bullet = Bullet(construction=create_construction(_id=_id, _no=_no
                                                         , _init_pos=self.rect.center, _init_size=(12, 27))
                        , play_rect_area=self.play_rect_area)
        self.bullets.add(bullet)

    def move_left(self):
        self.vel.x = -self.speed

    def move_right(self):
        self.vel.x = self.speed

    def move_down(self):
        self.vel.y = self.speed

