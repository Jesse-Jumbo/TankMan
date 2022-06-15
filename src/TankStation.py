from os import path

from games.TankMan.GameFramework.Station import Station
from games.TankMan.src.env import IMAGE_DIR
from mlgame.view.view_model import create_asset_init_data


class TankStation(Station):
    def __init__(self, construction, **kwargs):
        super().__init__(construction, **kwargs)
        self.level = kwargs["level"]

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
            image_data["id"] = f"bullets_{self.level}"
        else:
            image_data["id"] = f"oil_{self.level}"

        return image_data

    def get_image_init_data(self):
        img_data = {}
        for i in range(1, 4):
            img_data[f"bullets_{i}"] = f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/bullets_{i}.png"
            img_data[f"oil_{i}"] = f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/oil_{i}.png"
        image_init_data = []
        for id, url in img_data.items():
            image_init_data.append(create_asset_init_data(id, self.rect.width, self.rect.height,
                                                          path.join(IMAGE_DIR, f"{id}.png"), url))
        return image_init_data
