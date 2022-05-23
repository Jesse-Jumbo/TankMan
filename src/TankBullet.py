import pygame

from .env import WINDOW_HEIGHT, WINDOW_WIDTH
from ..GameFramework.Bullet import Bullet


vec = pygame.math.Vector2


class TankBullet(Bullet):
    def __init__(self, _id: int, center: tuple, width: int, height: int, rot: int):
        super().__init__(center, width, height)
        self.map_width = WINDOW_WIDTH
        self.map_height = WINDOW_HEIGHT
        self._id = _id
        self.rot = rot
        self.angle = 3.14 / 180 * (self.rot + 90)
        self.move = {"left_up": vec(-self.speed, -self.speed), "right_up": vec(self.speed, -self.speed),
                     "left_down": vec(-self.speed, self.speed), "right_down": vec(self.speed, self.speed),
                     "left": vec(-self.speed, 0), "right": vec(self.speed, 0), "up": vec(0, -self.speed),
                     "down": vec(0, self.speed)}

    def update_bullet(self):
        if self.rot == 0:
            self.rect.center += self.move["left"]
        elif self.rot == 315 or self.rot == -45:
            self.rect.center += self.move["left_up"]
        elif self.rot == 270 or self.rot == -90:
            self.rect.center += self.move["up"]
        elif self.rot == 225 or self.rot == -135:
            self.rect.center += self.move["right_up"]
        elif self.rot == 180 or self.rot == -180:
            self.rect.center += self.move["right"]
        elif self.rot == 135 or self.rot == -225:
            self.rect.center += self.move["right_down"]
        elif self.rot == 90 or self.rot == -270:
            self.rect.center += self.move["down"]
        elif self.rot == 45 or self.rot == -315:
            self.rect.center += self.move["left_down"]
