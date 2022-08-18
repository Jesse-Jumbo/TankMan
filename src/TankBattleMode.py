import random

import pygame.event
from .GameFramework.BattleMode import BattleMode
from mlgame.game.paia_game import GameResultState, GameStatus
from .TankWall import TankWall
from mlgame.view.view_model import create_asset_init_data, create_image_view_data, create_text_view_data, \
    create_rect_view_data, create_line_view_data
from .TankBullet import TankBullet
from .TankSoundController import TankSoundController
from .TankStation import TankStation
from .collide_hit_rect import *
from .env import *


# TODO refactor attribute to methodp
class TankBattleMode(BattleMode):
    def __init__(self, user_num: int, map_path: str, frame_limit: int, is_sound: bool):
        super().__init__(user_num, map_path, frame_limit, is_sound)
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
        self.all_sprites.add(self.player_1P, self.player_2P)
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
        self.HEIGHT_CENTER = self.map.map_height // 2
        # init floor pos
        self.floor = []
        for x in range(self.map.width):
            for y in range(self.map.height):
                no = random.randrange(3)
                self.floor.append(no)

    def update(self, command: dict):
        if command["1P"] and "DEBUG" in command["1P"]:
            self.is_debug = not self.is_debug
        self.walls.update()
        self.update_game_mode(command)
        self.oil_stations.update()
        self.bullet_stations.update()
        self.bullets.update()
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
        score_1P = (3 - self.player_2P.lives) * 20
        score_2P = (3 - self.player_1P.lives) * 20
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
                collide_with_bullet_stations(player, self.bullet_stations, self.all_sprites)
                collide_with_oil_stations(player, self.oil_stations, self.all_sprites)
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
        i = 0
        for x in range(self.map.width):
            for y in range(self.map.height):
                no = self.floor[i]
                i += 1
                all_sprite_data.append(create_image_view_data(f"floor_{no}"
                                                              , x * self.map.tile_width, y * self.map.tile_height
                                                              , 50, 50, 0))
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

        if self.is_debug:
            for sprite in self.all_sprites:
                all_sprite_data.extend(self.draw_rect(sprite))

        all_sprite_data.append(create_image_view_data("border", 0, 0, self.map.map_width, self.map.map_height, 0))

        return all_sprite_data

    def draw_foreground_data(self):
        all_foreground_data = []


        return all_foreground_data

    def draw_toggle_data(self):
        all_toggle_data = []
        score_1P = self.player_1P.score + self.calculate_score()[0]
        score_2P = self.player_2P.score + self.calculate_score()[1]
        x = 10
        y = 20
        _x = 0
        for score in range(min(score_1P, score_2P)):
            all_toggle_data.append(create_rect_view_data("score", x, y, 1, 10, YELLOW))
            x += 2
            if x > 500:
                y = 32
                x = 10
                _x = x
        for score in range(abs(score_1P - score_2P)):
            if score_1P > score_2P:
                all_toggle_data.append(create_rect_view_data("score", x, y, 1, 10, GREEN))
            else:
                all_toggle_data.append(create_rect_view_data("score", x, y, 1, 10, BLUE))
            x += 2
            if x > 500:
                y = 32
                x = 10
                if _x:
                    x = _x
        x = 10
        for frame in range((self.frame_limit - self.used_frame) // 30):
            all_toggle_data.append(create_rect_view_data("frame", x, 8, 1, 10, RED))
            x += 2
        all_toggle_data.append(create_text_view_data(f"Score: {score_1P}",
                                                     self.WIDTH_CENTER + 50, 8, GREEN,
                                                     "24px Arial"))
        all_toggle_data.append(create_text_view_data(f"Score: {score_2P}",
                                                     self.WIDTH_CENTER + 190, 8, BLUE, "24px Arial"))
        all_toggle_data.append(create_text_view_data(f"Frame: {self.frame_limit - self.used_frame}",
                                                     self.WIDTH_CENTER + self.WIDTH_CENTER // 2 + 85, 8, RED,
                                                     "24px Arial"))
        # 1P
        x = 10
        for live in range(self.player_1P.lives):
            all_toggle_data.append(create_image_view_data("1P_lives", x, WINDOW_HEIGHT - 35, 30, 30))
            x += 35
        all_toggle_data.append(
            create_rect_view_data("1P_oil", x+10, WINDOW_HEIGHT - 25, int(self.player_1P.oil), 10, ORANGE))
        x += 120
        for power in range(self.player_1P.power):
            all_toggle_data.append(create_rect_view_data("1P_power", x, WINDOW_HEIGHT - 25, 8, 10, BLUE))
            x += 10
        # 2P
        x = self.WIDTH_CENTER + 10
        for live in range(self.player_2P.lives):
            all_toggle_data.append(create_image_view_data("2P_lives", x, WINDOW_HEIGHT - 35, 30, 30))
            x += 35
        all_toggle_data.append(
            create_rect_view_data("2P_oil", x+10, WINDOW_HEIGHT - 25, int(self.player_2P.oil), 10,
                                  ORANGE))
        x += 120
        for power in range(self.player_2P.power):
            all_toggle_data.append(create_rect_view_data("2P_power", x, WINDOW_HEIGHT - 25, 8, 10, BLUE))
            x += 10

        return all_toggle_data

    def create_init_image_data(self):
        all_init_image_data = []
        for i in range(3):
            all_init_image_data.append(create_asset_init_data(f"floor_{i}", 50, 50
                                                              , path.join(IMAGE_DIR, f"grass_{i}.png"), ""))
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
        bullet_image_init_data = create_asset_init_data(img_id, BULLET_SIZE[0], BULLET_SIZE[1], path.join(IMAGE_DIR, f"{img_id}.png"), img_url)
        all_init_image_data.append(bullet_image_init_data)
        border_image_init_data = create_asset_init_data("border", self.map.map_width, self.map.map_height, path.join(IMAGE_DIR, "border.png"), "")
        all_init_image_data.append(border_image_init_data)
        for data in self.player_1P.get_image_init_data():
            all_init_image_data.append(data)
        lives_image_init_data_1 = create_asset_init_data("1P_lives", 30, 30, path.join(IMAGE_DIR, "1P_lives.png"), "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/1P_lives.png")
        all_init_image_data.append(lives_image_init_data_1)
        lives_image_init_data_2 = create_asset_init_data("2P_lives", 30, 30, path.join(IMAGE_DIR, "2P_lives.png"), "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/2P_lives.png")
        all_init_image_data.append(lives_image_init_data_2)
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
                player_info = []
                if player._id == 2:
                    player_info.append(self.player_1P.get_info())
                else:
                    player_info.append(self.player_2P.get_info())
                info["player_info"] = player_info
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

    def get_other_result(self, origin_result):
        if origin_result["id"] == "1P":
            origin_result["score"] = self.player_1P.score + self.calculate_score()[0]
        else:
            origin_result["score"] = self.player_2P.score + self.calculate_score()[1]
        return origin_result

    def draw_rect(self, sprite):
        all_line = []
        point = [(sprite.rect.x, sprite.rect.y), sprite.rect.topright, sprite.rect.bottomright, sprite.rect.bottomleft, (sprite.rect.x, sprite.rect.y)]
        hit_point = [(sprite.hit_rect.x, sprite.hit_rect.y), sprite.hit_rect.topright, sprite.hit_rect.bottomright, sprite.hit_rect.bottomleft, (sprite.hit_rect.x, sprite.hit_rect.y)]
        for i in range(4):
            all_line.append(create_line_view_data(f"{sprite.get_info()['id']}", point[i][0], point[i][1], point[i+1][0], point[i+1][1], YELLOW, 2))
            all_line.append(create_line_view_data(f"hit_{sprite.get_info()['id']}", hit_point[i][0], hit_point[i][1], hit_point[i+1][0], hit_point[i+1][1], RED, 2))
        return all_line
