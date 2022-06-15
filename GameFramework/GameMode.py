import pygame.event

from mlgame.view.view_model import create_image_view_data
from .constants import ID, X, Y, WIDTH, HEIGHT, ANGLE
from .sound_controller import SoundController
from mlgame.gamedev.game_interface import GameResultState, GameStatus

from .TiledMap import TiledMap
from games.TankMan.src.env import *


class GameMode:
    _ID = ID
    _X = X
    _Y = Y
    _WIDTH = WIDTH
    _HEIGHT = HEIGHT
    _ANGLE = ANGLE

    def __init__(self, map_path: str, time_limit: int, is_sound: bool):
        self.map_path = map_path
        self.frame_limit = time_limit * FPS
        self.sound_controller = SoundController(is_sound)
        self.is_paused = False
        self.is_debug = False
        self.all_sprites = pygame.sprite.Group()
        self.map = TiledMap(self.map_path)
        self.used_frame = 0
        self.state = GameResultState.FAIL
        self.status = GameStatus.GAME_ALIVE
        self.players = pygame.sprite.Group()

    # TODO refactor result info and position
    def get_result(self) -> list:
        """Define the end of game will return the player's info for user"""
        res = []
        for player in self.players:
            get_res = player.get_result()
            get_res["state"] = self.state
            get_res["status"] = self.status
            res.append(get_res)
        return res

    def update_game_mode(self, command: dict):
        self.set_result(GameResultState.FAIL, GameStatus.GAME_ALIVE)
        if not self.is_paused:
            self.used_frame += 1
            self.all_sprites.update()
            number = 1
            for player in self.players:
                player.update(command[f"{number}P"])
                number += 1
                if not player.is_alive or self.used_frame > self.frame_limit:
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

    def draw_text_data(self):
        """
        Example:
        all_text_data = [{"content": "", "x": 0, "y": 0, "color": "", "font_style": "30px Arial"}]
        return all_text_data
        """
        print("Please overwrite 'self.draw_text_data' method")

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
