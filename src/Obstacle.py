import ntpath

import pygame.math

from .env import *


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.rect = ALL_OBJECT_SIZE.copy()
        self.rect.x = x
        self.rect.y = y
        self.hit_rect = WALL_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = pygame.math.Vector2(self.rect.center)

    def update(self, *args, **kwargs) -> None:
        pass

    def get_position(self):
        return self.rect.x, self.rect.y
