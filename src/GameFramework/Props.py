import pygame


class Props(pygame.sprite.Sprite):
    def __init__(self, construction, **kwargs):
        super().__init__()
        self.rect = pygame.Rect(construction["_init_pos"], construction["_init_size"])
        self.hit_rect = pygame.Rect(0, 0, construction["_init_size"][0]-kwargs["margin"]
                                    , construction["_init_size"][1]-kwargs["spacing"])
        self.hit_rect.center = self.rect.center
        self._id = construction["_id"]
        self._no = construction["_no"]

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

    def get_image_init_data(self):
        """
        return image_init_data = {"id": "image_id", "width": 0, "height": 0, "path": "image_path, "url": 0}
        """
        print("please overwrite 'self.get_image_init_data' method")
