import pygame

vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, _no: int, x: int, y: int, width: int, height: int):
        super().__init__()
        self._no = _no
        self.rect = pygame.Rect(x, y, width, height)
        self.origin_center = self.rect.center
        self.hit_rect = pygame.Rect(x, y, width - 2, height - 2)
        self.result_info = {}
        self.score = 0
        self.used_frame = 0
        self.lives = 3
        self.vel = vec(0, 0)
        self.is_alive = True
        self.origin_size = (width, height)

    def update(self, commands: str):
        self.used_frame += 1
        self.hit_rect.center = self.rect.center
        self.act(commands)
        if self.lives < 0:
            self.is_alive = False

    def act(self, commands: str):
        pass

    def get_info(self):
        player_info = {"player_id": f"{self._no}P",
                       "x": self.rect.x,
                       "y": self.rect.y,
                       }
        return player_info

    def collide_with_walls(self):
        pass

    def get_pos_xy(self):
        return self.rect.x, self.rect.y

    def get_origin_size(self):
        return self.origin_size

    def reset(self):
        self.rect.center = self.origin_center
