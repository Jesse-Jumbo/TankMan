from os import path

import pygame
from mlgame.utils.enum import get_ai_name
from mlgame.view.view_model import create_image_view_data, create_asset_init_data

from .env import IMAGE_DIR


DOWN_CMD = "DOWN"
UP_CMD = "UP"
RIGHT_CMD = "RIGHT"
LEFT_CMD = "LEFT"
SHOOT_CMD = "SHOOT"
Vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, construction: dict, **kwargs):
        """
        初始化玩家資料
        construction可直接由TiledMap打包地圖資訊後傳入
        :param construction:
        :param kwargs:
        """
        super().__init__()
        self.image_id = "1P"
        self.id = construction["_id"]
        self.no = construction["_no"]
        self.rect = pygame.Rect(construction["_init_pos"], construction["_init_size"])
        self.play_rect_area = kwargs["play_rect_area"]
        self.origin_xy = self.rect.topleft
        self.origin_center = self.rect.center
        self.angle = 0
        self.used_frame = 0
        self.vel = Vec(0, 0)
        self.is_alive = True
        self.speed = 10

    def update(self, command: dict) -> None:
        """
        更新玩家資料
        :param command:
        :return:
        """
        self.used_frame += 1
        self.rect.center += self.vel
        self.act(command[self.id])

    def reset(self) -> None:
        """
        Reset Player center = origin_center
        :return:
        """
        self.rect.topleft = self.origin_xy

    def act(self, action: list) -> None:
        if not action:
            return
        if SHOOT_CMD in action:
            self.shoot()
        if LEFT_CMD in action and self.rect.left > self.play_rect_area.left:
            self.move_left()
        elif RIGHT_CMD in action and self.rect.right < self.play_rect_area.right:
            self.move_right()
        elif UP_CMD in action and DOWN_CMD not in action and self.rect.top > self.play_rect_area.top:
            self.move_up()
        elif DOWN_CMD in action and UP_CMD not in action and self.rect.bottom < self.play_rect_area.bottom:
            self.move_down()
        else:
            self.vel = Vec(0, 0)

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
        info = {"id": f"{self.id}P",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": self.angle
                }
        return info

    def get_obj_progress_data(self) -> dict or list:
        """
        使用view_model函式，建立符合mlgame物件更新資料格式的資料，在遊戲主程式更新畫面資訊時被調用
        :return:
        """
        image_data = create_image_view_data(f"{self.id}P", *self.rect.topleft, self.rect.width, self.rect.height, self.angle)
        return image_data

    def get_obj_init_data(self) -> dict or list:
        """
        使用view_model函式，建立符合mlgame物件初始資料格式的資料，在遊戲主程式初始畫面資訊時被調用
        :return:
        """
        image_init_data = create_asset_init_data(f"{self.id}P", self.rect.width, self.rect.height
                                                 , path.join(IMAGE_DIR, f"{self.id}.png"), "url")
        return image_init_data

    def get_info_to_game_result(self):
        info = {"id": f"{self.id}P"
                , "x": self.rect.x
                , "y": self.rect.y
                }
        return info

    def shoot(self):
        pass

    def move_left(self):
        self.vel.x = -self.speed

    def move_right(self):
        self.vel.x = self.speed

    def move_up(self):
        self.vel.y = -self.speed

    def move_down(self):
        self.vel.y = self.speed

