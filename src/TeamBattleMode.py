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
from .Gun import Gun
from .Station import Station
from .Wall import Wall
from .collide_hit_rect import *
from .env import *
from .game_module.fuctions import set_topleft, add_score, set_shoot
from .MapGenerator import MapGenerator
from .Unbreakable_Wall import Unbreakable_Wall


class TeamBattleMode:
    def __init__(self, green_team_num: int, blue_team_num: int, is_manual: bool, frame_limit: int, sound_path: str, play_rect_area: pygame.Rect):
        # init game
        pygame.init()
        self.sound_path = sound_path
        self.green_team_num = green_team_num
        self.blue_team_num = blue_team_num if (6 - (green_team_num + blue_team_num)) >= 0 else (6 - green_team_num)
        self.map_name = f"map_{green_team_num}_v_{self.blue_team_num}.tmx" if not IS_DEBUG else f"test_map_{green_team_num}_v_{self.blue_team_num}.tmx"
        self.map_path = path.join(MAP_DIR, self.map_name)
        self.map_generator = MapGenerator(self.green_team_num, self.blue_team_num, 40, 24)
        self.tileSize = self.map_generator.getTileSize()
        self.size_multiplier = self.tileSize / 50
        self.map_generator.generate_map()
        self.map = TiledMap(self.map_path)
        # self.scene_width = self.map.map_width
        self.scene_width, _ = self.map_generator.getScreeenSize()
        self.scene_height = self.map.map_height + 100
        self.width_center = self.scene_width // 2
        self.height_center = self.scene_height // 2
        self.play_rect_area = play_rect_area
        self.play_rect_area.width = self.scene_width
        self.used_frame = 0
        self.state = GameResultState.FAIL
        self.status = GameStatus.GAME_ALIVE
        self.sound_controller = SoundController(sound_path, self.get_sound_data())
        self.sound_controller.play_music(self.get_bgm_data())
        self.frame_limit = frame_limit
        self.is_manual = is_manual
        self.obj_rect_list = []
        self.team_green_score = 0
        self.team_blue_score = 0

        # control variables
        self.is_invincible = False
        self.is_through_wall = False
        # initialize sprites group
        self.all_sprites = pygame.sprite.Group()
        self.players_a = pygame.sprite.Group()
        self.players_b = pygame.sprite.Group()
        self.all_players = pygame.sprite.Group()
        self.guns = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.unbreakable_walls = pygame.sprite.Group()
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
        self.map.add_init_obj_data(BULLET_STATION_IMG_NO, Station, spawn_cd=30, margin=2, spacing=2, capacity=5, quadrant=1)
        self.map.add_init_obj_data(OIL_STATION_IMG_NO, Station, spawn_cd=30, margin=2, spacing=2, capacity=30, quadrant=1)
        self.map.add_init_obj_data(UNBREAK_WALL_IMG_NO, Unbreakable_Wall, margin=8, spacing=8)
        # create obj
        all_obj = self.map.create_init_obj_dict()
        # init players
        self.players_a.add(all_obj[PLAYER_1_IMG_NO])
        self.players_b.add(all_obj[PLAYER_2_IMG_NO])
        no = 1
        for player in self.players_a:
            player.no = no
            no += 1
        for player in self.players_b:
            player.no = no
            no += 1
        self.all_players.add(*self.players_a, *self.players_b)
        self.guns.add(*[player.gun for player in self.all_players])
        self.all_sprites.add(*self.players_a, *self.players_b)
        self.all_sprites.add(*[player.gun for player in self.all_players])
        # init walls
        self.walls.add(all_obj[WALL_IMG_NO])
        self.all_sprites.add(*self.walls)
        # init unbreakable walls
        self.unbreakable_walls.add(all_obj[UNBREAK_WALL_IMG_NO])
        self.all_sprites.add(*self.unbreakable_walls)
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
                create_image_view_data(f"floor_{no}", pos[0], pos[1], self.tileSize, self.tileSize, 0))
        self.obj_list = [self.oil_stations, self.bullet_stations, self.bullets, self.all_players, self.guns, self.walls, self.unbreakable_walls]
        self.background.append(create_image_view_data("border", 0, -50, self.scene_width, WINDOW_HEIGHT, 0))
        # self.background.append(create_image_view_data("border", 0, -self.tileSize, self.scene_width, self.scene_height, 0))

    def update(self, command: dict):
        # refactor
        self.team_green_score = sum([player.score for player in self.players_a if isinstance(player, Player)])
        self.team_blue_score = sum([player.score for player in self.players_b if isinstance(player, Player)])
        self.used_frame += 1
        self.check_collisions()
        self.walls.update()
        self.unbreakable_walls.update()
        self.create_bullet(self.all_players)
        self.bullets.update()
        self.bullet_stations.update()
        self.oil_stations.update()
        self.all_players.update(command)
        self.get_player_end()
        if self.used_frame >= self.frame_limit:
            self.get_game_end()

    def reset(self):
        # reset init game
        self.__init__(self.green_team_num, self.blue_team_num, self.is_manual, self.frame_limit, self.sound_path, self.play_rect_area)
        # reset player pos
        self.change_player_pos()

    def get_player_end(self):
        is_alive_team_green = False
        is_alive_team_blue = False
        for player in self.all_players:
            if isinstance(player, Player) and player.is_alive:
                if player.no > self.green_team_num and not is_alive_team_blue:
                    is_alive_team_blue = True
                elif player.no <= self.green_team_num:
                    is_alive_team_green = True

        if not is_alive_team_blue:
            self.set_result(GameResultState.FINISH, "GREEN_TEAM_WIN")
        elif not is_alive_team_green:
            self.set_result(GameResultState.FINISH, "BLUE_TEAM_WIN")

    def get_game_end(self):
        if self.team_green_score > self.team_blue_score:
            self.set_result(GameResultState.FINISH, "GREEN_TEAM_WIN")
        elif self.team_green_score < self.team_blue_score:
            self.set_result(GameResultState.FINISH, "BLUE_TEAM_WIN")
        else:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_DRAW)

    def set_result(self, state: str, status: str):
        self.state = state
        self.status = status

    def get_player_result(self) -> list:
        """Define the end of game will return the player's info for user"""
        res = []
        for player in self.all_players:
            if isinstance(player, Player):
                if player.no > self.green_team_num:
                    team_id = "blue"
                else:
                    team_id = "green"
                get_res = player.get_info_to_game_result()
                get_res["no"] = f"{team_id}_{player.no}P"
                get_res["state"] = self.state
                get_res["status"] = self.status
                get_res["used_frame"] = self.used_frame
                res.append(get_res)
        return res

    def check_collisions(self):
        if not self.is_through_wall:
            collide_with_walls(self.all_players, self.walls)
            collide_with_walls(self.all_players, self.unbreakable_walls)
            
        if not self.is_invincible:
            player_score_data = collide_with_bullets(self.all_players, self.bullets, self.green_team_num)
            for player, score in player_score_data.items():
                self.add_player_score(player, score)
            # TODO refactor stations

            supply_stations = []

            # Check collision between player and supply stations
            supply_stations.extend(collide_with_supply_stations(self.all_players, self.bullet_stations))
            supply_stations.extend(collide_with_supply_stations(self.all_players, self.oil_stations))

            # Check collision between bullet and supply stations
            supply_stations.extend(collide_with_supply_stations(self.bullets, self.bullet_stations))
            supply_stations.extend(collide_with_supply_stations(self.bullets, self.oil_stations))

            # Update stations position
            self.change_obj_pos(supply_stations)

        collide_with_bullets(self.unbreakable_walls, self.bullets)
        player_score_data = collide_with_bullets(self.walls, self.bullets)
        for player, score in player_score_data.items():
            self.add_player_score(player, score)

    def change_player_pos(self):
        for player in self.all_players:
            quadrant = player.quadrant
            self.empty_quadrant_pos_dict[quadrant].append(player.rect.topleft)
            if quadrant == 2 or quadrant == 3:
                player.quadrant = random.choice([2, 3])
            else:
                player.quadrant = random.choice([1, 4])
            quadrant = player.quadrant
            new_pos = self.empty_quadrant_pos_dict[quadrant].pop(
                random.randrange(len(self.empty_quadrant_pos_dict[quadrant])))
            set_topleft(player, new_pos)
            set_topleft(player.gun, new_pos)

    # TODO move method to Station
    def change_obj_pos(self, objs=None):
        if objs is None:
            return
        for obj in objs:
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
            bullet_speed = 30 * self.size_multiplier
            self.sound_controller.play_sound("shoot", 0.03, -1)
            bullet_travel_distance = int(600 * self.size_multiplier)
            init_data = create_construction(sprite.id, sprite.no, sprite.rect.center, (BULLET_SIZE[0] * self.size_multiplier, BULLET_SIZE[1] * self.size_multiplier))
            bullet = Bullet(init_data, rot=sprite.gun.get_rot(), margin=2, spacing=2, bullet_speed=bullet_speed, bullet_travel_distance=bullet_travel_distance
                            , play_rect_area=self.play_rect_area)
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
        for unbreakable_wall in self.unbreakable_walls:
            if isinstance(unbreakable_wall, Unbreakable_Wall):
                for data in unbreakable_wall.get_obj_init_data():
                    init_image_data.append(data)
                break
        
        img_id = ["team_a_bullet", "team_b_bullet"]
        for id in img_id:
            img_url = f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/{id}.svg"
            bullet_image_init_data = create_asset_init_data(id, BULLET_SIZE[0], BULLET_SIZE[1],
                                                            path.join(IMAGE_DIR, f"{id}.png"), img_url)
            init_image_data.append(bullet_image_init_data)
        border_image_init_data = create_asset_init_data("border", self.scene_width, WINDOW_HEIGHT,
                                                        path.join(IMAGE_DIR, "border.png"),
                                                        f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/border.svg")
        init_image_data.append(border_image_init_data)
        for player in self.all_players:
            if isinstance(player, Player):
                data = player.get_obj_init_data()
                init_image_data.append(data[0])
                init_image_data.append(data[1])
                break
        for gun in self.guns:
            if isinstance(gun, Gun):
                data = gun.get_obj_init_data()
                init_image_data.append(data[0])
                init_image_data.append(data[1])
                break
        for i in range(1, 4):
            team_a_lives = "team_a_lives"
            team_a_lives_image_init_data = create_asset_init_data(f"{team_a_lives}_{i}", LIVES_SIZE[0], LIVES_SIZE[1], path.join(IMAGE_DIR, f"{team_a_lives}_{i}.png"),
                                                                  f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/{team_a_lives}_{i}.svg")
            init_image_data.append(team_a_lives_image_init_data)
            team_b_lives = "team_b_lives"
            team_b_lives_image_init_data = create_asset_init_data(f"{team_b_lives}_{i}", LIVES_SIZE[0], LIVES_SIZE[1], path.join(IMAGE_DIR, f"{team_b_lives}_{i}.png"),
                                                                  f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/{team_b_lives}_{i}.svg")
            init_image_data.append(team_b_lives_image_init_data)
        return init_image_data

    def get_toggle_progress_data(self):
        toggle_data = []
        hourglass_index = 0
        hourglass_size = self.tileSize*20/50
        if self.is_manual:
            hourglass_index = self.used_frame // 10 % 15
        toggle_data.append(
            # create_image_view_data(image_id=f"hourglass_{hourglass_index}", x=0, y=2, width=20, height=20, angle=0))
            create_image_view_data(image_id=f"hourglass_{hourglass_index}", x=0, y=2, width=hourglass_size, height=hourglass_size, angle=0))
        x = 23
        y = 8
        for frame in range((self.frame_limit - self.used_frame) // int((30 * 2))):
            toggle_data.append(create_rect_view_data("frame", x, y, 3, 10, RED))
            x += 3.5
        # toggle_data.append(create_text_view_data(f"Frame: {self.frame_limit - self.used_frame}",
        #                                          self.width_center + self.width_center // 2 + 85, 8, RED,
        #                                          "24px Arial BOLD"))
        toggle_data.append(create_text_view_data(f"Frame: {self.frame_limit - self.used_frame}",
                                                 self.scene_width-165, 8, RED,
                                                 "24px Arial BOLD"))
        x = 24
        y = 20
        for score in range(min(self.team_green_score, self.team_blue_score)):
            toggle_data.append(create_rect_view_data(name="score", x=x, y=y, width=1, height=10, color=ORANGE))
            x += 1.5
            if x > self.width_center:
                if y == 32:
                    y = 44
                else:
                    y = 32
                x = 24
        for score in range(abs(self.team_green_score - self. team_blue_score)):
            if self.team_green_score > self.team_blue_score:
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
        # x = WINDOW_WIDTH - 125
        # y = WINDOW_HEIGHT - 40
        x = self.scene_width - 125
        y = self.scene_height - 40
        toggle_data.append(create_text_view_data(f"Score: {self.team_green_score}", x, y, DARKGREEN, "24px Arial BOLD"))
        # 2P
        x = 5
        # y = WINDOW_HEIGHT - 40
        y = self.scene_height - 40
        toggle_data.append(create_text_view_data(f"Score: {self.team_blue_score}", x, y, BLUE, "24px Arial BOLD"))
        for player in self.all_players:
            if isinstance(player, Player) and player.is_alive:
                # lives
                team_id = "team_a_lives" if player.id == 1 else "team_b_lives"
                color = DARKGREEN  if player.id == 1 else BLUE
                x = player.play_rect_area.midbottom[0] + 7 + (player.no - 1) * 60 if player.id == 1 \
                    else player.play_rect_area.midbottom[0] - (player.no - self.green_team_num) * 60
                y = player.play_rect_area.height + 73
                toggle_data.append(
                    create_text_view_data(f"{player.no}P", x - 5, y - 25, color, "22px Arial BOLD"))
                for live in range(1, player.lives+1):
                    toggle_data.append(create_image_view_data(f"{team_id}_{live}", x, y, LIVES_SIZE[0], LIVES_SIZE[1])) 
                    x += 10
                    y -= 10
        return toggle_data

    def get_toggle_with_bias_data(self):
        toggle_with_bias_data = []
        color = WHITE
        for player in self.all_players:
            if isinstance(player, Player) and player.is_alive:
                # number
                if player.no > self.green_team_num:
                    color = WHITE
                x = player.rect.x
                y = player.rect.y - 18
                toggle_with_bias_data.append(create_text_view_data(f"{player.no}P", x, y, color, "16px Arial BOLD"))
                team_id = "team_a"
                if player.no > self.green_team_num:
                    team_id = "team_b"
                # oil
                y = player.rect.bottom
                multiplier = self.tileSize / 50
                x = player.rect.x - 25 * (1 - multiplier)
                # toggle_with_bias_data.append(create_rect_view_data(f"{team_id}_oil", x, y, int(player.oil*0.5)*multiplier, 8*multiplier, ORANGE))
                toggle_with_bias_data.append(create_rect_view_data(f"{team_id}_oil", x, y, int(player.oil*0.5), 8, ORANGE))

                # power
                y = player.rect.bottom + 10
                # x = player.rect.midbottom - 4
                for power in range(player.power):
                    toggle_with_bias_data.append(create_rect_view_data(f"{team_id}_power", x+1, y, 3, 8, BLUE))
                    # toggle_with_bias_data.append(create_rect_view_data(f"{team_id}_power", x+1, y, 3*multiplier, 8*multiplier, BLUE))
                    x += 5

        return toggle_with_bias_data

    def get_ai_data_to_player(self):
        to_player_data = {}
        num = 0
        competitor_info = {1: [player.get_data_from_obj_to_game() for player in self.players_a if isinstance(player, Player)]
                           , 2: [player.get_data_from_obj_to_game() for player in self.players_b if isinstance(player, Player)]
                           }
        walls_info = [wall.get_data_from_obj_to_game() for wall in self.walls if isinstance(wall, Wall)]
        unbreak_wall_info = [wall.get_data_from_obj_to_game() for wall in self.unbreakable_walls if isinstance(wall, Unbreakable_Wall)]
        walls_info.extend(unbreak_wall_info)
        bullet_stations_info = [bullst_station.get_data_from_obj_to_game() for bullst_station in self.bullet_stations if
                                isinstance(bullst_station, Station)]
        oil_stations_info = [oil_station.get_data_from_obj_to_game() for oil_station in self.oil_stations if
                             isinstance(oil_station, Station)]
        bullets_info = [bullet.get_data_from_obj_to_game() for bullet in self.bullets if
                             isinstance(bullet, Bullet)]
        for player in self.players_a:
            if isinstance(player, Player):
                to_game_data = player.get_data_from_obj_to_game()
                to_game_data["used_frame"] = self.used_frame
                to_game_data["status"] = self.status
                to_game_data["teammate_info"] = competitor_info[1]
                to_game_data["competitor_info"] = competitor_info[2]
                to_game_data["walls_info"] = walls_info
                to_game_data["bullets_info"] = bullets_info
                to_game_data["bullet_stations_info"] = bullet_stations_info
                to_game_data["oil_stations_info"] = oil_stations_info
                to_game_data["size_multiplier"] = self.size_multiplier
                to_player_data[get_ai_name(num)] = to_game_data
                num += 1
        for player in self.players_b:
            if isinstance(player, Player):
                to_game_data = player.get_data_from_obj_to_game()
                to_game_data["used_frame"] = self.used_frame
                to_game_data["status"] = self.status
                to_game_data["teammate_info"] = competitor_info[2]
                to_game_data["competitor_info"] = competitor_info[1]
                to_game_data["walls_info"] = walls_info
                to_game_data["bullets_info"] = bullets_info
                to_game_data["bullet_stations_info"] = bullet_stations_info
                to_game_data["oil_stations_info"] = oil_stations_info
                to_game_data["size_multiplier"] = self.size_multiplier
                to_player_data[get_ai_name(num)] = to_game_data
                num += 1

        return to_player_data

    def get_bgm_data(self):
        return create_bgm_data("BGM.ogg", 0.1)

    def get_sound_data(self):
        return [create_sounds_data("shoot", "shoot.wav")
            , create_sounds_data("touch", "touch.wav")]

    def add_player_score(self, player_no: int, score: int):
        if not player_no or not score:
            return
        for player in self.all_players:
            if isinstance(player, Player) and player_no == player.no and player.lives >= 0:
                add_score(player, score)

    def debugging(self, is_debug: bool):
        self.obj_rect_list = []
        if not is_debug:
            return
        play_rect_area_points = [self.play_rect_area.topleft, self.play_rect_area.topright
                                 , self.play_rect_area.bottomright, self.play_rect_area.bottomleft
                                 , self.play_rect_area.topleft]

        for sprite in self.all_sprites:
            if isinstance(sprite, pygame.sprite.Sprite):
                top_left = sprite.rect.topleft
                points = [top_left, sprite.rect.topright, sprite.rect.bottomright
                    , sprite.rect.bottomleft, top_left]
                for index in range(len(points) - 1):
                    self.obj_rect_list.append(create_line_view_data("rect", *points[index], *points[index + 1], RED))
                    self.obj_rect_list.append(create_line_view_data("play_rect_area", *play_rect_area_points[index]
                                                                    , *play_rect_area_points[index + 1], RED))
