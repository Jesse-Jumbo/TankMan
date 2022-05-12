import pygame.event

from mlgame.gamedev.game_interface import GameResultState, GameStatus
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
        return self.status, self.state

    def check_events(self):
        pass

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
        pass

    def create_init_image_data(self):
        pass

    def draw_text_data(self):
        pass
