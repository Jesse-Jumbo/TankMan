from os import path
import pygame

'''width and height'''
WIDTH = 1320
HEIGHT = 660

'''environment data'''
FPS = 60

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
MAP_DIR = path.join(GAME_DIR, '..', "asset", 'maps')

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
BULLET_SIZE = pygame.Rect(0, 0, 8, 8)

"""all setting"""
DOWN_IMG = 'down'
RIGHT_IMG = 'right'
UP_IMG = 'up'
LEFT_IMG = 'left'

"""collide setting"""
WITH_PLAYER = 'player'

"""rect"""
PLAYRE_HIT_RECT = pygame.Rect(0, 0, 59, 59)
WALL_HIT_RECT = pygame.Rect(0, 0, 59, 59)
BULLET_HIT_RECT = pygame.Rect(0, 0, 8, 6)

"""speed"""
PLAYER_SPEED = 3

"""image"""
PLAYER_IMG_LIST = ["player_1P.png", "player_2P.png"]
WALL_IMG = "wall.png"

"""map data numbers"""
PLAYER_IMG_NO_LIST = [1, 2]
WALL_IMG_NO = 3

"""music"""
BGM = 'background_music.ogg/.wav/.mp3'
MENU_SND = 'MenuTheme.ogg/.wav/.mp3'

"""image url"""
PLAYER_URL = "https://github.com/Jesse-Jumbo/GameName/master/asset/image/player.png?raw=true"
BACKGROUND_URL = "https://github.com/Jesse-Jumbo/GameName/master/asset/image/background.jpg?raw=true"
WALL_UML = ["https://github.com/Jesse-Jumbo/GameName/master/asset/image/walls.png?raw=true"]

"""image path"""
PLAYER_IMG_PATH_LIST = [path.join(IMAGE_DIR, "player_1P.png"), path.join(IMAGE_DIR, "player_2P.png")]
WALL_IMG_PATH = path.join(IMAGE_DIR, "wall.png")
BULLET_IMG_PATH = path.join(IMAGE_DIR, "bullet.png")
