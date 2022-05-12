from mlgame.gamedev.game_interface import PaiaGame, GameStatus
from mlgame.view.test_decorator import check_game_result
from mlgame.view.view_model import create_text_view_data, create_asset_init_data, create_image_view_data, \
    Scene
from .BattleMode import BattleMode
from .sound_controller import *

'''need some fuction same as arkanoid which without dash in the name of fuction'''


class TankMan(PaiaGame):
    def __init__(self, map_no: int, time_limit: int, sound: str):
        super().__init__()
        self.scene = Scene(WIDTH, HEIGHT, BLACK)
        self.map_path = path.join(MAP_DIR, f"map_0{map_no}.tmx")
        self.time_limit = time_limit
        if sound == "on":
            self.is_sound = True
        else:
            self.is_sound = False
        self.game_mode = self.set_game_mode()
        self.attachements = []

    def game_to_player_data(self) -> dict:
        return self.game_mode.create_game_data_to_player()

    @property
    def get_scene_info(self):
        """
        Get the scene information
        """
        scene_info = self.game_mode.create_scene_info()
        return scene_info

    def update(self, commands: dict):
        self.frame_count += 1
        self.game_mode.update(commands)
        if not self.is_running():
            self.rank()
            return "RESET"

    def reset(self):
        self.frame_count = 0
        self.game_mode = self.set_game_mode()
        self.rank()

    def is_running(self):
        if self.game_mode.status == GameStatus.GAME_ALIVE:
            return True
        else:
            return False

    def get_scene_init_data(self) -> dict:
        """
        Get the scene and object information for drawing on the web
        """
        game_info = {'scene': self.scene.__dict__,
                     'assets': []}

        images_init_data = self.game_mode.create_init_image_data()
        for image_init_data in images_init_data:
            obj_init = create_asset_init_data(image_init_data["_id"], image_init_data["width"],
                                              image_init_data["height"],
                                              image_init_data["path"], image_init_data["url"])
            game_info["assets"].append(obj_init)

        return game_info

    # @check_game_progress
    def get_scene_progress_data(self) -> dict:
        """
        Get the position of src objects for drawing on the web
        """

        game_progress = {'background': [],
                         'object_list': [],
                         'toggle': [],
                         'foreground': [],
                         'user_info': [],
                         'game_sys_info': {}}

        images_data = self.game_mode.draw_sprite_data()
        for image_data in images_data:
            obj = create_image_view_data(image_data["_id"], image_data["x"], image_data["y"],
                                         image_data["width"], image_data["height"], image_data["angle"])
            game_progress["object_list"].append(obj)

        all_text_data = self.game_mode.draw_text_data()
        for text_data in all_text_data:
            text = create_text_view_data(text_data["content"], text_data["x"], text_data["y"],
                                         text_data["color"], text_data["font_style"])
            game_progress["foreground"].append(text)

        return game_progress

    @check_game_result
    def get_game_result(self):
        """
        Get the src result for the web
        """

        return {"frame_used": self.frame_count,
                "state": self.game_result_state,
                "attachment": self.rank()
                }

    def get_keyboard_command(self):
        """
        Get the command according to the pressed keys
        """
        # 此處回傳的資料 要與 ml_play.py 一致

        if not self.is_running():
            return {"1P": "RESET",
                    "2P": "RESET",
                    }

        return self.game_mode.check_events()

    @staticmethod
    def ai_clients():
        """
        let MLGame know how to parse your ai,
        you can also use this names to get different cmd and send different data to each ai client
        """
        return [{"name": "1P"}, {"name": "2P"}]

    def set_game_mode(self):
        game_mode = BattleMode(self.map_path, self.time_limit, self.is_sound)
        return game_mode

    def rank(self):
        self.game_result_state = self.game_mode.state
        self.attachements = self.game_mode.get_result()
        return self.attachements
