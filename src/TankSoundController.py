from os import path

from GameFramework.sound_controller import SoundController
from games.TankMan.src.env import SOUND_DIR


class TankSoundController(SoundController):
    BGM_PATH = path.join(SOUND_DIR, "BGM.ogg")
    SHOOT_PATH = path.join(SOUND_DIR, "shoot.wav")
    TOUCH_PATH = path.join(SOUND_DIR, "touch.wav")

    def play_bgm(self):
        self.play_music(self.BGM_PATH, 0.2)

    def play_shoot_sound(self):
        self.play_sound(self.SHOOT_PATH, 0.6, -1)

    def play_touch_sound(self):
        self.play_sound(self.TOUCH_PATH, 0.6, -1)


