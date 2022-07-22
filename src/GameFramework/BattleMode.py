from mlgame.game.paia_game import GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name

from .GameMode import GameMode


class BattleMode(GameMode):
    def __init__(self, user_num:int, map_path: str, frame_limit: int, is_sound: bool):
        super().__init__(user_num, map_path, frame_limit, is_sound)
    def reset(self):
        if self.player_1P.is_alive and not self.player_2P.is_alive:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_1P_WIN)
        elif not self.player_1P.is_alive and self.player_2P.is_alive:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_2P_WIN)
        else:
            self.reset_2()

    def get_act_command(self):
        """
        Define the action represented by the key
        (1) press to execute
        key_pressed_list = pygame.key.get_pressed()
        (2)
        get key to execute
        for even in pygame.event.get():
            pass
        """
        ai_1P = get_ai_name[0]
        ai_2P = get_ai_name[1]
        cmd_1P = self.get_1P_command()
        cmd_2P = self.get_2P_command()

        return {ai_1P: cmd_1P, ai_2P: cmd_2P}

    def get_1P_command(self):
        """
        Define command to control 1P
        """
        print("Please overwrite 'self.get_1P_command()' method")
        return

    def get_2P_command(self):
        """
        Define command to control 1P
        """
        print("Please overwrite 'self.get_2P_command()' method")
        return

    def get_scene_info(self):
        scene_info = {"frame": self.used_frame,
                      "status": self.status,
                      "background": [1320, 660],
                      "1P_xy_pos": self.player_1P.get_xy_pos(),
                      "2P_xy_pos": self.player_2P.get_xy_pos(),
                      "game_result": self.get_result(),
                      "state": self.state}

        return scene_info

    def reset_2(self):
        pass
