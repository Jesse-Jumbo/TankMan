import random

import pygame.event
import pygame.event
from mlgame.game.paia_game import GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name
from mlgame.view.view_model import create_asset_init_data, create_text_view_data, \
    create_rect_view_data, create_line_view_data
from mlgame.view.view_model import create_image_view_data

from src.game_module.SoundController import create_sounds_data, create_bgm_data, SoundController
from src.game_module.TiledMap import create_construction, TiledMap
from .Bullet import Bullet
from .Player import Player
from .Station import Station
from .Wall import Wall
from .collide_hit_rect import *
from .env import *
from .game_module.fuctions import set_topleft, add_score, set_shoot, get_sprites_progress_data


class BattleMode:
    def __init__(self, is_manual: bool, map_path: str, frame_limit: int, sound_path: str, play_rect_area: pygame.Rect):
        # init game
        pygame.init()
        self._user_num = 2
        self.sound_path = sound_path
        self.map_path = map_path
        self.map = TiledMap(self.map_path)
        self.scene_width = self.map.map_width
        self.scene_height = self.map.map_height + 100
        self.width_center = self.scene_width // 2
        self.height_center = self.scene_height // 2
        self.play_rect_area = play_rect_area
        self.used_frame = 0
        self.state = GameResultState.FAIL
        self.status = GameStatus.GAME_ALIVE
        self.sound_controller = SoundController(sound_path, self.get_sound_data())
        self.sound_controller.play_music(self.get_bgm_data())
        self.frame_limit = frame_limit
        self.is_manual = is_manual
        self.obj_rect_list = []
        # control variables
        self.is_invincible = False
        self.is_through_wall = False
        # initialize sprites group
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.bullet_stations = pygame.sprite.Group()
        self.oil_stations = pygame.sprite.Group()
        # init players
        act_cd = 0
        if self.is_manual:
            act_cd = 10
        # init obj data
        self.map.add_init_obj_data(PLAYER_1_IMG_NO, Player, act_cd=act_cd, play_rect_area=self.play_rect_area)
        self.map.add_init_obj_data(PLAYER_2_IMG_NO, Player, act_cd=act_cd, play_rect_area=self.play_rect_area)
        self.map.add_init_obj_data(WALL_IMG_NO, Wall, margin=8, spacing=8)
        self.map.add_init_obj_data(BULLET_STATION_IMG_NO, Station, margin=2, spacing=2, capacity=5, quadrant=1)
        self.map.add_init_obj_data(OIL_STATION_IMG_NO, Station, margin=2, spacing=2, capacity=30, quadrant=1)
        # create obj
        all_obj = self.map.create_init_obj_dict()
        # init player
        self.player_1P = all_obj[PLAYER_1_IMG_NO][0]
        self.player_2P = all_obj[PLAYER_2_IMG_NO][0]
        self.players.add(self.player_1P, self.player_2P)
        self.all_sprites.add(self.player_1P, self.player_2P)
        # init walls
        self.walls.add(all_obj[WALL_IMG_NO])
        self.all_sprites.add(*self.walls)
        # init bullet stations
        self.bullet_stations.add(all_obj[BULLET_STATION_IMG_NO])
        self.all_sprites.add(*self.bullet_stations)
        # init oil stations
        self.oil_stations.add(all_obj[OIL_STATION_IMG_NO])
        self.all_sprites.add(*self.oil_stations)
        # init pos list
        self.all_pos_list = self.map.all_pos_list
        self.empty_quadrant_pos_dict = self.map.empty_quadrant_pos_dict
        self.background = []
        for pos in self.all_pos_list:
            no = random.randrange(3)
            self.background.append(
                create_image_view_data(f"floor_{no}", pos[0], pos[1], 50, 50, 0))
        self.obj_list = [self.oil_stations, self.bullet_stations, self.bullets, self.players, self.walls]
        self.background.append(create_image_view_data("border", 0, -50, self.scene_width, WINDOW_HEIGHT, 0))

    def update(self, command: dict):
        self.used_frame += 1
        self.check_collisions()
        self.walls.update()
        self.create_bullet(self.players)
        self.bullets.update()
        self.players.update(command)
        self.get_player_end()
        if self.used_frame >= self.frame_limit:
            self.get_game_end()

    def reset(self):
        # reset init game
        self.__init__(self.is_manual, self.map_path, self.frame_limit, self.sound_path, self.play_rect_area)
        # reset player pos
        self.empty_quadrant_pos_dict[1].append(self.player_1P.origin_xy)
        self.empty_quadrant_pos_dict[2].append(self.player_2P.origin_xy)
        set_topleft(self.player_1P,
                    self.empty_quadrant_pos_dict[1].pop(random.randrange(len(self.empty_quadrant_pos_dict[1]))))
        set_topleft(self.player_2P,
                    self.empty_quadrant_pos_dict[2].pop(random.randrange(len(self.empty_quadrant_pos_dict[2]))))

    def get_player_end(self):
        if self.player_1P.is_alive and not self.player_2P.is_alive:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_1P_WIN)
        elif not self.player_1P.is_alive and self.player_2P.is_alive:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_2P_WIN)

    def get_game_end(self):
        score_1P = self.player_1P.score
        score_2P = self.player_2P.score
        if score_1P > score_2P:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_1P_WIN)
        elif score_1P < score_2P:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_2P_WIN)
        else:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_DRAW)

    def set_result(self, state: str, status: str):
        self.state = state
        self.status = status

    def get_player_result(self) -> list:
        """Define the end of game will return the player's info for user"""
        res = []
        for player in self.players:
            if isinstance(player, Player):
                get_res = player.get_info_to_game_result()
                get_res["state"] = self.state
                get_res["status"] = self.status
                get_res["used_frame"] = self.used_frame
                res.append(get_res)
        return res

    def check_collisions(self):
        if not self.is_through_wall:
            collide_with_walls(self.players, self.walls)
        if not self.is_invincible:
            self.add_player_score(collide_with_bullets(self.players, self.bullets)[0])
            # TODO refactor stations
            bs = collide_with_bullet_stations(self.players, self.bullet_stations)
            self.change_obj_pos(bs)
            os = collide_with_oil_stations(self.players, self.oil_stations)
            self.change_obj_pos(os)
        player_id, score = collide_with_bullets(self.walls, self.bullets)
        if player_id == 1:
            add_score(self.player_1P, score)
        elif player_id == 2:
            add_score(self.player_2P, score)

    # TODO move method to Station
    def change_obj_pos(self, objs=None):
        if objs is None:
            return
        for obj in objs:
            if isinstance(obj, Station):
                quadrant = obj.quadrant
                self.empty_quadrant_pos_dict[quadrant].append(obj.rect.topleft)
                if quadrant == 2 or quadrant == 3:
                    obj.quadrant = random.choice([2, 3])
                else:
                    obj.quadrant = random.choice([1, 4])
                quadrant = obj.quadrant
                new_pos = self.empty_quadrant_pos_dict[quadrant].pop(
                    random.randrange(len(self.empty_quadrant_pos_dict[quadrant])))
                set_topleft(obj, new_pos)

    def create_bullet(self, sprites: pygame.sprite.Group):
        for sprite in sprites:
            if not sprite.is_shoot:
                continue
            self.sound_controller.play_sound("shoot", 0.03, -1)
            init_data = create_construction(sprite.id, 0, sprite.rect.center, (13, 13))
            bullet = Bullet(init_data, rot=sprite.get_rot(), margin=2, spacing=2,
                            play_rect_area=self.play_rect_area)
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)
            set_shoot(sprite, False)

    def get_init_image_data(self):
        init_image_data = []
        for i in range(3):
            init_image_data.append(create_asset_init_data(f"floor_{i}", 50, 50
                                                          , path.join(IMAGE_DIR, f"grass_{i}.png"),
                                                          f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/grass_{i}.png"))
        for i in range(15):
            init_image_data.append(create_asset_init_data(f"hourglass_{i}", 42, 42
                                                          , path.join(IMAGE_DIR, f"hourglass_{i}.png"),
                                                          f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/hourglass_{i}.png"))
        for station in self.bullet_stations:
            if isinstance(station, Station):
                for data in station.get_obj_init_data():
                    init_image_data.append(data)
                break
        for wall in self.walls:
            if isinstance(wall, Wall):
                for data in wall.get_obj_init_data():
                    init_image_data.append(data)
                break
        img_id = "bullet"
        img_url = "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/bullet.png"
        bullet_image_init_data = create_asset_init_data(img_id, BULLET_SIZE[0], BULLET_SIZE[1],
                                                        path.join(IMAGE_DIR, f"{img_id}.png"), img_url)
        init_image_data.append(bullet_image_init_data)
        border_image_init_data = create_asset_init_data("border", self.scene_width, WINDOW_HEIGHT,
                                                        path.join(IMAGE_DIR, "border.png"),
                                                        f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/border.png")
        init_image_data.append(border_image_init_data)
        for data in self.player_1P.get_obj_init_data():
            init_image_data.append(data)
        lives_image_init_data_1 = create_asset_init_data("1P_lives", 30, 30, path.join(IMAGE_DIR, "1P_lives.png"),
                                                         "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/1P_lives.png")
        init_image_data.append(lives_image_init_data_1)
        lives_image_init_data_2 = create_asset_init_data("2P_lives", 30, 30, path.join(IMAGE_DIR, "2P_lives.png"),
                                                         "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/2P_lives.png")
        init_image_data.append(lives_image_init_data_2)
        return init_image_data

    def get_toggle_progress_data(self):
        toggle_data = []
        hourglass_index = 0
        if self.is_manual:
            hourglass_index = self.used_frame // 10 % 15
        toggle_data.append(
            create_image_view_data(image_id=f"hourglass_{hourglass_index}", x=0, y=2, width=20, height=20, angle=0))
        x = 23
        y = 8
        for frame in range((self.frame_limit - self.used_frame) // int((30 * 2))):
            toggle_data.append(create_rect_view_data("frame", x, y, 3, 10, RED))
            x += 3.5
        toggle_data.append(create_text_view_data(f"Frame: {self.frame_limit - self.used_frame}",
                                                 self.width_center + self.width_center // 2 + 85, 8, RED,
                                                 "24px Arial BOLD"))
        score_1P = self.player_1P.score
        score_2P = self.player_2P.score
        x = 24
        y = 20
        for score in range(min(score_1P, score_2P)):
            toggle_data.append(create_rect_view_data(name="score", x=x, y=y, width=1, height=10, color=ORANGE))
            x += 1.5
            if x > self.width_center:
                if y == 32:
                    y = 44
                else:
                    y = 32
                x = 24
        for score in range(abs(score_1P - score_2P)):
            if score_1P > score_2P:
                toggle_data.append(create_rect_view_data("score", x, y, 1, 10, DARKGREEN))
            else:
                toggle_data.append(create_rect_view_data("score", x, y, 1, 10, BLUE))
            x += 1.5
            if x > self.width_center:
                if y == 32:
                    y = 44
                else:
                    y = 32
                x = 24
        # 1P
        x = WINDOW_WIDTH - 105
        y = WINDOW_HEIGHT - 40
        toggle_data.append(create_text_view_data(f"Score: {score_1P}", x, y, DARKGREEN, "24px Arial BOLD"))
        x = self.width_center + 5
        y = WINDOW_HEIGHT - 40
        for live in range(self.player_1P.lives):
            toggle_data.append(create_image_view_data("1P_lives", x, y, 30, 30))
            x += 35
        # 620 px
        x = self.width_center + 120
        y = WINDOW_HEIGHT - 40
        toggle_data.append(
            create_rect_view_data("1P_oil", x, y, self.player_1P.oil, 10, ORANGE))
        x = self.width_center + 121
        y = WINDOW_HEIGHT - 20
        for power in range(self.player_1P.power):
            toggle_data.append(create_rect_view_data("1P_power", x, y, 8, 10, BLUE))
            x += 10
        # 2P
        x = 5
        y = WINDOW_HEIGHT - 40
        toggle_data.append(create_text_view_data(f"Score: {score_2P}", x, y, BLUE, "24px Arial BOLD"))
        x = self.width_center - 40
        y = WINDOW_HEIGHT - 40
        for live in range(self.player_2P.lives):
            toggle_data.append(create_image_view_data("2P_lives", x, y, 30, 30))
            x -= 35
        # 375 px
        x = self.width_center - 125 - 100 + (100 - self.player_2P.oil)
        y = WINDOW_HEIGHT - 40
        toggle_data.append(
            create_rect_view_data("2P_oil", x, y, self.player_2P.oil, 10,
                                  ORANGE))
        x = self.width_center - 125 - 9
        y = WINDOW_HEIGHT - 20
        for power in range(self.player_2P.power):
            toggle_data.append(create_rect_view_data("2P_power", x, y, 8, 10, BLUE))
            x -= 10

        return toggle_data

    def get_ai_data_to_player(self):
        to_player_data = {}
        num = 0
        competitor_info = {1: self.player_2P.get_data_from_obj_to_game()
                           , 2: self.player_1P.get_data_from_obj_to_game()
                           }
        walls_info = [wall.get_data_from_obj_to_game() for wall in self.walls if isinstance(wall, Wall)]
        bullet_stations_info = [bullst_station.get_data_from_obj_to_game() for bullst_station in self.bullet_stations if
                                isinstance(bullst_station, Station)]
        oil_stations_info = [oil_station.get_data_from_obj_to_game() for oil_station in self.oil_stations if
                             isinstance(oil_station, Station)]
        for player in self.players:
            if isinstance(player, Player):
                to_game_data = player.get_data_from_obj_to_game()
                to_game_data["used_frame"] = self.used_frame
                to_game_data["status"] = self.status
                to_game_data["competitor_info"] = competitor_info[player.id]
                to_game_data["walls_info"] = walls_info
                to_game_data["bullet_stations_info"] = bullet_stations_info
                to_game_data["oil_stations_info"] = oil_stations_info
                to_player_data[get_ai_name(num)] = to_game_data
                num += 1

        return to_player_data

    def get_bgm_data(self):
        return create_bgm_data("BGM.ogg", 0.1)

    def get_sound_data(self):
        return [create_sounds_data("shoot", "shoot.wav")
            , create_sounds_data("touch", "touch.wav")]

    def add_player_score(self, player_id: int):
        if not player_id:
            return
        if player_id == 1:
            add_score(self.player_1P, 20)
        else:
            add_score(self.player_2P, 20)

    def debugging(self, is_debug: bool):
        self.obj_rect_list = []
        if not is_debug:
            return
        for sprite in self.all_sprites:
            if isinstance(sprite, pygame.sprite.Sprite):
                top_left = sprite.rect.topleft
                points = [top_left, sprite.rect.topright, sprite.rect.bottomright
                    , sprite.rect.bottomleft, top_left]
                for index in range(len(points) - 1):
                    self.obj_rect_list.append(create_line_view_data("rect", *points[index], *points[index + 1], WHITE))
                    self.obj_rect_list.append(create_line_view_data("play_rect_area"
                                                                    , self.play_rect_area.x
                                                                    , self.play_rect_area.y
                                                                    , self.play_rect_area.width
                                                                    , self.play_rect_area.height, RED))
