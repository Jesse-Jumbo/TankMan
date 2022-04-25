import pygame.math

from .env import *


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obj_id: int, img_no: int,  x: int, y: int):
        super().__init__()
        self.img_path = WALL_IMG
        self.obj_id = obj_id
        self.rect = ALL_OBJECT_SIZE.copy()
        self.rect.x = x
        self.rect.y = y
        self.hit_rect = self.rect
        self.pos = pygame.math.Vector2(x, y)

    def update(self, *args, **kwargs) -> None:
        pass

    def get_position(self):
        return self.rect.x, self.rect.y
