import pygame.event

from games.TankMan.src.Player import Player
from mlgame.gamedev.game_interface import GameResultState, GameStatus
from .GameMode import GameMode
from .collide_hit_rect import *
from .env import *


class BattleMode(GameMode):
    def __init__(self, map_path: str, time_limit: int, is_sound: bool):
        super().__init__(map_path, time_limit, is_sound)
        # control variables
        self.is_debug = False
        # initialize sprites group
        self.players = pygame.sprite.Group()

        # init players
        players = self.map.create_obj_init_data(PLAYER_IMG_NO_LIST)
        # TODO how better
        for player in players:
            if player["_id"] == 1:
                self.player_1P = Player(1, player["x"], player["y"], player["width"], player["height"])
            else:
                self.player_2P = Player(2, player["x"], player["y"], player["width"], player["height"])
        self.players.add(self.player_1P, self.player_2P)

    def get_result(self) -> list:
        res = [{"1P": self.player_1P.get_info()},
               {"2P": self.player_2P.get_info()}]
        return res

    def update(self, command: dict):
        super().update(command)
        if not self.is_paused:
            self.player_1P.update(command["1P"])
            self.player_2P.update(command["2P"])
            if not self.player_1P.is_alive or not self.player_2P.is_alive:
                self.reset()

    def reset(self):
        if self.player_1P.is_alive and not self.player_2P.is_alive:
            self.status = GameStatus.GAME_1P_WIN
            self.state = GameResultState.FINISH
        elif not self.player_1P.is_alive and self.player_2P.is_alive:
            self.status = GameStatus.GAME_2P_WIN
            self.state = GameResultState.FINISH
        else:
            self.status = GameStatus.GAME_OVER
            self.state = GameResultState.FAIL

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
        cmd_1P = ""
        cmd_2P = ""

        return {"1P": cmd_1P, "2P": cmd_2P}

    def check_collisions(self):
        pass

    def draw_sprite_data(self):
        """
        Draw pictures in the order in which they were added
        """
        all_sprite_data = []
        for player in self.players:
            if isinstance(player, Player):
                all_sprite_data.append(player.get_image_data())

        return all_sprite_data

    def create_init_image_data(self):
        all_init_image_data = []
        c = 1
        for img_path in PLAYER_IMG_PATH_LIST:
            all_init_image_data.append(self.data_creator.create_image_init_data(f"{c}P", TILE_X_SIZE, TILE_Y_SIZE,
                                                                                img_path, PLAYER_URL[f"{c}P"]))
            c += 1

        return all_init_image_data

    def draw_text_data(self):
        all_text_data = []
        all_text_data.append(self.data_creator.create_text_data(f"1P_Score: {self.player_1P.score}",
                                                                WIDTH_CENTER + WIDTH_CENTER // 2 - 45, 0, WHITE,
                                                                "30px Arial"))
        all_text_data.append(self.data_creator.create_text_data(f"2P_Score: {self.player_2P.score}",
                                                                WIDTH_CENTER // 2 - 45, 0, WHITE, "30px Arial"))
        all_text_data.append(self.data_creator.create_text_data(f"Time: {self.used_frame // 60}", WIDTH - 100, 0, WHITE,
                                                                "30px Arial"))
        all_text_data.append(self.data_creator.create_text_data(f"2P Lives: {self.player_2P.lives}", 5, HEIGHT - 35,
                                                                WHITE, "30px Arial"))
        all_text_data.append(self.data_creator.create_text_data(f"1P Lives: {self.player_2P.lives}", WIDTH_CENTER + 200,
                                                                HEIGHT - 35, WHITE, "30px Arial"))
        return all_text_data

    def create_scene_info(self):
        scene_info = {"frame": self.used_frame,
                      "status": self.status,
                      "background": [WIDTH, HEIGHT],
                      "walls_xy_pos": [],
                      "1P_xy_pos": self.player_1P.get_xy_pos(),
                      "2P_xy_pos": self.player_2P.get_xy_pos(),
                      "game_result": self.get_result(),
                      "state": self.state}

        return scene_info

    def create_game_data_to_player(self):
        to_player_data = {}
        for player in self.players:
            if isinstance(player, Player):
                info = player.get_info()
                info["used_frame"] = self.used_frame
                info["status"] = self.status
                to_player_data[f"{player._no}P"] = info

        return to_player_data
