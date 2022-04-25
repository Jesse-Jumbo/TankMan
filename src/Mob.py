import pygame
from env import *


class Mob(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image_path = MOB_IMG
        self.image_id = ""
        self.rect = ALL_OBJECT_SIZE.copy()
        self.rect.x = x
        self.rect.y = y
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = pygame.math.Vector2(0, 0)
        self.pos.xy = self.rect.center
        self.vel = pygame.math.Vector2(0, 0)
        self.speed = MOB_SPEED

    def update(self, *args, **kwargs) -> None:
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def collide_with_walls(self):
        self.vel *= -1
        self.pos += self.vel
        self.hit_rect.center = self.pos
        self.rect.center = self.pos

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

    def get_position(self):
        return self.rect.x, self.rect.y
