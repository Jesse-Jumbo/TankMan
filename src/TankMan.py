from os import path

from mlgame.view.view_model import Scene
from .TankBattleMode import TankBattleMode
from .env import WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, MAP_DIR
from games.TankMan.GameFramework.MyGame import GameFramework

'''need some fuction same as arkanoid which without dash in the name of fuction'''


class TankMan(GameFramework):
    def __init__(self, user_num: int, map_no: int, frame_limit: int, sound: str):
        super().__init__(user_num, map_no, frame_limit, sound)
        # self.scene = Scene(WINDOW_WIDTH, WINDOW_HEIGHT, BLACK)
        self.game_mode = self.set_game_mode()

    def set_game_mode(self):
        map_path = path.join(MAP_DIR, self.map_name)
        game_mode = TankBattleMode(self._user_num, map_path, self.frame_limit, self.is_sound)
        return game_mode
