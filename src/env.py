# 圖片來源
"""
https://opengameart.org/content/simple-2d-tank
https://opengameart.org/content/motor-oil-container
https://opengameart.org/content/simple-shooter-icons
https://opengameart.org/content/upgrade-symbols
"""
# sound sours
"""
BGM: https://opengameart.org/content/commando-team-action-loop-cut
SHOOT: https://opengameart.org/content/random-low-quality-sfx
"""

from os import path

import pygame

'''width and height'''
WIDTH = 1320
HEIGHT = 660

'''environment data'''
FPS = 60
SHOOT_COOLDOWN = FPS // 4

'''color'''
BLACK = "#000000"
WHITE = "#ffffff"
RED = "#ff0000"
YELLOW = "#ffff00"
GREEN = "#00ff00"
GREY = "#8c8c8c"
BLUE = "#0000ff"
LIGHT_BLUE = "#21A1F1"
CYAN_BLUE = "#00FFFF"
PINK = "#FF00FF"
DARKGREY = "#282828"
LIGHTGREY = "#646464"
BROWN = "#643705"
FOREST = "#22390A"
MAGENTA = "#FF00FF"
MEDGRAY = "#4B4B4B"

'''command'''
LEFT_CMD = "TURN_LEFT"
RIGHT_CMD = "TURN_RIGHT"
FORWARD_CMD = "FORWARD"
BACKWARD_CMD = "BACKWARD"
SHOOT = "SHOOT"

'''data path'''
GAME_DIR = path.dirname(__file__)
IMAGE_DIR = path.join(GAME_DIR, "..", "asset", "image")
SOUND_DIR = path.join(GAME_DIR, "..", "asset", "sound")
MAP_DIR = path.join(GAME_DIR, "..", "asset", 'maps')

'''BG View'''
TITLE = "TankMan!"
BG_COLOR = DARKGREY
TILE_X_SIZE = 60
TILE_Y_SIZE = 60
TILE_SIZE = 60
GRID_WIDTH = WIDTH / TILE_X_SIZE
GRID_HEIGHT = HEIGHT / TILE_Y_SIZE
TEXT_SIZE = 100

'''window pos'''
WIDTH_CENTER = WIDTH / 2
HEIGHT_CENTER = HEIGHT / 2

'''object size'''
ALL_OBJECT_SIZE = pygame.Rect(0, 0, 60, 60)
BULLET_SIZE = (13, 13)

"""all setting"""
DOWN_IMG = 'down'
RIGHT_IMG = 'right'
UP_IMG = 'up'
LEFT_IMG = 'left'

"""collide setting"""
WITH_PLAYER = 'player'

"""map data numbers"""
PLAYER_IMG_NO_LIST = [1, 2]
WALL_IMG_NO_LIST = [3]
BULLET_STATION_IMG_NO_LIST = [4]
OIL_STATION_IMG_NO_LIST = [5]

"""music"""
BGM = 'background_music.ogg/.wav/.mp3'
MENU_SND = 'MenuTheme.ogg/.wav/.mp3'

"""image url"""
PLAYER_URL = {"1P": "https://github.com/Jesse-Jumbo/TankMan/blob/main/asset/image/player_1P.png",
              "2P": "https://github.com/Jesse-Jumbo/TankMan/blob/main/asset/image/player_2P.png"}
WALL_URL = {"3.5": "https://github.com/Jesse-Jumbo/TankMan/blob/main/asset/image/wall_3.5.png",
            "3.4": "https://github.com/Jesse-Jumbo/TankMan/blob/main/asset/image/wall_3.4.png",
            "3.3": "https://github.com/Jesse-Jumbo/TankMan/blob/main/asset/image/wall_3.3png",
            "3.2": "https://github.com/Jesse-Jumbo/TankMan/blob/main/asset/image/wall_3.2.png",
            "3.1": "https://github.com/Jesse-Jumbo/TankMan/blob/main/asset/image/wall_3.1.png"}
BULLETS_URL = {3: "https://github.com/Jesse-Jumbo/TankMan/blob/main/asset/image/bullets_3.png",
               2: "https://github.com/Jesse-Jumbo/TankMan/blob/main/asset/image/bullets_2.png",
               1: "https://github.com/Jesse-Jumbo/TankMan/blob/main/asset/image/bullets_1.png", }
OIL_URL = {3: "https://github.com/Jesse-Jumbo/TankMan/blob/main/asset/image/oil_3.png",
           2: "https://github.com/Jesse-Jumbo/TankMan/blob/main/asset/image/oil_2.png",
           1: "https://github.com/Jesse-Jumbo/TankMan/blob/main/asset/image/oil_1.png", }
BULLET_URL = "https://github.com/Jesse-Jumbo/TankMan/blob/main/asset/image/bullet.png"

"""image path"""
PLAYER_IMG_PATH_DICT = {}
for i in range(1, 3):
    PLAYER_IMG_PATH_DICT[f"{i}P"] = path.join(IMAGE_DIR, f"player_{i}P.png")
WALL_IMG_PATH_DICT = {}
for i in range(5, 0, -1):
    key = f"3.{i}"
    WALL_IMG_PATH_DICT[key] = path.join(IMAGE_DIR, f"wall_{key}.png")
BULLET_IMG_PATH = path.join(IMAGE_DIR, "bullet.png")

BULLET_STATION_IMG_PATH_DICT = {}
OIL_STATION_IMG_PATH_DICT = {}
for i in range(3, 0, -1):
    BULLET_STATION_IMG_PATH_DICT[i] = path.join(IMAGE_DIR, f"bullets_{i}.png")
    OIL_STATION_IMG_PATH_DICT[i] = path.join(IMAGE_DIR, f"oil_{i}.png")
