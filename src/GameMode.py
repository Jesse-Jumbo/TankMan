import random
import sys

import pygame.event

from mlgame.gamedev.game_interface import GameResultState, GameStatus
from .Bullet import Bullet
from .Player import Player
from .TiledMap import TiledMap
from .collide_hit_rect import *
from games.TankMan.src.collide_hit_rect import collide_hit_rect
from games.TankMan.src.Obstacle import Obstacle
from games.TankMan.src.Player import Player


from .env import *


class GameMode:
    def __init__(self, map_name: str, sound_controller=None):
        self.sound_controller = sound_controller
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        # control variables
        self.playing = True
        self.draw_debug = False
        self.is_paused = False
        self.map_name = map_name
        # initialize sprites group
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.map = TiledMap(self.map_name)
        self.map.render()
        self.player_1P = Player(self.map.players[0]["_no"], self.map.players[0]["x"], self.map.players[0]["y"])
        self.player_2P = Player(self.map.players[1]["_no"], self.map.players[1]["x"], self.map.players[1]["y"])
        self.players.add(self.player_1P)
        self.players.add(self.player_2P)
        for wall in self.map.walls:
            self.walls.add(Obstacle(wall["x"], wall["y"]))
        self.frame = 0
        self.state = GameResultState.FAIL
        self.status = GameStatus.GAME_ALIVE

    def get_result(self) -> list:
        res = [{"1P": self.player_1P.get_result()},
               {"2P": self.player_2P.get_result()}]
        return res

    def run(self, command: dict):
        self.check_events()
        if not self.is_paused:
            self.update(command)

    def update(self, command: dict):
        self.status = GameStatus.GAME_ALIVE
        self.frame += 1
        # update potion of the game loop
        self.all_sprites.update()
        self.players.update(command)
        self.check_collisions()
        if command["1P"] == SHOOT:
            self.shoot(self.player_1P)
        if command["2P"] == SHOOT:
            self.shoot(self.player_2P)
        if self.player_1P.status == GameStatus.GAME_OVER:
            self.state = GameResultState.FINISH
            self.status = GameStatus.GAME_2P_WIN
            self.player_2P.status = GameStatus.GAME_2P_WIN
            self.playing = False
        if self.player_2P.status == GameStatus.GAME_OVER:
            self.state = GameResultState.FAIL
            self.status = GameStatus.GAME_1P_WIN
            self.player_1P.status = GameStatus.GAME_1P_WIN
            self.playing = False

    def check_events(self):
        pass

    def check_collisions(self):
        for player in self.players:
            collide_with_walls(player, self.walls)
            collide_with_bullets(player, self.bullets)
        collide_bullets_with_walls(self.bullets, self.walls)

    def shoot(self, player):
        if player.can_shoot:
            if player._no != 1:
                bullet = Bullet(2, player.pos, player.rot - 180)
            else:
                bullet = Bullet(1, player.pos, player.rot)
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)
            player.last_frame = self.frame
            player.can_shoot = False
