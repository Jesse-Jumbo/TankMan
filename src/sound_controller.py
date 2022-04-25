from os import path
import pygame
from .env import *


class SoundController:
    def __init__(self, is_sound_on: str):
        if is_sound_on == "on":
            self.is_sound_on = True
            try:
                pygame.mixer.init()
                self.warn_sound = pygame.mixer.Sound(path.join(SOUND_DIR, "count_time.mp3"))
            except Exception as e:
                self.is_sound_on = False
                print(f"sound_error:{e}")
        else:
            self.is_sound_on = False

    def play_normal_music(self):
        if self.is_sound_on:
            pass
        else:
            pass
