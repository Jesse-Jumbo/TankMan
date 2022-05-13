from .env import FPS
from games.TankMan.src.Props import Props


class Station(Props):
    def __init__(self, level: int, x: int, y: int, width: int, height: int, capacity: int, cooldown):
        super().__init__(x, y, width, height)
        self.count_frame = 0
        self.capacity = capacity
        self.power = capacity
        self.cool_down = cooldown
        self.level = level

    def update(self):
        if self.power != self.capacity:
            self.count_frame += 1
            if self.count_frame == self.cool_down * FPS:
                self.power += 1
                self.count_frame = 0

    def get_power(self):
        power = self.power
        self.power = 0
        return power

    def get_info(self):
        """
        info = {"id": "", "x": self.rect.x, "y": self.rect.y, "power": self.power}
        """

    def get_image_data(self):
        """
        image_data = {"id": "", "x": self.rect.x, "y": self.rect.y, "width": self.rect.width,
                      "height": self.rect.height, "angle": 0}
        """
