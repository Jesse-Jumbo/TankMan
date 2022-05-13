import pygame.event

from mlgame.gamedev.game_interface import GameResultState, GameStatus
from .DataCreator import DataCreator
from .TankManMap import TankManMap
from .env import *


class GameMode:
    def __init__(self, map_path: str, time_limit: int, is_sound: bool):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.map_path = map_path
        self.frame_limit = time_limit * FPS
        # control variables
        self.is_sound = is_sound
        self.is_paused = False
        # initialize sprites group
        self.all_sprites = pygame.sprite.Group()
        # initialize map
        self.map = TankManMap(self.map_path)
        # Game attribute
        self.used_frame = 0
        self.state = GameResultState.FAIL
        self.status = GameStatus.GAME_ALIVE
        self.data_creator = DataCreator()

    def get_result(self) -> list:
        res = [{"1P": {}}]
        return res

    def update(self, command: dict):
        self.check_events()
        self.status = GameStatus.GAME_ALIVE
        if not self.is_paused:
            self.used_frame += 1
            self.all_sprites.update()
            self.check_collisions()

            if self.used_frame > self.frame_limit:
                self.reset()

    def reset(self):
        """
        Determine the game result state and status
        """

    def check_events(self):
        """
        add all key events
        """
        cmd_1P = ""
        return {"1P": cmd_1P}

    def check_collisions(self):
        pass

    def play_music(self, music_path: str, volume: float):
        pygame.mixer.init()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

    def play_sound(self, music_path: str, volume: float, max_time: int):
        pygame.mixer.Sound(music_path).play(maxtime=max_time).set_volume(volume)

    def draw_sprite_data(self):
        """
        Draw pictures in the order in which they were added
        all_sprite_data = [{"_id": "", "x": 0, "y": 0, "width": 0, "height": 0, "angle": 0}]
        """
        all_sprite_data = [{"_id": "", "x": 0, "y": 0, "width": 0, "height": 0, "angle": 0}]
        return all_sprite_data

    def create_init_image_data(self):
        """
        all_init_image_data = [{"_id": "", "width": 0, "height": 0, "path": "", "url": ""}]
        """
        all_init_image_data = [{"_id": "", "width": 0, "height": 0, "path": "", "url": ""}]
        return all_init_image_data

    def draw_text_data(self):
        """
        all_text_data = [{"content": "", "x": 0, "y": 0, "color": "", "font_style": "30px Arial"}]
        """
        all_text_data = [{"content": "", "x": 0, "y": 0, "color": "", "font_style": "30px Arial"}]
        return all_text_data

    def create_scene_info(self):
        """
        scene_info = {"frame": self.used_frame,
                      "status": self.status,
                      "background": [WIDTH, HEIGHT],
                      "game_result": self.get_result(),
                      "state": self.state}

        """
        scene_info = {"frame": self.used_frame,
                      "status": self.status,
                      "background": [WIDTH, HEIGHT],
                      "game_result": self.get_result(),
                      "state": self.state}
        return scene_info

    def create_game_data_to_player(self):
        """
        add all required information for player training
        to_player_data = {"1P": {"player_id": "1P",
                                 "x": 0,
                                 "y": 0,
                                 "used_frame": self.used_frame,
                                 "status": self.status},
                          "2P": {}}
        """
        to_player_data = {"1P": {"player_id": "1P",
                                 "x": 0,
                                 "y": 0,
                                 "used_frame": self.used_frame,
                                 "status": self.status},
                          "2P": {}}
        return to_player_data
