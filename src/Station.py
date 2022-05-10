from .env import FPS
from games.TankMan.src.Prop import Prop


class Station(Prop):
    def __init__(self, _no, x, y, width, height):
        super().__init__(x, y, width, height)
        self._no = _no
        self.count_frame = 0
        self.power = 10

    def update(self):
        if self.power != 10:
            self.count_frame += 1
            if self.count_frame == 5 * FPS:
                self.power += 1
                self.count_frame = 0

    def get_power(self):
        power = self.power
        self.power = 0
        return power
