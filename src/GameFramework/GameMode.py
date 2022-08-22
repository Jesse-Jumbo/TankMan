import pygame.event
from mlgame.game.paia_game import GameResultState, GameStatus

from mlgame.view.view_model import create_image_view_data
from .constants import ID, X, Y, WIDTH, HEIGHT, ANGLE
from .SoundController import SoundController

from .TiledMap import TiledMap

class GameMode:
    _ID = ID
    _X = X
    _Y = Y
    _WIDTH = WIDTH
    _HEIGHT = HEIGHT
    _ANGLE = ANGLE

    def __init__(self, user_num: int, map_path: str, frame_limit: int, is_sound: bool):
        self._user_num = user_num
        self.map_path = map_path
        self.frame_limit = frame_limit
        self.sound_controller = SoundController(is_sound)
        self.is_paused = False
        self.is_debug = False
        self.all_sprites = pygame.sprite.Group()
        self.map = TiledMap(self.map_path)
        self.used_frame = 0
        self.state = GameResultState.FAIL
        self.status = GameStatus.GAME_ALIVE
        self.players = pygame.sprite.Group()
        self.map_width = self.map.map_width
        self.map_height = self.map.map_height

    # TODO refactor result info and position
    def get_result(self) -> list:
        """Define the end of game will return the player's info for user"""
        res = []
        for player in self.players:
            get_res = player.get_result()
            get_res = self.get_other_result(get_res)
            get_res["state"] = self.state
            get_res["status"] = self.status
            res.append(get_res)
        return res

    def get_other_result(self, origin_result):
        """You can overwrite or append new result to origin result, when you finished, return origin_result"""
        return origin_result

    def update_game_mode(self, command: dict):
        self.set_result(GameResultState.FAIL, GameStatus.GAME_ALIVE)
        if not self.is_paused:
            self.used_frame += 1
            number = 1
            for player in self.players:
                player.update(command[f"{number}P"])
                number += 1
                # TODO refactor reset method
                if not player.is_alive or self.used_frame >= self.frame_limit:
                    self.reset()
            self.check_collisions()

    def reset(self):
        """
        Judge rur self.reset() should in what situation
        """
        print("please overwrite 'self.check_game_is_end' method")

    def set_result(self, state: str, status: str):
        self.state = state
        self.status = status

    def get_act_command(self):
        """
        Define you want add all key events
        return {"1P": cmd_1P}
        """
        print("please overwrite 'self.check_events' method")

    def check_collisions(self):
        pass

    def draw_players(self):
        player_data = []
        for player in self.players:
            data = player.get_image_data()
            player_data.append(create_image_view_data(data[self._ID], data[self._X], data[self._Y],
                                                      data[self._WIDTH], data[self._HEIGHT],
                                                      data[self._ANGLE]))

        return player_data

    def draw_sprite_data(self):
        """
        Draw pictures in the order in which they were added
        example:
        all_sprite_data = [{"id": "", "x": 0, "y": 0, "width": 0, "height": 0, "angle": 0}]
        return all_sprite_data
        """
        print("please overwrite 'self.draw_sprite_data' method")

    def create_init_image_data(self):
        """
        Add all image in game
        example:
        all_init_image_data = [{"id": "", "width": 0, "height": 0, "path": "", "url": ""}]
        return all_init_image_data
        """
        print("please overwrite 'self.create_init_image_data' method")

    def draw_foreground_data(self):
        """
        Example:
        all_foreground_data = [{"content": "", "x": 0, "y": 0, "color": "", "font_style": "24px Arial"}]
        return all_foreground_data
        """
        print("Please overwrite 'self.draw_foreground_data' method")

    def draw_toggle_data(self):
        """
        Example:
        all_toggle_data = [{"content": "", "x": 0, "y": 0, "color": "", "font_style": "24px Arial"}]
        return all_toggle_data
        """
        print("Please overwrite 'self.draw_toggle_data' method")

    def create_scene_info(self):
        """
        Example:
        scene_info = {"frame": self.used_frame,
                      "status": self.status,
                      "background": [WINDOW_WIDTH, WINDOW_HEIGHT],
                      "game_result": self.get_result(),
                      "state": self.state}
        return scene_info
        """
        print("Please overwrite 'self.create_scene_info' method")

    def create_game_data_to_player(self):
        """
        add all required information for player training
        Example:
        to_player_data = {"1P": {"player_id": "1P",
                                 "x": 0,
                                 "y": 0,
                                 "used_frame": self.used_frame,
                                 "status": self.status},
                          "2P": {}}
        return to_player_data
        """
        print("Please overwrite 'self.create_game_to_player' method")
