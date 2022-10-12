import pygame

from os import path
from mlgame.game.paia_game import GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name
from mlgame.view.view_model import create_line_view_data, create_asset_init_data, create_text_view_data

from .Mob import Mob
from .game_module.TiledMap import create_construction
from .Player import Player
from .env import WHITE, RED, IMAGE_DIR, YELLOW, GREEN

SCENE_WIDTH = 800
SCENE_HEIGHT = 600


class BattleMode:
    def __init__(self, play_rect_area: pygame.Rect, is_manual: bool, level: int):
        pygame.init()
        self._user_num = 2
        self.scene_width = SCENE_WIDTH
        self.scene_height = SCENE_HEIGHT
        self.width_center = SCENE_WIDTH // 2
        self.height_center = SCENE_HEIGHT // 2
        self.play_rect_area = play_rect_area
        self.all_sprites = pygame.sprite.Group()
        self.is_manual = is_manual
        self.game_level = level
        # init players
        self.players = pygame.sprite.Group()
        self.player_1P = Player(create_construction(get_ai_name(0), 0
                                                    , (self.width_center//2-50, self.scene_height-50)
                                                    , (50, 50)), play_rect_area=play_rect_area, is_manual=is_manual)
        self.player_2P = Player(create_construction(get_ai_name(1), 1
                                                    , (self.width_center+self.width_center//2, SCENE_HEIGHT-50)
                                                    , (50, 50)), play_rect_area=play_rect_area, is_manual=is_manual)
        self.players.add(self.player_1P)
        self.players.add(self.player_2P)
        self.all_sprites.add(*self.players)
        # init mobs
        self.mobs = pygame.sprite.Group()
        self.create_mobs(self.game_level)
        self.used_frame = 0
        self.state = GameResultState.FAIL
        self.status = GameStatus.GAME_ALIVE
        self.obj_rect_list = []

    def create_mobs(self, level: int):
        count = 0
        for x in range(50, self.scene_width - 50, 50):
            for y in range(50, self.height_center, 50):
                count += 1
                mob = Mob(create_construction(level, count, (x, y), (50, 50)), play_rect_area=self.play_rect_area)
                self.mobs.add(mob)
        self.all_sprites.add(*self.mobs)

    def update(self, command: dict) -> None:
        self.used_frame += 1
        self.players.update(command)
        self.mobs.update()
        self.handle_collisions()
        self.get_player_end()

    def reset(self) -> None:
        self.__init__(self.play_rect_area, self.is_manual, self.game_level)

    def get_player_end(self):
        if not self.player_1P.is_alive and not self.player_2P.is_alive:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_OVER)
        elif not len(self.mobs):
            if self.player_1P.score > self.player_2P.score:
                self.set_result(GameResultState.FINISH, GameStatus.GAME_1P_WIN)
            elif self.player_1P.score < self.player_2P.score:
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

    def get_init_image_data(self):
        init_image_data = []
        for player in self.players:
            if isinstance(player, Player):
                init_image_data.append(player.get_obj_init_data())
        for mob in self.mobs:
            if isinstance(mob, Mob):
                init_image_data.append(mob.get_obj_init_data())
                break
        for no in range(1, 7):
            init_image_data.append(create_asset_init_data(f"bullet_{no}", *(12, 27)
                                                          , path.join(IMAGE_DIR, f"bullet_0{no}.png"), "url"))

        return init_image_data

    def get_ai_data_to_player(self):
        to_player_data = {}
        num = 0
        competitor_info = {1: self.player_2P.get_data_from_obj_to_game()
                           , 2: self.player_1P.get_data_from_obj_to_game()
                           }
        mobs_info = [mob.get_data_from_obj_to_game() for mob in self.mobs if isinstance(mob, Mob)]

        for player in self.players:
            if isinstance(player, Player):
                to_game_data = player.get_data_from_obj_to_game()
                to_game_data["used_frame"] = self.used_frame
                to_game_data["status"] = self.status
                to_game_data["partner_info"] = competitor_info
                to_game_data["mob_info"] = mobs_info
                to_player_data[get_ai_name(num)] = to_game_data
                num += 1

        return to_player_data

    def get_obj_progress_data(self) -> list:
        obj_progress_data = []
        for player in self.players:
            if isinstance(player, Player):
                obj_progress_data.extend(player.get_obj_progress_data())
        for mob in self.mobs:
            if isinstance(mob, Mob):
                obj_progress_data.extend(mob.get_obj_progress_data())
        if self.obj_rect_list:
            obj_progress_data.extend(self.obj_rect_list)

        return obj_progress_data

    def get_toggle_data(self) -> list:
        toggle_data_list = [create_text_view_data(content=f"Frame: {self.used_frame}", x=self.scene_width-180, y=10
                                                      , color=RED, font_style="30px Arial BOLD")]
        data_1P = f"1P Lives: {self.player_1P.lives} Shield: {self.player_1P.shield} Score: {self.player_1P.score}"
        data_2P = f"2P Lives: {self.player_2P.lives} Shield: {self.player_2P.shield} Score: {self.player_2P.score}"
        toggle_data_list.append(create_text_view_data(content=data_1P, x=10, y=10, color=GREEN, font_style="28px Arial"))
        toggle_data_list.append(create_text_view_data(content=data_2P, x=10, y=50, color=YELLOW, font_style="28px Arial"))
        return toggle_data_list

    def debugging(self, is_debug: bool) -> list:
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

    def handle_collisions(self):
        for mob in self.mobs:
            if isinstance(mob, Mob):
                bullets = pygame.sprite.spritecollide(mob, self.player_1P.bullets, True, pygame.sprite.collide_rect_ratio(0.8))
                if bullets:
                    mob.kill()
                    self.player_1P.score += 10
                bullets = pygame.sprite.spritecollide(mob, self.player_2P.bullets, True, pygame.sprite.collide_rect_ratio(0.8))
                if bullets:
                    mob.kill()
                    self.player_2P.score += 10
                hits_dict = pygame.sprite.groupcollide(self.players, mob.bullets, False, True, pygame.sprite.collide_rect_ratio(0.8))
                for player, bullet in hits_dict.items():
                    if isinstance(player, Player):
                        player.shield -= len(bullet) * 10
                players = pygame.sprite.spritecollide(mob, self.players, False, self.collide_attack_rect)
                for player in  players:
                    if mob.is_attack:
                        mob.kill()
                        player.lives -= 1

    def collide_attack_rect(self, mob: Mob, player: Player) -> int:
        mob_hit_rect = pygame.Rect(*mob.attack_rect.topleft, mob.attack_rect.width - 2, mob.attack_rect.height - 2)
        mob_hit_rect.center = mob.attack_rect.center
        player_hit_rect = pygame.Rect(*player.rect.topleft, player.rect.width-2, player.rect.height-2)
        player_hit_rect.center = player.rect.center
        return mob_hit_rect.colliderect(player_hit_rect)
