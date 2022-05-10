from .env import FPS
from games.TankMan.src.Prop import Prop


class Station(Prop):
    def __init__(self, _id: int, _no: int, x: int, y: int, width: int, height: int, capacity: int, cooldown):
        super().__init__(x, y, width, height)
        self._id = _id
        self._no = _no
        self.count_frame = 0
        self.capacity = capacity
        self.power = capacity
        self.cool_down = cooldown

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
