import pygame.event

from games.TankMan.GameFramework.GameMode import GameMode
from games.TankMan.GameFramework.Player import Player
from games.TankMan.GameFramework.constants import ID, X, Y, WIDTH, HEIGHT, ANGLE
from games.TankMan.src.collide_hit_rect import *
from games.TankMan.src.env import *
from mlgame.gamedev.game_interface import GameResultState, GameStatus
from mlgame.view.view_model import create_image_view_data


class BattleMode(GameMode):
    def __init__(self, map_path: str, time_limit: int, is_sound: bool):
        super().__init__(map_path, time_limit, is_sound)
        self.players = pygame.sprite.Group()

    # TODO refactor result info and position
    def get_result(self) -> list:
        """Define the end of game will return the player's info for user"""
        res = []
        for player in self.players:
            res.append(player.get_info())
        return res

    def update_game_mode(self, command: dict):
        c = 1
        for player in self.players:
            player.update(command[f"{c}P"])
            c = 2
            if not player.is_alive:
                self.reset()
        self.update_game()

    def update_game(self):
        """Define update of this template's child"""
        print("please overwrite 'self.update_game' method")

    def check_game_is_end(self):
        # TODO how better
        if self.player_1P.is_alive and not self.player_2P.is_alive:
            self.reset(GameResultState.FINISH, GameStatus.GAME_1P_WIN)
        elif not self.player_1P.is_alive and self.player_2P.is_alive:
            self.reset(GameResultState.FINISH, GameStatus.GAME_2P_WIN)
        elif self.player_1P.score > self.player_2P.score:
            self.reset(GameResultState.FAIL, GameStatus.GAME_1P_WIN)
        elif self.player_1P.score < self.player_2P.score:
            self.reset(GameResultState.FAIL, GameStatus.GAME_2P_WIN)
        else:
            self.reset(GameResultState.FAIL, GameStatus.GAME_OVER)
        self.reset_game_mode()

    def check_events(self):
        """
        Define the action represented by the key
        (1) press to execute
        key_pressed_list = pygame.key.get_pressed()
        (2)
        get key to execute
        for even in pygame.event.get():
            pass
        """
        cmd_1P = self.get_1P_command()
        cmd_2P = self.get_2P_command()

        return {"1P": cmd_1P, "2P": cmd_2P}

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

    def check_collisions(self):
        pass

    def draw_sprite_data(self):
        """
        Draw pictures in the order in which they were added
        """
        print("please overwrite 'self.draw_sprite_data' method")

    def draw_players(self):
        # TODO need?
        player_data = []
        for player in self.players:
            if isinstance(player, Player):
                data = player.get_image_data()
                player_data.append(create_image_view_data(data[ID], data[X], data[Y], data[WIDTH], data[HEIGHT],
                                                          data[ANGLE]))

        return player_data

    def create_init_image_data(self):
        """
        Example:
        all_init_image_data = []
        for _id, img_path in PLAYER_IMG_PATH_DICT.items():
            all_init_image_data.append(create_asset_init_data(_id, TILE_X_SIZE, TILE_Y_SIZE,
                                                              img_path, PLAYER_URL[_id]))

        return all_init_image_data
        """
        print("please overwrite 'self.create_init_image_data' method")

    def draw_text_data(self):
        """
        all_text_data = []
        Example: all_text_data.append(create_text_view_data("Hello World", WIDTH_CENTER - 45, HEIGHT_CENTER, WHITE, "30px Arial"))
        return all_text_data
        """
        print("Please overwrite 'self.draw_text_data' method")

    def create_scene_info(self):
        """
        Example:
            self.get_scene_info()
        """
        print("Please overwrite 'self.draw_text_data' method")

    def get_scene_info(self):
        scene_info = {"frame": self.used_frame,
                      "status": self.status,
                      "background": [WINDOW_WIDTH, WINDOW_HEIGHT],
                      "1P_xy_pos": self.player_1P.get_xy_pos(),
                      "2P_xy_pos": self.player_2P.get_xy_pos(),
                      "game_result": self.get_result(),
                      "state": self.state}

        return scene_info

    def create_game_data_to_player(self):
        """
        Example:
        to_player_data = {}
        for player in self.players:
            if isinstance(player, Player):
                info = player.get_info()
                info["used_frame"] = self.used_frame
                info["status"] = self.status
                to_player_data[f"{player._id}P"] = info

        return to_player_data
        """
        print("Please overwrite 'self.create_game_data_to_player' method")

    def reset_game_mode(self):
        pass
