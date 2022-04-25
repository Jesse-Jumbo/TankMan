import pygame.sprite
import pytmx

from games.TankMan.src.Obstacle import Obstacle
from games.TankMan.src.Player import Player
from games.TankMan.src.Mob import Mob
from .env import *


class TiledMap:
    def __init__(self, filename: str):
        tm = pytmx.load_pygame(filename, pixealpha=True)
        self.width = tm.tilewidth
        self.height = tm.tileheight
        self.tmxdata = tm
        self.wall_no = 0
        self.player = pygame.sprite.Sprite()
        self.mobs = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

    def render(self):
        for layer in self.tmxdata.visible_layers:
            for x, y, gid, in layer:
                if isinstance(layer, pytmx.TiledTileLayer):
                    if gid != 0:  # 0代表空格，無圖塊
                        if layer.parent.tiledgidmap[gid] in WALL_IMG_NO_LIST:
                            self.wall_no += 1
                            wall = Obstacle(self.wall_no, layer.parent.tiledgidmap[gid],
                                            x * TILE_X_SIZE, y * TILE_Y_SIZE)
                            self.walls.add(wall)
                        elif layer.parent.tiledgidmap[gid] in MOB_IMG_NO_LIST:
                            mob = Mob(x * TILE_X_SIZE, y * TILE_Y_SIZE)
                            self.mobs.add(mob)
                        elif layer.parent.tiledgidmap[gid] == PLAYER_IMG_NO:
                            self.player = Player(x * TILE_X_SIZE, y * TILE_Y_SIZE)

    def make_map(self):
        return self.render()
