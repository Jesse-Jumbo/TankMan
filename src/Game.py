from os import path

import pygame
from mlgame.game.paia_game import PaiaGame, GameStatus
from mlgame.view.view_model import Scene

from .TeamBattleMode import TeamBattleMode
from .game_module.fuctions import get_sprites_progress_data

MAP_WIDTH = 1000
MAP_HEIGHT = 600
GAME_DIR = path.dirname(__file__)
MAP_DIR = path.join(GAME_DIR, "..", "asset", "maps")
SOUND_DIR = path.join(GAME_DIR, "..", "asset", "sound")
IMAGE_DIR = path.join(GAME_DIR, "..", "asset", "image")


class Game(PaiaGame):
    def __init__(self, user_num: int, green_team_num: int, blue_team_num: int, is_manual: str, frame_limit: int, sound: str):
        super().__init__(user_num)
        # init game
        self.green_team_num = green_team_num
        self.blue_team_num = blue_team_num
        self.is_paused = False
        self.is_debug = False
        self.is_sound = False
        self.is_manual = False
        if sound == "on":
            self.is_sound = True
        if is_manual:
            self.is_manual = True
        self.attachements = []
        self.frame_limit = frame_limit
        self.game_mode = self.set_game_mode()
        self.scene = Scene(width=self.game_mode.scene_width, height=self.game_mode.scene_height, color="#ffffff",
                           bias_y=50)

    def get_data_from_game_to_player(self) -> dict:
        to_players_data = self.game_mode.get_ai_data_to_player()
        return to_players_data

    def update(self, commands: dict):
        self.handle_event(commands)
        self.game_mode.debugging(self.is_debug)
        if not self.is_paused:
            self.frame_count += 1
            self.game_mode.update(commands)
            if not self.is_running():
                return "RESET"

    def reset(self):
        self.frame_count = 0
        self.game_mode.reset()
        self.rank()

    def get_scene_init_data(self) -> dict:
        """
        Get the scene and object information for drawing on the web
        """
        game_info = {'scene': self.scene.__dict__,
                     'assets': self.game_mode.get_init_image_data()}

        return game_info

    def get_scene_progress_data(self) -> dict:
        """
        Get the position of src objects for drawing on the web
        """
        scene_progress = {'background': [],
                          'object_list': [*self.game_mode.background, *self.get_obj_progress_data()],
                          'toggle_with_bias': [*self.game_mode.get_toggle_with_bias_data()],
                          'toggle': self.game_mode.get_toggle_progress_data(),
                          'foreground': [],
                          'user_info': [],
                          'game_sys_info': {}}

        return scene_progress

    def get_obj_progress_data(self):
        obj_list = []
        for sprites in self.game_mode.obj_list:
            obj_list.extend(get_sprites_progress_data(sprites))
        obj_list.extend(self.game_mode.obj_rect_list)
        return obj_list

    def get_game_result(self):
        """
        Get the src result for the web
        """
        self.rank()
        return {"frame_used": self.frame_count,
                "state": self.game_result_state,
                "attachment": self.attachements
                }

    def is_running(self):
        return self.game_mode.status == GameStatus.GAME_ALIVE

    def rank(self):
        self.game_result_state = self.game_mode.state
        self.attachements = self.game_mode.get_player_result()
        return self.attachements

    def handle_event(self, commands):
        if ["DEBUG"] in commands.values():
            self.is_debug = not self.is_debug
        if ["PAUSED"] in commands.values():
            self.is_paused = not self.is_paused

    def set_game_mode(self):
        sound_path = ""
        if self.is_sound:
            sound_path = SOUND_DIR
        play_rect_area = pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT)
        game_mode = TeamBattleMode(self.green_team_num, self.blue_team_num, self.is_manual, self.frame_limit, sound_path, play_rect_area)
        return game_mode
