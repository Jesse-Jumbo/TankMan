import pygame.sprite
import pytmx

from .env import *


class TankManMap:
    def __init__(self, filename: str):
        tm = pytmx.load_pygame(filename, pixealpha=True)
        self.width = tm.tilewidth
        self.height = tm.tileheight
        self.tmxdata = tm
        self.player_no = 0
        self.wall_no = 0
        self.players = []
        self.walls = []

    def render(self):
        for layer in self.tmxdata.visible_layers:
            for x, y, gid, in layer:
                if isinstance(layer, pytmx.TiledTileLayer):
                    if gid != 0:  # 0代表空格，無圖塊
                        if layer.parent.tiledgidmap[gid] == WALL_IMG_NO:
                            wall_info = {"x": x * TILE_X_SIZE, "y": y * TILE_Y_SIZE}
                            self.walls.append(wall_info)
                        elif layer.parent.tiledgidmap[gid] in PLAYER_IMG_NO_LIST:
                            self.player_no = layer.parent.tiledgidmap[gid]
                            player_info = {"_no": self.player_no, "x": x * TILE_X_SIZE, "y": y * TILE_Y_SIZE}
                            self.players.append(player_info)

    def make_map(self):
        return self.render()
