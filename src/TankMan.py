import ntpath
import pygame
from mlgame.gamedev.game_interface import PaiaGame, GameStatus
from mlgame.view.test_decorator import check_game_result
from mlgame.view.view_model import create_text_view_data, create_asset_init_data, create_image_view_data, \
    Scene
from .GameMode import GameMode
from .sound_controller import *

'''need some fuction same as arkanoid which without dash in the name of fuction'''


class TankMan(PaiaGame):
    def __init__(self, map_no: int, sound: str):
        super().__init__()
        self.scene = Scene(WIDTH, HEIGHT, BLACK)
        self.is_sound = sound
        # self.sound_controller = SoundController(self.is_sound)
        self.map = ntpath.join(MAP_DIR, f"map_0{map_no}.tmx")
        self.game_mode = self.set_game_mode(self.map)
        self.attachements = []

    def game_to_player_data(self) -> dict:
        scene_info = self.get_scene_info
        to_player_data = {}
        for player in self.game_mode.players:
            player_data = player.get_info()
            player_data["frame"] = scene_info["frame"]
            player_data["status"] = scene_info["status"]
            player_data["mobs_pos"] = []
            player_data["walls_pos"] = []

            for wall in self.game_mode.walls:
                player_data["walls_pos"].append(wall.pos)

            to_player_data[player_data['player_id']] = player_data

        if to_player_data:
            return to_player_data
        else:
            return {
                "1P": scene_info,
                "2P": scene_info,
                "3P": scene_info,
                "4P": scene_info
            }

    @property
    def get_scene_info(self):
        """
        Get the scene information
        """
        scene_info = {'frame': self.game_mode.frame,
                      'status': self.game_mode.status,
                      'background': [WIDTH, HEIGHT],
                      'walls_pos': [],
                      'game_result': self.game_mode.get_result(),
                      'state': self.game_mode.state}

        for player in self.game_mode.players:
            scene_info[f"{player._no}P_pos"] = player.pos
        for wall in self.game_mode.walls:
            scene_info["walls_pos"].append(wall.pos)
        return scene_info

    def update(self, commands: dict):
        self.frame_count += 1
        self.game_mode.run(commands)
        if not self.is_running():
            return "RESET"

    def reset(self):
        self.frame_count = 0
        self.game_mode = self.set_game_mode(self.map)
        # self.game_mode.sound_controller.player_music()

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

        # initialize bullets image
        game_info["assets"].append(create_asset_init_data("bullets", TILE_X_SIZE, TILE_Y_SIZE
                                                          , BULLET_IMG_PATH, ""))
        # initialize player image
        for player in self.game_mode.players:
            game_info['assets'].append(create_asset_init_data(f'{player._no}P', TILE_X_SIZE, TILE_Y_SIZE
                                                              , player.img_path, ""))
        # initialize walls image
        for wall in self.game_mode.walls:
            game_info["assets"].append(create_asset_init_data("walls", TILE_X_SIZE, TILE_Y_SIZE
                                                              , WALL_IMG_PATH, ""))

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

        # update bullet image
        for bullet in self.game_mode.bullets:
            bullet_obj = create_image_view_data('bullets', bullet.rect.x, bullet.rect.y,
                                                bullet.rect.width, bullet.rect.height, bullet.angle)
            game_progress["object_list"].append(bullet_obj)
        # update player image
        for player in self.game_mode.players:
            player_obj = create_image_view_data(f'{player._no}P', player.rect.x, player.rect.y,
                                                TILE_X_SIZE, TILE_Y_SIZE, player.angle)
            game_progress["object_list"].append(player_obj)
        # update walls image
        for wall in self.game_mode.walls:
            game_progress["object_list"].append(create_image_view_data('walls', wall.rect.x, wall.rect.y,
                                                                       TILE_X_SIZE, TILE_Y_SIZE))
        # update 1P score text
        game_progress["foreground"].append(create_text_view_data(f"1P_Score: {self.game_mode.player_1P.score}",
                                                                 WIDTH / 2 - 30, 0, WHITE, "20px Arial"))
        # update 1P score text
        game_progress["foreground"].append(create_text_view_data(f"2P_Score: {self.game_mode.player_2P.score}",
                                                                 WIDTH / 2 - 30, HEIGHT - 25, WHITE, "20px Arial"))
        # update frame text
        game_progress["foreground"].append(create_text_view_data(f"Time: {(self.game_mode.frame // 60)}",
                                                                 WIDTH - 90, 0, WHITE, "20px Arial"))
        # update 1P live text
        game_progress["foreground"].append(create_text_view_data(f"1P live: {self.game_mode.player_1P.live}",
                                                                 WIDTH - 90, HEIGHT - 25, WHITE, "20px Arial"))
        # update 2P live text
        game_progress["foreground"].append(create_text_view_data(f"2P live: {self.game_mode.player_2P.live}",
                                                                 5, HEIGHT - 25, WHITE, "20px Arial"))

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
        # TODO 此處回傳的資料 要與 ml_play.py 一致
        cmd_1P = ""
        cmd_2P = ""
        cmd_3P = ""
        cmd_4P = ""

        key_pressed_list = pygame.key.get_pressed()
        if key_pressed_list[pygame.K_UP]:
            cmd_1P = FORWARD_CMD
        elif key_pressed_list[pygame.K_DOWN]:
            cmd_1P = BACKWARD_CMD

        if key_pressed_list[pygame.K_w]:
            cmd_2P = FORWARD_CMD
        elif key_pressed_list[pygame.K_s]:
            cmd_2P = BACKWARD_CMD

        if key_pressed_list[pygame.K_SPACE]:
            cmd_1P = SHOOT
        if key_pressed_list[pygame.K_f]:
            cmd_2P = SHOOT

        for even in pygame.event.get():
            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_RIGHT:
                    cmd_1P = RIGHT_CMD
                elif even.key == pygame.K_LEFT:
                    cmd_1P = LEFT_CMD

                if even.key == pygame.K_d:
                    cmd_2P = RIGHT_CMD
                elif even.key == pygame.K_a:
                    cmd_2P = LEFT_CMD

        if not self.is_running():
            return {"1P": "RESET",
                    "2P": "RESET",
                    "3P": "RESET",
                    "4P": "RESET",
                    }

        return {"1P": cmd_1P,
                "2P": cmd_2P,
                "3P": cmd_3P,
                "4P": cmd_4P,
                }

    @staticmethod
    def ai_clients():
        """
        let MLGame know how to parse your ai,
        you can also use this names to get different cmd and send different data to each ai client
        """
        return [
            {"name": "1P"},
            {"name": "2P"},
            {"name": "3P"},
            {"name": "4P"}
        ]

    def set_game_mode(self, map_name: str):
        game_mode = GameMode(map_name)
        return game_mode

    def rank(self):
        self.game_result_state = self.game_mode.state
        game_result = self.game_mode.get_result()
        self.attachements = game_result
        return self.attachements
