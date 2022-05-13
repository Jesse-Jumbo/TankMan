from .env import FPS
from games.TankMan.src.Props import Props


class Station(Props):
    def __init__(self, _id: int, level: int, x: int, y: int, width: int, height: int, capacity: int, cooldown):
        super().__init__(x, y, width, height)
        self.count_frame = 0
        self.capacity = capacity
        self.power = capacity
        self.cool_down = cooldown
        self._id = _id
        self.level = level

    def update(self):
        if self.power != self.capacity:
            self.count_frame += 1
            if self.count_frame == self.cool_down * FPS:
                self.power += 1
                self.count_frame = 0
        if self.power < self.capacity // 3:
            self.level = 1
        elif self.power != self.capacity:
            self.level = 2
        else:
            self.level = 3

    def get_power(self):
        power = self.power
        self.power = 0
        return power

    def get_info(self):
        info = {"id": "", "x": self.rect.x, "y": self.rect.y, "power": self.power}
        return info

    def get_image_data(self):
        super().get_image_data()
        if self._id == 4:
            self.image_data["id"] = f"bullet_station_{self.level}"
        else:
            self.image_data["id"] = f"oil_station_{self.level}"

        return self.image_data
