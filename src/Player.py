import pygame

from mlgame.gamedev.game_interface import GameStatus, GameResultState
from .env import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.player_no = 1
        self.image_dic = {}
        self.image_index = 0
        self.image_id = f""
        self.rect = ALL_OBJECT_SIZE.copy()
        self.rect.x = x
        self.rect.y = y
        self.status = GameStatus.GAME_ALIVE
        self.pacman_info = {}
        self.result_info = {}
        self.used_frame = 0

        self.hit_rect = PLAYRE_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(0, 0)
        self.pos.xy = self.rect.center
        self.speed = PLAYER_SPEED
        self.img_change_control = 0.4
        self.score = 0

    def update(self, commands: dict):
        self.used_frame += 1
        self.image_index += self.img_change_control
        if self.image_index >= len(self.image_dic):
            self.image_index = 0
        self.handle_key_event(commands)
        self.rect.center = self.pos

        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        self.rect.center = self.hit_rect.center

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def handle_key_event(self, commands: dict):
        if not commands[f"{self.player_no}P"]:
            return True
        else:
            if commands[f"{self.player_no}P"] == LEFT_CMD:
                self.move_left()
            elif commands[f"{self.player_no}P"] == RIGHT_CMD:
                self.move_right()
            elif commands[f"{self.player_no}P"] == UP_CMD:
                self.move_up()
            elif commands[f"{self.player_no}P"] == DOWN_CMD:
                self.move_down()

    def move_up(self):
        self.image_path = f""
        self.vel.y = -self.speed
        self.pos.y += self.vel.y

    def move_down(self):
        self.image_path = f""
        self.vel.y = self.speed
        self.pos.y += self.vel.y

    def move_left(self):
        self.image_path = f""
        self.vel.x = -self.speed
        self.pos.x += self.vel.x

    def move_right(self):
        self.image_path = f""
        self.vel.x = self.speed
        self.pos.x += self.vel.x

    def get_info(self):
        self.player_info = {"player_id": f"{self.player_no}P",
                            "pos_x": int(self.pos.x),
                            "pos_y": int(self.pos.y),
                            "velocity": "{:.2f}".format(self.speed),
                            "score": self.score,
                            }
        return self.player_info

    def get_result(self):
        self.result_info = {"player_id": f"{self.player_no}P",
                            "pos_x": int(self.pos.x),
                            "pos_y": int(self.pos.y),
                            "velocity": "{:.2f}".format(self.speed),
                            "score": self.score,
                            "used_frame": self.used_frame,
                            }
        return self.result_info

    def collide_with_walls(self):
        self.vel *= -1
        self.pos += self.vel
        self.hit_rect.center = self.pos
        self.rect.center = self.pos

    def collide_with_mobs(self):
        self.status = GameStatus.GAME_OVER

    @property
    def player_data(self):
        return {
            "type": "rect",
            "name": f"player_{self.player_no}",
            "x": self.rect.x,
            "y": self.rect.y,
            "angle": 0,
            "width": self.rect.width,
            "height": self.rect.height,
        }

    def get_position(self):
        return self.rect.x, self.rect.y
