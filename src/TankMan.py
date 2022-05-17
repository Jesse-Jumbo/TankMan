from os import path

from mlgame.view.view_model import Scene
from .TankBattleMode import TankBattleMode
from GameFramework.MyGame import GameFramework
from .env import WIDTH, HEIGHT, BLACK, MAP_DIR

'''need some fuction same as arkanoid which without dash in the name of fuction'''


class TankMan(GameFramework):
    def __init__(self, map_no: int, time_limit: int, sound: str):
        super().__init__(map_no, time_limit, sound)
        self.scene = Scene(WIDTH, HEIGHT, BLACK)
        self.game_mode = self.set_game_mode()

    def set_game_mode(self):
        map_path = path.join(MAP_DIR, self.map_name)
        game_mode = TankBattleMode(map_path, self.time_limit, self.is_sound)
        return game_mode
