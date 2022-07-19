import sys
from os import path
from games.TankMan.src.TankMan import TankMan

GAME_SETUP = {
    "game": TankMan,
}

sys.path.append(path.dirname(__file__))
