import sys
from os import path

import pygame.display
from mlgame.view.view_model import Scene

from .TankBattleMode import TankBattleMode
from .env import MAP_DIR, IMAGE_DIR, GREEN
from .GameFramework.MyGame import GameFramework

'''need some fuction same as arkanoid which without dash in the name of fuction'''


class TankMan(GameFramework):
    def __init__(self, user_num: int, is_manual: str, map_no: int, frame_limit: int, sound: str):
        self.is_manual = is_manual
        super().__init__(user_num, map_no, frame_limit, sound)
        self.scene = Scene(width=self.game_mode.map_width, height=self.game_mode.map_height+100, color="#ffffff", bias_y=50)
        pygame.display.set_caption(f"TankMan！ user_num: {user_num} ；is_manual: {is_manual} ；map_no: {map_no} ；frame_limit: {frame_limit} ；sound: {sound}")
        pygame.display.set_icon(pygame.image.load(path.join(IMAGE_DIR, "logo.png")))

    def set_game_mode(self):
        map_path = path.join(MAP_DIR, self.map_name)
        game_mode = TankBattleMode(self._user_num, self.is_manual, map_path, self.frame_limit, self.is_sound)
        return game_mode
