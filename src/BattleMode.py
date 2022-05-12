import pygame.event

from games.TankMan.src.Obstacle import Obstacle
from games.TankMan.src.TankPlayer import TankPlayer
from mlgame.gamedev.game_interface import GameResultState, GameStatus
from .Bullet import Bullet
from .GameMode import GameMode
from .collide_hit_rect import *
from .env import *


class BattleMode(GameMode):
    def __init__(self, map_path: str, time_limit: int, is_sound: bool):
        super().__init__(map_path, time_limit, is_sound)
        # control variables
        self.is_debug = False
        self.is_invincible = True
        self.is_through_wall = True
        # initialize sprites group
        self.players = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.bullet_stations = pygame.sprite.Group()
        self.oil_stations = pygame.sprite.Group()

        # init players
        players = self.map.create_img_init_data(PLAYER_IMG_NO_LIST)
        for player in players:
            if player["_id"] == 1:
                self.player_1P = TankPlayer(1, player["x"], player["y"], player["width"], player["height"])
            else:
                self.player_2P = TankPlayer(2, player["x"], player["y"], player["width"], player["height"])
        self.players.add(self.player_1P)
        self.players.add(self.player_2P)
        # init walls
        walls = self.map.create_img_init_data(WALL_IMG_NO_LIST)
        for wall in walls:
            self.walls.add(Obstacle(wall["_no"], wall["x"], wall["y"], wall["width"], wall["height"]))
        self.all_sprites.add(self.walls)
        # init bullet stations
        bullet_stations = self.map.create_img_init_data(BULLET_STATION_IMG_NO_LIST)
        for bullet_station in bullet_stations:
            self.bullet_stations.add(Station(bullet_station["_id"],
                                             bullet_station["x"], bullet_station["y"],
                                             bullet_station["width"], bullet_station["height"], 10, 5))
        self.all_sprites.add(self.bullet_stations)
        # init oil stations
        oil_stations = self.map.create_img_init_data(OIL_STATION_IMG_NO_LIST)
        for oil_station in oil_stations:
            self.oil_stations.add(Station(oil_station["_id"],
                                          oil_station["x"], oil_station["y"],
                                          oil_station["width"], oil_station["height"], 100, 1))
        self.all_sprites.add(self.oil_stations)

    def get_result(self) -> list:
        res = [{"1P": self.player_1P.get_info()},
               {"2P": self.player_2P.get_info()}]
        return res

    def update(self, command: dict):
        super().update(command)
        if not self.is_paused:
            self.player_1P.update(command["1P"])
            self.player_2P.update(command["2P"])
            if self.player_1P.is_shoot:
                shoot_info = self.player_1P.create_shoot_info()
                self.create_bullet(shoot_info)
                self.player_1P.is_shoot = False

            if self.player_2P.is_shoot:
                shoot_info = self.player_2P.create_shoot_info()
                shoot_info["rot"] -= 180
                self.create_bullet(shoot_info)
                self.player_2P.is_shoot = False

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
        super().reset()

    def check_events(self):
        pass

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
        bullet = Bullet(shoot_info["player_no"], shoot_info["center_pos"], shoot_info["rot"])
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def draw_sprite_data(self):
        all_sprite_data = []
        for oil_station in self.oil_stations:
            bullet_station_image_data = oil_station.get_image_data()
            bullet_station_image_data["_id"] = f"oil_station_{oil_station._no}"
            all_sprite_data.append(bullet_station_image_data)
        for bullet_station in self.bullet_stations:
            bullet_station_image_data = bullet_station.get_image_data()
            bullet_station_image_data["_id"] = f"bullet_station_{bullet_station._no}"
            all_sprite_data.append(bullet_station_image_data)
        for bullet in self.bullets:
            all_sprite_data.append(bullet.get_image_data())
        for player in self.players:
            all_sprite_data.append(player.get_image_data())
        for wall in self.walls:
            if wall.get_image_data():
                all_sprite_data.append(wall.get_image_data())

        return all_sprite_data

    def create_init_image_data(self):
        all_init_image_data = []
        c = 0
        for img_path in OIL_STATION_IMG_PATH_LIST:
            c += 1
            all_init_image_data.append(
                {"_id": f"oil_station_{c}", "width": TILE_X_SIZE, "height": TILE_Y_SIZE, "path": img_path, "url": ""})
        c = 0
        for img_path in BULLET_STATION_IMG_PATH_LIST:
            c += 1
            all_init_image_data.append(
                {"_id": f"bullet_station_{c}", "width": TILE_X_SIZE, "height": TILE_Y_SIZE, "path": img_path,
                 "url": ""})
        c = 5
        for img_path in WALL_IMG_PATH_LIST:
            all_init_image_data.append(
                {"_id": f"wall_{c}", "width": TILE_X_SIZE, "height": TILE_Y_SIZE, "path": img_path, "url": ""})
            c -= 1
        bullet_data = {"_id": "bullets", "width": TILE_X_SIZE, "height": TILE_Y_SIZE, "path": BULLET_IMG_PATH,
                       "url": ""}
        all_init_image_data.append(bullet_data)
        for player in self.players:
            all_init_image_data.append(player.get_image_init_data())

        return all_init_image_data

    def draw_text_data(self):
        all_text_data = []
        all_text_data.append(
            {"content": f"1P_Score: {self.player_1P.score}", "x": WIDTH_CENTER + WIDTH_CENTER // 2 - 45, "y": 0,
             "color": WHITE, "font_style": "30px Arial"})
        all_text_data.append({"content": f"2P_Score: {self.player_2P.score}", "x": WIDTH_CENTER // 2 - 45, "y": 0,
                              "color": WHITE, "font_style": "30px Arial"})
        all_text_data.append({"content": f"Time: {self.used_frame // 60}", "x": WIDTH - 100, "y": 0,
                              "color": WHITE, "font_style": "30px Arial"})
        all_text_data.append(
            {"content": f"2P Shield: {self.player_2P.shield} Power: {self.player_2P.power} Oil: {self.player_2P.oil}",
             "x": 5, "y": HEIGHT - 35,
             "color": WHITE, "font_style": "30px Arial"})
        all_text_data.append(
            {"content": f"1P Oil: {self.player_1P.oil} Power {self.player_1P.power} Shield: {self.player_1P.shield}",
             "x": WIDTH - 380, "y": HEIGHT - 35,
             "color": WHITE, "font_style": "30px Arial"})
        return all_text_data
