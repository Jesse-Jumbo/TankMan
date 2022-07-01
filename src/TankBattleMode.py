import pygame.event

from games.TankMan.src.TankWall import TankWall
from mlgame.gamedev.game_interface import GameStatus, GameResultState
from mlgame.view.view_model import create_asset_init_data, create_image_view_data, create_text_view_data
from .TankBullet import TankBullet
from .TankSoundController import TankSoundController
from .TankStation import TankStation
from .collide_hit_rect import *
from .env import *
from games.TankMan.GameFramework.BattleMode import BattleMode


class TankBattleMode(BattleMode):
    def __init__(self, map_path: str, frame_limit: int, is_sound: bool):
        super().__init__(map_path, frame_limit, is_sound)
        pygame.init()
        self.sound_controller = TankSoundController(is_sound)
        self.sound_controller.play_bgm()
        # control variables
        self.is_invincible = True
        self.is_through_wall = True
        # initialize sprites group
        self.walls = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.bullet_stations = pygame.sprite.Group()
        self.oil_stations = pygame.sprite.Group()
        # init players
        self.player_1P = self.map.create_init_obj(PLAYER_1_IMG_NO, TankPlayer)
        self.player_2P = self.map.create_init_obj(PLAYER_2_IMG_NO, TankPlayer)
        self.players.add(self.player_1P, self.player_2P)
        # init walls
        walls = self.map.create_init_obj_list(WALL_IMG_NO, TankWall, margin=8, spacing=8)
        [self.walls.add(wall) for wall in walls]
        self.all_sprites.add(self.walls)
        # init bullet stations
        bullet_stations = self.map.create_init_obj_list(BULLET_STATION_IMG_NO, TankStation, margin=2, spacing=2, capacity=10, cd_time=5, level=3)
        [self.bullet_stations.add(bullet_station) for bullet_station in bullet_stations]
        self.all_sprites.add(self.bullet_stations)
        # init oil stations
        oil_stations = self.map.create_init_obj_list(OIL_STATION_IMG_NO, TankStation, margin=2, spacing=2, capacity=100, cd_time=1, level=3)
        [self.oil_stations.add(oil_station) for oil_station in oil_stations]
        self.all_sprites.add(self.oil_stations)
        self.WIDTH_CENTER = self.map.map_width // 2

    def update(self, command: dict):
        self.update_game_mode(command)
        if self.player_1P.is_shoot:
            shoot_info = self.player_1P.create_shoot_info()
            self.create_bullet(shoot_info)
            self.player_1P.is_shoot = False

        if self.player_2P.is_shoot:
            shoot_info = self.player_2P.create_shoot_info()
            shoot_info["rot"] -= 180
            self.create_bullet(shoot_info)
            self.player_2P.is_shoot = False

    def calculate_score(self) -> tuple:
        score_1P = 100 - self.player_2P.shield + (3 - self.player_2P.lives) * 100
        score_2P = 100 - self.player_1P.shield + (3 - self.player_1P.lives) * 100
        return score_1P, score_2P

    def reset_2(self):
        score_1P = self.player_1P.score + self.calculate_score()[0]
        score_2P = self.player_2P.score + self.calculate_score()[1]
        if score_1P > score_2P:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_1P_WIN)
        elif score_1P < score_2P:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_2P_WIN)
        else:
            self.set_result(GameResultState.FAIL, GameStatus.GAME_DRAW)

    def get_1P_command(self) -> list:
        cmd_1P = []
        key_pressed_list = pygame.key.get_pressed()
        if key_pressed_list[pygame.K_UP]:
            cmd_1P.append(FORWARD_CMD)
        elif key_pressed_list[pygame.K_DOWN]:
            cmd_1P.append(BACKWARD_CMD)

        if key_pressed_list[pygame.K_SPACE]:
            cmd_1P.append(SHOOT)

        for even in pygame.event.get():
            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_RIGHT:
                    cmd_1P.append(RIGHT_CMD)
                elif even.key == pygame.K_LEFT:
                    cmd_1P.append(LEFT_CMD)

        return cmd_1P

    def get_2P_command(self) -> list:
        cmd_2P = []
        key_pressed_list = pygame.key.get_pressed()
        if key_pressed_list[pygame.K_w]:
            cmd_2P.append(FORWARD_CMD)
        elif key_pressed_list[pygame.K_s]:
            cmd_2P.append(BACKWARD_CMD)

        if key_pressed_list[pygame.K_f]:
            cmd_2P.append(SHOOT)

        for even in pygame.event.get():
            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_d:
                    cmd_2P.append(RIGHT_CMD)
                elif even.key == pygame.K_a:
                    cmd_2P.append(LEFT_CMD)

        return cmd_2P

    def check_collisions(self):
        if self.is_through_wall:
            for player in self.players:
                collide_with_walls(player, self.walls)
        if self.is_invincible:
            for player in self.players:
                collide_with_bullets(player, self.bullets)
                collide_with_bullet_stations(player, self.bullet_stations)
                collide_with_oil_stations(player, self.oil_stations)
        for wall in self.walls:
            player_id, score = collide_with_bullets(wall, self.bullets)
            for player in self.players:
                if player._id == player_id:
                    player.score += score

    def create_bullet(self, shoot_info):
        self.sound_controller.play_shoot_sound()
        bullet = TankBullet(shoot_info["id"], shoot_info["center_pos"], BULLET_SIZE[0], BULLET_SIZE[1],
                            shoot_info["rot"])
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def draw_sprite_data(self):
        all_sprite_data = []
        for oil_station in self.oil_stations:
            if isinstance(oil_station, TankStation):
                data = oil_station.get_image_data()
                all_sprite_data.append(create_image_view_data(data[self._ID], data[self._X], data[self._Y],
                                                              data[self._WIDTH], data[self._HEIGHT],
                                                              data[self._ANGLE]))

        for bullet_station in self.bullet_stations:
            if isinstance(bullet_station, TankStation):
                data = bullet_station.get_image_data()
                all_sprite_data.append(create_image_view_data(data[self._ID], data[self._X], data[self._Y],
                                                              data[self._WIDTH], data[self._HEIGHT],
                                                              data[self._ANGLE]))

        for bullet in self.bullets:
            if isinstance(bullet, TankBullet):
                data = bullet.get_image_data()
                all_sprite_data.append(create_image_view_data(data[self._ID], data[self._X], data[self._Y],
                                                              data[self._WIDTH], data[self._HEIGHT],
                                                              data[self._ANGLE]))

        for player in self.draw_players():
            all_sprite_data.append(player)

        for wall in self.walls:
            if isinstance(wall, TankWall):
                data = wall.get_image_data()
                if data:
                    all_sprite_data.append(create_image_view_data(data[self._ID], data[self._X], data[self._Y],
                                                                  data[self._WIDTH], data[self._HEIGHT],
                                                                  data[self._ANGLE]))

        return all_sprite_data

    def draw_text_data(self):
        all_text_data = []
        all_text_data.append(create_text_view_data(f"1P_Score: {self.player_1P.score + self.calculate_score()[0]}",
                                                   5, 0, GREEN,
                                                   "30px Arial"))
        all_text_data.append(create_text_view_data(f"2P_Score: {self.player_2P.score + self.calculate_score()[1]}",
                                                   self.WIDTH_CENTER, 0, BLUE, "30px Arial"))
        all_text_data.append(create_text_view_data(f"CountDownFrame: {self.frame_limit - self.used_frame}",
                                                   self.WIDTH_CENTER + self.WIDTH_CENTER // 2 + 30, 0, RED,
                                                   "30px Arial"))
        all_text_data.append(create_text_view_data(
            f"2P Lives: {self.player_2P.lives} Oil: {int(self.player_2P.oil)} Power: {self.player_2P.power} Shield: {self.player_2P.shield}",
            self.WIDTH_CENTER, WINDOW_HEIGHT - 35, BLUE, "30px Arial"))
        all_text_data.append(create_text_view_data(
            f"1P Lives: {self.player_2P.lives} Oil: {int(self.player_1P.oil)} Power {self.player_1P.power} Shield: {self.player_1P.shield}",
            5, WINDOW_HEIGHT - 35, GREEN, "30px Arial"))

        return all_text_data

    def create_init_image_data(self):
        all_init_image_data = []
        for station in self.oil_stations:
            if isinstance(station, TankStation):
                for data in station.get_image_init_data():
                    all_init_image_data.append(data)
                break
        for wall in self.walls:
            if isinstance(wall, TankWall):
                for data in wall.get_image_init_data():
                    all_init_image_data.append(data)
                break
        img_id = "bullet"
        img_url = "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/version_0.0.10/asset/image/bullet.png"
        image_init_data = create_asset_init_data(img_id, BULLET_SIZE[0], BULLET_SIZE[1], path.join(IMAGE_DIR, f"{img_id}.png"), img_url)
        all_init_image_data.append(image_init_data)
        for data in self.player_1P.get_image_init_data():
            all_init_image_data.append(data)
        return all_init_image_data

    def create_scene_info(self):
        scene_info = self.get_scene_info()
        scene_info["background"] = [WINDOW_WIDTH, WINDOW_HEIGHT]
        scene_info["walls_xy_pos"] = []
        scene_info["bullet_stations_xy_pos"] = []
        scene_info["oil_stations_xy_pos"] = []

        for wall in self.walls:
            if isinstance(wall, TankWall):
                scene_info["walls_xy_pos"].append(wall.get_xy_pos())
        for bullet_station in self.bullet_stations:
            if isinstance(bullet_station, TankStation):
                scene_info["bullet_stations_xy_pos"].append(bullet_station.get_xy_pos())
        for oil_station in self.oil_stations:
            if isinstance(oil_station, TankStation):
                scene_info["oil_stations_xy_pos"].append(oil_station.get_xy_pos())
        return scene_info

    def create_game_data_to_player(self):
        to_player_data = {}
        for player in self.players:
            if isinstance(player, TankPlayer):
                info = player.get_info()
                info["used_frame"] = self.used_frame
                info["status"] = self.status
                walls_info = []
                for wall in self.walls:
                    if isinstance(wall, TankWall):
                        walls_info.append(wall.get_info())
                info["walls_info"] = walls_info
                bullet_stations_info = []
                for bullet_station in self.bullet_stations:
                    if isinstance(bullet_station, TankStation):
                        bullet_stations_info.append(bullet_station.get_info())
                info["bullet_stations_info"] = bullet_stations_info
                oil_stations_info = []
                for oil_station in self.oil_stations:
                    if isinstance(oil_station, TankStation):
                        oil_stations_info.append(oil_station.get_info())
                info["oil_stations_info"] = oil_stations_info

                to_player_data[f"{player._id}P"] = info

        return to_player_data
