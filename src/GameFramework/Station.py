from .Props import Props


class Station(Props):
    def __init__(self, construction, **kwargs):
        super().__init__(construction, **kwargs)
        self.count_frame = 0
        self.capacity = kwargs["capacity"]
        self.power = kwargs["capacity"]
        self.cd_time = kwargs["cd_time"]

    def update(self):
        if self.power != self.capacity:
            self.count_frame += 1
            if self.count_frame == self.cd_time * 30:
                self.power += 1
                self.count_frame = 0
        self.update_children()

    def update_children(self):
        """
        A update method for this parent's children
        """
        print("Please overwrite 'self.update_children'")

    def get_supply(self):
        power = self.power
        self.power = 0
        return power

    def get_info(self):
        """
        info = {"id": "", "x": self.rect.x, "y": self.rect.y, "power": self.power}
        """
        print("please overwrite 'self.get_info' method")

    def get_image_data(self):
        """
        image_data = {"id": "", "x": self.rect.x, "y": self.rect.y, "width": self.rect.width,
                      "height": self.rect.height, "angle": 0}
        """
        print("please overwrite 'self.get_image_data' method")

    def get_image_init_data(self):
        """
        return image_init_data = {"id": "image_id", "width": 0, "height": 0, "path": "image_path, "url": 0}
        """
        print("please overwrite 'self.get_image_init_data' method")

