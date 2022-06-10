from mlgame.gamedev.game_interface import PaiaGame, GameStatus
from mlgame.view.test_decorator import check_game_result
from mlgame.view.view_model import Scene

'''need some fuction same as arkanoid which without dash in the name of fuction'''


class GameFramework(PaiaGame):
    def __init__(self, map_no: int, time_limit: int, sound: str):
        super().__init__()
        self.scene = Scene(0, 0, "#000000")
        self.map_name = f"map_0{map_no}.tmx"
        self.time_limit = time_limit
        if sound == "on":
            self.is_sound = True
        else:
            self.is_sound = False
        self.game_mode = None
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
                     'assets': self.game_mode.create_init_image_data()}

        return game_info

    # @check_game_progress
    def get_scene_progress_data(self) -> dict:
        """
        Get the position of src objects for drawing on the web
        """

        game_progress = {'background': [],
                         'object_list': self.game_mode.draw_sprite_data(),
                         'toggle_with_bias': [],
                         'toggle': [],
                         'foreground': self.game_mode.draw_text_data(),
                         'user_info': [],
                         'game_sys_info': {}}

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
            reset_dict = {}
            for i in range(1, len(self.game_mode.playes)+1):
                reset_dict[f"{i}P"] = "RESET"
            return reset_dict

        return self.game_mode.get_act_command()

    @staticmethod
    def ai_clients():
        """
        let MLGame know how to parse your ai,
        you can also use this names to get different cmd and send different data to each ai client
        """
        return [{"name": "1P", "args": ("1P",)}, {"name": "2P", "args": ("2P",)},
                {"name": "3P", "args": ("3P",)}, {"name": "4P", "args": ("4P",)}]

    def set_game_mode(self):
        print("please overwrite 'self.set_game_mode' method")
        """
        Example:
        game_mode = GameMode(self.map_name, self.time_limit, self.is_sound)
        return game_mode
        """
    def rank(self):
        self.game_result_state = self.game_mode.state
        self.attachements = self.game_mode.get_result()
        return self.attachements
