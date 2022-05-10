import random

import pygame.draw

from mlgame.gamedev.game_interface import GameStatus
from .Player import Player
from .env import *

vec = pygame.math.Vector2


class TankPlayer(Player):
    def __init__(self, _no: int, x: int, y: int, width: int, height: int):
        super().__init__(_no, x, y, width, height)
        self.image_id = f"player_{self._no}P"
        self.img_path = PLAYER_IMG_PATH_LIST[self._no - 1]
        self.surface = pygame.Surface((width, height))
        self.speed = PLAYER_SPEED
        self.angle = 0
        self.score = 0
        self.used_frame = 0
        self.move = {"left_up": vec(-self.speed, -self.speed), "right_up": vec(self.speed, -self.speed), "left_down": vec(-self.speed, self.speed), "right_down": vec(self.speed, self.speed),
                     "left": vec(-self.speed, 0), "right": vec(self.speed, 0), "up": vec(0, -self.speed), "down": vec(0, self.speed)}
        self.rot = 0
        self.last_shoot_frame = self.used_frame
        self.rot_speed = 45
        self.shield = 100
        self.power = 10
        self.oil = 100
        self.is_shoot = False
        self.is_forward = False
        self.is_backward = False
        self.is_alive = True

    def update(self, commands: str):
        super().update(commands)
        self.rotate()
        if self.power > 10:
            self.power = 10
        self.oil = round(self.oil, 2)
        if self.oil > 100:
            self.oil = 100

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def rotate(self):
        new_sur = pygame.transform.rotate(self.surface, self.rot)
        self.rot = self.rot % 360
        self.angle = 3.14 / 180 * self.rot
        origin_center = self.rect.center
        self.rect = new_sur.get_rect()
        self.rect.center = origin_center

    def create_shoot_info(self):
        shoot_info = {"player_no": self._no, "center_pos": self.rect.center, "rot": self.rot}
        return shoot_info

    def act(self, commands: str):
        if self.oil:
            if commands == LEFT_CMD:
                self.oil -= 0.1
                self.turn_left()
            elif commands == RIGHT_CMD:
                self.oil -= 0.1
                self.turn_right()
            elif commands == FORWARD_CMD:
                self.oil -= 0.1
                self.is_forward = True
                self.is_backward = False
                self.forward()
            elif commands == BACKWARD_CMD:
                self.oil -= 0.1
                self.is_backward = True
                self.is_forward = False
                self.backward()
        if self.power and commands == SHOOT:
            if self.used_frame - self.last_shoot_frame > SHOOT_COOLDOWN:
                self.last_shoot_frame = self.used_frame
                self.power -= 1
                self.is_shoot = True

    def forward(self):
        if self._no != 1:
            rot = self.rot - 180
        else:
            rot = self.rot
        if rot == 0:
            self.rect.center += self.move["left"]
        elif rot == 315 or rot == -45:
            self.rect.center += self.move["left_up"]
        elif rot == 270 or rot == -90:
            self.rect.center += self.move["up"]
        elif rot == 225 or rot == -135:
            self.rect.center += self.move["right_up"]
        elif rot == 180 or rot == -180:
            self.rect.center += self.move["right"]
        elif rot == 135 or rot == -225:
            self.rect.center += self.move["right_down"]
        elif rot == 90 or rot == -270:
            self.rect.center += self.move["down"]
        elif rot == 45 or rot == -315:
            self.rect.center += self.move["left_down"]

    def backward(self):
        if self._no != 1:
            rot = self.rot - 180
        else:
            rot = self.rot
        if rot == 0:
            self.rect.center += self.move["right"]
        elif rot == 315 or rot == -45:
            self.rect.center += self.move["right_down"]
        elif rot == 270 or rot == -90:
            self.rect.center += self.move["down"]
        elif rot == 225 or rot == -135:
            self.rect.center += self.move["left_down"]
        elif rot == 180 or rot == -180:
            self.rect.center += self.move["left"]
        elif rot == 135 or rot == -225:
            self.rect.center += self.move["left_up"]
        elif rot == 90 or rot == -270:
            self.rect.center += self.move["up"]
        elif rot == 45 or rot == -315:
            self.rect.center += self.move["right_up"]

    def turn_left(self):
        self.rot += self.rot_speed

    def turn_right(self):
        self.rot -= self.rot_speed

    def collide_with_walls(self):
        if self.is_forward:
            self.backward()
        else:
            self.forward()

    def collide_with_bullets(self):
        self.shield -= random.randrange(1, 10)
        if self.shield <= 0:
            self.lives -= 1
            self.reset()

    def get_info(self):
        player_info = {"player_id": f"{self._no}P",
                       "x": self.rect.x,
                       "y": self.rect.y,
                       "speed": self.speed,
                       "score": self.score
                       }
        return player_info
