import pygame.event

from games.TankMan.src.TankWall import TankWall
from games.TankMan.src.TankPlayer import TankPlayer
from GameFramework.BattleMode import BattleMode
from .TankBullet import TankBullet
from .collide_hit_rect import *
from .env import *


class TankBattleMode(BattleMode):
    def __init__(self, map_path: str, time_limit: int, is_sound: bool):
        super().__init__(map_path, time_limit, is_sound)
        self.players.__init__()
        # control variables
        self.is_invincible = True
        self.is_through_wall = True
        # initialize sprites group
        self.walls = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.bullet_stations = pygame.sprite.Group()
        self.oil_stations = pygame.sprite.Group()
        # init players
        players = self.map.create_obj_init_data(PLAYER_IMG_NO_LIST)
        # TODO how better
        for player in players:
            if player["_id"] == 1:
                self.player_1P = TankPlayer(player['_id'], player["_no"], player["x"], player["y"], player["width"], player["height"])
            else:
                self.player_2P = TankPlayer(player['_id'], player["_no"], player["x"], player["y"], player["width"], player["height"])
        self.players.add(self.player_1P, self.player_2P)
        # init walls
        walls = self.map.create_obj_init_data(WALL_IMG_NO_LIST)
        for wall in walls:
            self.walls.add(TankWall(wall['_id'], wall["x"], wall["y"], wall["width"], wall["height"]))
        self.all_sprites.add(self.walls)
        # init bullet stations
        bullet_stations = self.map.create_obj_init_data(BULLET_STATION_IMG_NO_LIST)
        for bullet_station in bullet_stations:
            self.bullet_stations.add(TankStation(bullet_station["_id"], 3,
                                                 bullet_station["x"], bullet_station["y"],
                                                 bullet_station["width"], bullet_station["height"], 10, 5))
        self.all_sprites.add(self.bullet_stations)
        # init oil stations
        oil_stations = self.map.create_obj_init_data(OIL_STATION_IMG_NO_LIST)
        for oil_station in oil_stations:
            self.oil_stations.add(TankStation(oil_station["_id"], 3,
                                              oil_station["x"], oil_station["y"],
                                              oil_station["width"], oil_station["height"], 100, 1))
        self.all_sprites.add(self.oil_stations)

    def game_update(self, command: dict):
        if not self.is_paused:
            if self.player_1P.is_shoot:
                shoot_info = self.player_1P.create_shoot_info()
                self.create_bullet(shoot_info)
                self.player_1P.is_shoot = False

            if self.player_2P.is_shoot:
                shoot_info = self.player_2P.create_shoot_info()
                shoot_info["rot"] -= 180
                self.create_bullet(shoot_info)
                self.player_2P.is_shoot = False

    def check_events(self):
        # TODO 要能邊前進邊射擊
        cmd_1P = ""
        cmd_2P = ""

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

        return {"1P": cmd_1P, "2P": cmd_2P}

    def check_collisions(self):
        if self.is_through_wall:
            for player in self.players:
                collide_with_walls(player, self.walls)
        if self.is_invincible:
            for player in self.players:
                collide_with_bullets(player, self.bullets)
                collide_with_stations(player, self.bullet_stations)
                collide_with_stations(player, self.oil_stations)
        for wall in self.walls:
            collide_with_bullets(wall, self.bullets)

    def create_bullet(self, shoot_info):
        bullet = TankBullet(shoot_info["id"], shoot_info["center_pos"], BULLET_SIZE[0], BULLET_SIZE[1], shoot_info["rot"])
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def draw_sprite_data(self):
        # 有辦法減少迴圈嗎?
        all_sprite_data = []
        for oil_station in self.oil_stations:
            if isinstance(oil_station, TankStation):
                oil_station_image_data = oil_station.get_image_data()
                all_sprite_data.append(oil_station_image_data)
        for bullet_station in self.bullet_stations:
            if isinstance(bullet_station, TankStation):
                bullet_station_image_data = bullet_station.get_image_data()
                all_sprite_data.append(bullet_station_image_data)
        for bullet in self.bullets:
            if isinstance(bullet, TankBullet):
                all_sprite_data.append(bullet.get_image_data())
        for player in self.players:
            if isinstance(player, TankPlayer):
                all_sprite_data.append(player.get_image_data())
        for wall in self.walls:
            if isinstance(wall, TankWall):
                if wall.get_image_data():
                    all_sprite_data.append(wall.get_image_data())

        return all_sprite_data

    def create_init_image_data(self):
        all_init_image_data = []
        for _id, img_path in OIL_STATION_IMG_PATH_DICT.items():
            all_init_image_data.append(self.data_creator.create_image_init_data(f"oil_station_{_id}", TILE_X_SIZE,
                                                                                TILE_Y_SIZE, img_path, OIL_URL[_id]))
        for _id, img_path in BULLET_STATION_IMG_PATH_DICT.items():
            all_init_image_data.append(self.data_creator.create_image_init_data(f"bullet_station_{_id}", TILE_X_SIZE,
                                                                                TILE_Y_SIZE, img_path, BULLETS_URL[_id]))
        for _id, img_path in WALL_IMG_PATH_DICT.items():
            all_init_image_data.append(self.data_creator.create_image_init_data(f"wall_{_id}", TILE_X_SIZE, TILE_Y_SIZE,
                                                                                img_path, WALL_URL[_id]))
        all_init_image_data.append(self.data_creator.create_image_init_data("bullets", TILE_X_SIZE, TILE_Y_SIZE,
                                                                            BULLET_IMG_PATH, BULLET_URL))
        for id, img_path in PLAYER_IMG_PATH_DICT.items():
            all_init_image_data.append(self.data_creator.create_image_init_data(id, TILE_X_SIZE, TILE_Y_SIZE,
                                                                                img_path, PLAYER_URL[id]))

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
        all_text_data.append(self.data_creator.create_text_data(
            f"2P Shield: {self.player_2P.shield} Power: {self.player_2P.power} Oil: {self.player_2P.oil} Lives: {self.player_2P.lives}",
            5, HEIGHT - 35, WHITE, "30px Arial"))
        all_text_data.append(self.data_creator.create_text_data(
            f"1P Lives: {self.player_2P.lives} Oil: {self.player_1P.oil} Power {self.player_1P.power} Shield: {self.player_1P.shield}",
            WIDTH_CENTER + 200, HEIGHT - 35, WHITE, "30px Arial"))
        return all_text_data

    def create_scene_info(self):
        scene_info = {"frame": self.used_frame,
                      "status": self.status,
                      "background": [WIDTH, HEIGHT],
                      "walls_xy_pos": [],
                      "1P_xy_pos": self.player_1P.get_xy_pos(),
                      "2P_xy_pos": self.player_2P.get_xy_pos(),
                      "bullet_stations_xy_pos": [],
                      "oil_stations_xy_pos": [],
                      "game_result": self.get_result(),
                      "state": self.state}

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
