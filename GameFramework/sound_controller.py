import pygame.mixer

from games.PacMan.src.env import *


class SoundController:
    def __init__(self, is_sound: bool):
        self.is_sound = is_sound

    def play_music(self, music_path: str, volume: float):
        if self.is_sound:
            pygame.mixer.init()
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)

    def play_sound(self, music_path: str, volume: float, max_frame: int):
        pygame.mixer.init()
        if self.is_sound:
            pygame.mixer.Sound(music_path).play(maxtime=max_frame).set_volume(volume)
