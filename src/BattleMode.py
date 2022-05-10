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
            self.walls.add(Obstacle(wall["x"], wall["y"]))

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
        collide_bullets_with_walls(self.bullets, self.walls)

    def create_bullet(self, shoot_info):
        bullet = Bullet(shoot_info["player_no"], shoot_info["center_pos"], shoot_info["rot"])
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)
