from ..GameFramework.Station import Station


class TankStation(Station):
    def __init__(self, _id: int, level: int, x: int, y: int, width: int, height: int, capacity: int, cooldown_time):
        super().__init__(level, x, y, width, height, capacity, cooldown_time)
        self._id = _id
        self.level = level

    def update_children(self):
        if self.power < self.capacity // 3:
            self.level = 1
        elif self.power != self.capacity:
            self.level = 2
        else:
            self.level = 3

    def get_info(self):
        if self._id == 4:
            _id = "bullet_station"
        else:
            _id = "oil_station"
        info = {"id": _id, "x": self.rect.x, "y": self.rect.y, "power": self.power}
        return info

    def get_image_data(self):
        image_data = {"id": f"", "x": self.rect.x, "y": self.rect.y, "width": self.rect.width,
                      "height": self.rect.height, "angle": 0}
        if self._id == 4:
            image_data["id"] = f"bullet_station_{self.level}"
        else:
            image_data["id"] = f"oil_station_{self.level}"

        return image_data
