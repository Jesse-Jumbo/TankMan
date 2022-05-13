from .env import FPS
from games.TankMan.src.Props import Props


class Station(Props):
    def __init__(self, _id: int, x: int, y: int, width: int, height: int, capacity: int, cooldown):
        super().__init__(x, y, width, height)
        self._id = _id
        self.count_frame = 0
        self.capacity = capacity
        self.power = capacity
        self.cool_down = cooldown
        self._no = 3
        # 不確定要不要留
        if self._id == 4:
            self.station_name = "bullet_station"
        else:
            self.station_name = "oil_station"

    def update(self):
        if self.power != self.capacity:
            self.count_frame += 1
            if self.count_frame == self.cool_down * FPS:
                self.power += 1
                self.count_frame = 0
        if self.power < self.capacity // 3:
            self._no = 1
        elif self.power != self.capacity:
            self._no = 2
        else:
            self._no = 3

    def get_power(self):
        power = self.power
        self.power = 0
        return power

    def get_info(self):
        info = {"_id": "", "x": self.rect.x, "y": self.rect.y, "power": self.power}
        return info

    def get_image_data(self):
        super().get_image_data()
        return self.image_data
