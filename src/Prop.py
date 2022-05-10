import pygame


class Prop(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.hit_rect = pygame.Rect(x, y, width-2, height-2)

    def update(self):
        pass

    def get_pos_xy(self):
        return self.rect.x, self.rect.y

    def get_size(self):
        return self.rect.width, self.rect.height
