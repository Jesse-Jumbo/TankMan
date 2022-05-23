import pygame.event

from .sound_controller import SoundController
from mlgame.gamedev.game_interface import GameResultState, GameStatus

from .TiledMap import TiledMap
from games.TankMan.src.env import *


class GameMode:
    def __init__(self, map_path: str, time_limit: int, is_sound: bool):
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
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

    def get_result(self) -> list:
        """Define the end of game will return the player's info for user
        res = [{"1P": {}}]
        return res
        """
        print("please overwrite 'self.get_result' method")

    def update(self, command: dict):
        self.check_events()
        if not self.is_paused:
            self.used_frame += 1
            self.all_sprites.update()
            self.check_collisions()

            if self.used_frame > self.frame_limit:
                self.reset()
            self.update_game_mode(command)

    def update_game_mode(self, command: dict):
        """Define belong to the children update"""
        print("please overwrite 'self.update_game' method")

    def reset(self):
        """
        Determine the game result state and status
        """
        print("please overwrite 'self.reset' method")

    def check_events(self):
        """
        Define you want add all key events
        return {"1P": cmd_1P}
        """
        print("please overwrite 'self.check_events' method")

    def check_collisions(self):
        pass

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
