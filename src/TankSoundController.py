from os import path

from GameFramework.sound_controller import SoundController
from games.TankMan.src.env import SOUND_DIR


class TankSoundController(SoundController):
    def __init__(self, is_sound: bool):
        super().__init__(is_sound)
        self.bgm_path = path.join(SOUND_DIR, "BGM.ogg")
        self.shoot_path = path.join(SOUND_DIR, "shoot.wav")
        self.touch_path = path.join(SOUND_DIR, "touch.wav")

    def play_bgm(self):
        self.play_music(self.bgm_path, 0.2)

    def play_shoot_sound(self):
        self.play_sound(self.shoot_path, 0.6, -1)

    def play_touch_sound(self):
        self.play_sound(self.touch_path, 0.6, -1)


