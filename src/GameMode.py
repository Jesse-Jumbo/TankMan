import random
import sys

import pygame.event

from mlgame.gamedev.game_interface import GameResultState, GameStatus
from .Player import Player
from .TiledMap import TiledMap
from .collide_hit_rect import *
from games.GameName.src.collide_hit_rect import collide_hit_rect

from .env import *


class GameMode:
    def __init__(self, map_name: str, sound_controller):
        self.sound_controller = sound_controller
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        # control variables
        self.playing = True
        self.draw_debug = False
        self.is_paused = False
        self.map_name = map_name
        # initialize sprites group
        self.all_sprites = pygame.sprite.Group()
        self.map = TiledMap(self.map_name)
        self.player = self.map.player
        self.walls = self.map.walls
        self.mobs = self.map.mobs
        self.frame = 0
        self.state = GameResultState.FAIL
        self.status = GameStatus.GAME_ALIVE
        self.player = Player(0, 0)

    def get_result(self) -> list:
        res = [self.player.get_result()]
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
        self.player.update(command)
        self.check_collisions()
        """"
        if gamewin:
            self.playing = False
            self.state = GameResultState.FINISH
            self.status = GameStatus.GAME_PASS
        if gamelose:
            self.state = GameResultState.FAIL
            self.status = GameStatus.GAME_OVER
            self.playing = False
        """

    def check_events(self):
        pass

    def check_collisions(self):
        collide_with_mobs(self.player, self.mobs)
        collide_with_walls(self.player, self.mobs)
        for mob in self.mobs:
            collide_with_walls(mob, self.walls)
        pass
