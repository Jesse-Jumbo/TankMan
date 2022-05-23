import pygame

vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, _id: int, _no: int, x: int, y: int, width: int, height: int):
        super().__init__()
        self._id = _id
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
        self.image_init_data = {}

    def update(self, commands):
        self.used_frame += 1
        self.hit_rect.center = self.rect.center
        self.act(commands)
        if self.lives < 0:
            self.is_alive = False
        self.update_children()

    def update_children(self):
        """Define belong to the children update"""
        print("please overwrite this update")

    def act(self, commands):
        """Define when receive act commands will run what method"""
        print("please overwrite 'self.act' method")

    def get_info(self):
        """
        add all player information

        info = {"id": "", "x": 0, "y": 0}
        """
        print("please overwrite 'self.get_info' method")

    def collide_with_walls(self):
        pass

    def get_xy_pos(self):
        return self.rect.x, self.rect.y

    def reset(self):
        self.rect.center = self.origin_center

    def get_image_data(self):
        """
        return image_data = {"id": "image_id", "x": 0, "y": 0, "width": 0, "height": 0, "angle": 0}
        """
        print("please overwrite 'self.get_image_data' method")
