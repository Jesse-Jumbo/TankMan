from os import path
import pygame

'''width and height'''
WIDTH = 1920
HEIGHT = 1080

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
LEFT_CMD = "MOVE_LEFT"
RIGHT_CMD = "MOVE_RIGHT"
UP_CMD = "MOVE_UP"
DOWN_CMD = "MOVE_DOWN"

'''data path'''
GAME_DIR = path.dirname(__file__)
IMAGE_DIR = path.join(GAME_DIR, "..", "asset", "image")
SOUND_DIR = path.join(GAME_DIR, "..", "asset", "sound")
MAP_DIR = path.join(GAME_DIR, '..', 'maps')

'''BG View'''
TITLE = "GameName!"
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

"""all setting"""
DOWN_IMG = 'down'
RIGHT_IMG = 'right'
UP_IMG = 'up'
LEFT_IMG = 'left'

"""collide setting"""
WITH_MOB = 'mob'
WITH_PLAYER = 'player'

"""rect"""
PLAYRE_HIT_RECT = pygame.Rect(0, 0, 60, 60)
MOB_HIT_RECT = pygame.Rect(0, 0, 60, 60)
WALL_HIT_RECT = pygame.Rect(0, 0, 60, 60)

"""speed"""
PLAYER_SPEED = 2.0
MOB_SPEED = 1.0

"""image"""
PLAYER_IMG = "player.png"
MOB_IMG = "mob.png"
WALL_IMG = "wall.png"

"""map data numbers"""
PLAYER_IMG_NO = 0
MOB_IMG_NO_LIST = [0]
WALL_IMG_NO_LIST = [0]

"""music"""
BGM = 'background_music.ogg/.wav/.mp3'
MENU_SND = 'MenuTheme.ogg/.wav/.mp3'

"""image url"""
PLAYER_URL = "https://github.com/Jesse-Jumbo/GameName/master/asset/image/player.png?raw=true"
BACKGROUND_URL = "https://github.com/Jesse-Jumbo/GameName/master/asset/image/background.jpg?raw=true"
MOB_URL = ["https://github.com/Jesse-Jumbo/GameName/master/asset/image/mobs.png?raw=true"]
WALL_UML = ["https://github.com/Jesse-Jumbo/GameName/master/asset/image/walls.png?raw=true"]
