from games.TankMan.src.env import FPS
from GameFramework.Props import Props


class Station(Props):
    def __init__(self, level: int, x: int, y: int, width: int, height: int, capacity: int, cooldown_time: int):
        super().__init__(x, y, width, height)
        self.count_frame = 0
        self.capacity = capacity
        self.power = capacity
        self.cool_down_time = cooldown_time
        self.level = level

    def update(self):
        if self.power != self.capacity:
            self.count_frame += 1
            if self.count_frame == self.cool_down_time * FPS:
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

    def get_image_data(self):
        """
        image_data = {"id": "", "x": self.rect.x, "y": self.rect.y, "width": self.rect.width,
                      "height": self.rect.height, "angle": 0}
        """
