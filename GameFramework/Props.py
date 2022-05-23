import pygame


class Props(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.hit_rect = pygame.Rect(x, y, width - 2, height - 2)

    def update(self):
        pass

    def get_xy_pos(self):
        return self.rect.x, self.rect.y

    def get_info(self):
        """
        add all required information for player training

        info = {"id": f"{self.id}", "x": 0, "y": 0}
        """

    def get_size(self):
        return self.rect.width, self.rect.height

    def get_image_data(self):
        """
        image_data = {"id": f"", "x": self.rect.x, "y": self.rect.y, "width": self.get_size()[0],
                           "height": self.get_size()[1], "angle": 0}
        """


