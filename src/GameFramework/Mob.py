import pygame

vec = pygame.math.Vector2


class Mob(pygame.sprite.Sprite):
    def __init__(self, construction, **kwargs):
        super().__init__()
        self._id = construction["_id"]
        self._no = construction["_no"]
        self.rect = pygame.Rect(construction["_init_pos"], construction["_init_size"])
        self.origin_center = self.rect.center
        self.hit_rect = pygame.Rect(0, 0, construction["_init_size"][0] - 2, construction["_init_size"][1] - 2)
        self.hit_rect.center = self.rect.center
        self.used_frame = 0
        self.vel = vec(0, 0)

    def update(self):
        self.used_frame += 1
        self.hit_rect.center = self.rect.center
        self.update_children()
        self.act()

    def update_children(self):
        """Define belong to the children update"""
        print("please overwrite this update")

    def act(self):
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
