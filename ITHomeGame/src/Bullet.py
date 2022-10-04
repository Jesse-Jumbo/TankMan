from os import path

import pygame
from mlgame.utils.enum import get_ai_name
from mlgame.view.view_model import create_image_view_data, create_asset_init_data

from .env import IMAGE_DIR


Vec = pygame.math.Vector2


class Bullet(pygame.sprite.Sprite):
    def __init__(self, construction: dict, **kwargs):
        """
        初始化子彈資料
        construction可直接由TiledMap內的函式打包資訊後傳入
        :param construction:
        :param kwargs:
        """
        super().__init__()
        self.image_id = "bullet"
        self.id = construction["_id"]
        self.no = construction["_no"]
        self.rect = pygame.Rect(construction["_init_pos"], construction["_init_size"])
        self.play_rect_area = kwargs["play_rect_area"]
        self.origin_xy = self.rect.topleft
        self.origin_center = self.rect.center
        self.angle = 0
        if self.id == "mob":
            self.angle = 180 * 3.14 // 180
        self.vel = Vec(0, 0)
        self.is_alive = True
        self.speed = 10

    def update(self) -> None:
        """
        更新子彈資料
        :param command:
        :return:
        """
        self.rect.center += self.vel
        if self.id == "player":
            self.move_up()
        else:
            self.move_down()

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
        image_data = create_image_view_data(self.image_id+"_"+self.id, *self.rect.topleft, self.rect.width, self.rect.height, self.angle)
        return image_data

    def get_obj_init_data(self) -> dict or list:
        """
        使用view_model函式，建立符合mlgame物件初始資料格式的資料，在遊戲主程式初始畫面資訊時被調用
        :return:
        """
        image_init_data = create_asset_init_data(self.image_id, self.rect.width, self.rect.height
                                                 , path.join(IMAGE_DIR, f"{self.image_id}_0{self.no}.png"), "url")
        return image_init_data

    def get_info_to_game_result(self):
        info = {"id": self.image_id+"_"+self.id
                , "x": self.rect.x
                , "y": self.rect.y
                }
        return info

    def move_up(self):
        self.vel.y = -self.speed

    def move_down(self):
        self.vel.y = self.speed

