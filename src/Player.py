import pygame.draw

from mlgame.gamedev.game_interface import GameStatus
from .env import *

vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, _no: int, x: int, y: int):
        super().__init__()
        self._no = _no
        self.image_id = f"player_{self._no}P"
        self.img_path = PLAYER_IMG_PATH_LIST[self._no - 1]
        self.surface = pygame.Surface((TILE_X_SIZE, TILE_Y_SIZE))

        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.origin_center = self.rect.center
        self.x = x
        self.y = y
        self.hit_rect = PLAYRE_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(0, 0)
        self.pos.xy = self.rect.center
        self.speed = PLAYER_SPEED
        self.result_info = {}
        self.status = GameStatus.GAME_ALIVE
        self.angle = 0
        self.score = 0
        self.used_frame = 0
        self.move = {"left_up": vec(-1, -1), "right_up": vec(1, -1), "left_down": vec(-1, 1), "right_down": vec(1, 1),
                     "left": vec(-1, 0), "right": vec(1, 0), "up": vec(0, -1), "down": vec(0, 1)}
        self.rot = 0
        self.last_frame = self.used_frame
        self.rot_speed = 45
        self.can_shoot = True
        self.live = 100

    def update(self, commands: dict):
        if self.used_frame - self.last_frame > FPS // 4:
            self.can_shoot = True
        new_sur = pygame.transform.rotate(self.surface, self.rot)
        self.rot = (self.rot + 360) % 360
        self.angle = 3.14 / 180 * self.rot
        new_rect = self.rect
        self.rect = new_sur.get_rect()
        self.rect.center = new_rect.center
        self.used_frame += 1
        self.handle_key_event(commands)
        self.pos = self.rect.center
        self.hit_rect.center = self.pos
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def handle_key_event(self, commands: dict):
        if not commands[f"{self._no}P"]:
            return True
        else:
            if commands[f"{self._no}P"] == LEFT_CMD:
                self.turn_left()
            elif commands[f"{self._no}P"] == RIGHT_CMD:
                self.turn_right()
            elif commands[f"{self._no}P"] == FORWARD_CMD:
                self.forward()
            elif commands[f"{self._no}P"] == BACKWARD_CMD:
                self.backward()

    def forward(self):
        if self._no != 1:
            rot = self.rot - 180
        else:
            rot = self.rot
        if rot == 0:
            self.rect = self.rect.move(self.move["left"])
        elif rot == 315 or rot == -45:
            self.rect = self.rect.move(self.move["left_up"])
        elif rot == 270 or rot == -90:
            self.rect = self.rect.move(self.move["up"])
        elif rot == 225 or rot == -135:
            self.rect = self.rect.move(self.move["right_up"])
        elif rot == 180 or rot == -180:
            self.rect = self.rect.move(self.move["right"])
        elif rot == 135 or rot == -225:
            self.rect = self.rect.move(self.move["right_down"])
        elif rot == 90 or rot == -270:
            self.rect = self.rect.move(self.move["down"])
        elif rot == 45 or rot == -315:
            self.rect = self.rect.move(self.move["left_down"])

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

    def get_info(self):
        self.player_info = {"player_id": f"{self._no}P",
                            "pos_x": int(self.pos.x),
                            "pos_y": int(self.pos.y),
                            "velocity": "{:.2f}".format(self.speed),
                            "score": self.score,
                            }
        return self.player_info

    def get_result(self):
        self.result_info = {"player_id": f"{self._no}P",
                            "pos_x": int(self.pos.x),
                            "pos_y": int(self.pos.y),
                            "velocity": "{:.2f}".format(self.speed),
                            "score": self.score,
                            "used_frame": self.used_frame,
                            }
        return self.result_info

    def collide_with_walls(self):
        self.backward()

    def collide_with_bullets(self):
        self.live -= 10
        if self.live <= 0:
            self.status = GameStatus.GAME_OVER

    @property
    def player_data(self):
        return {
            "type": "rect",
            "name": f"{self._no}P",
            "x": self.rect.x,
            "y": self.rect.y,
            "angle": self.angle,
            "width": self.rect.width,
            "height": self.rect.height,
        }

    def get_position(self):
        return self.rect.x, self.rect.y
