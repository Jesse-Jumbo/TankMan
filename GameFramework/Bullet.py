import pygame.sprite


class Bullet(pygame.sprite.Sprite):
    def __init__(self, center: tuple, width: int, height: int):
        super().__init__()
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center
        self.hit_rect = pygame.Rect(self.rect.x, self.rect.y, width - 2, height - 2)
        self.speed = 10
        self.map_height = 0
        self.map_width = 0
        self.angle = 0

    def update(self):
        self.hit_rect.center = self.rect.center

        if self.rect.bottom < 0 or self.rect.top > self.map_height \
                or self.rect.left > self.map_width or self.rect.right < 0:
            self.kill()

        self.update_bullet()

    def update_bullet(self):
        """A update method for this template's child"""
        print("please overwrite 'self.update_bullet' method")

    def get_image_data(self):
        image_data = {"id": "bullet", "x": self.rect.x, "y": self.rect.y,
                      "width": self.rect.width, "height": self.rect.height, "angle": self.angle}
        return image_data

    def get_image_init_data(self):
        """
        return image_init_data = {"id": "image_id", "width": 0, "height": 0, "path": "image_path, "url": 0}
        """
        print("please overwrite 'self.get_image_init_data' method")

