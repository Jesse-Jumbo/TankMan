from ..GameFramework.Props import Props


class TankWall(Props):
    def __init__(self, _id: int, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self._id = _id
        self.lives = 5

    def update(self, *args, **kwargs) -> None:
        if self.lives <= 0:
            self.kill()

    def collide_with_bullets(self):
        if self.lives > 0:
            self.lives -= 1

    def get_xy_pos(self):
        return self.rect.x, self.rect.y

    def get_info(self):
        info = {"id": f"wall_{self._id}.{self.lives}", "x": self.rect.x, "y": self.rect.y, "lives": self.lives}
        return info

    def get_image_data(self):
        if self.lives > 0:
            image_data = {"id": f"wall_{self._id}.{self.lives}", "x": self.rect.x, "y": self.rect.y,
                          "width": self.rect.width, "height": self.rect.height, "angle": 0}
            return image_data
