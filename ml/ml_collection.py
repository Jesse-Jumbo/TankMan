"""
The template of the main script of the machine learning process
"""
import random
import pygame
import numpy
import os
import pickle
from datetime import datetime
from ml.env import *
from ml.test import *
import numpy as np
import math

class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.side = ai_name
        print(f"Initial Game {ai_name} ml script")
        self.time = 0
        self.user_x = 800
        # 儲存動作
        self.scene_info = []
        self.commands = []
        self.data = {"scene_info":[], "command":[]}

        # 環境狀況

        # 最大訓練長度
        self.max_count = 2500

        # 成功率
        self.game_count = 0
        self.game_win_count = 0


    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        # print(keyboard)
        
        if scene_info["status"] != "GAME_ALIVE":            
            return "RESET"

        command = self.__rule(scene_info)        
        return command

    def reset(self):
        """
        Reset the status
        """
        print(f"reset Game {self.side}")
        self.data["scene_info"] = self.scene_info
        self.data["command"] = self.commands

        filepath = "log"
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        print("--------------------------------------------------------------------")
        
        
        self.game_count += 1
        with open(os.path.join(os.path.dirname(__file__), \
                '../log/scene_info_{:%Y_%m_%d_%H_%M_%S}.pickle'.format(datetime.now())),\
                    'wb') as f:
                pickle.dump(self.data, f)
        
        self.scene_info = []
        self.commands = []
        

    def __rule(self, scene_info):
        command = []
        TORRANCE = 8
        target_pos = {"x":scene_info["competitor_info"][0]["x"], "y":scene_info["competitor_info"][0]["y"]}
        tank_pos = {"x": scene_info["x"], "y": scene_info["y"]}
        tank_angle = scene_info["angle"]
        tank_gun_angle = scene_info["gun_angle"]

        bullet = Bullet()
        print("tank_gun_angle", tank_gun_angle)
        is_wall_in_bullet_range = bullet.is_wall_in_bullet_range(tank_pos, tank_gun_angle, scene_info["walls_info"], 50)
        print(is_wall_in_bullet_range)
        is_target_in_bullet_range = bullet.is_target_in_bullet_range(tank_pos, tank_gun_angle, target_pos, BULLET_TRAVEL_DISTANCE)
        
        if abs(tank_pos["y"] - target_pos["y"]) > TORRANCE:
            if tank_angle != 90:
                command.append("TURN_RIGHT")
            elif is_wall_in_bullet_range:
                command.append("SHOOT")
            else:    
                if tank_pos["y"] < target_pos["y"]:
                    command.append("FORWARD")
                else:
                    command.append("BACKWARD")
        
        elif abs(tank_pos["x"] - target_pos["x"]) > TORRANCE:
            if tank_angle != 0:
                command.append("TURN_RIGHT")
            elif is_target_in_bullet_range or is_wall_in_bullet_range:                       
                command.append("SHOOT")
            else:
                if tank_pos["x"] < target_pos["x"]:                    
                    command.append("BACKWARD")
                else:
                    command.append("FORWARD")
        
        # 儲存資料
        self.scene_info.append(scene_info)
        self.commands.append(command)

        if len(self.scene_info) > self.max_count:
            return "RESET"
        
        if len(command) == 0:
            command.append("NONE")
            
        return command