"""
The template of the main script of the machine learning process
"""
import random
import pygame
import os
import pickle
from datetime import datetime
from src.env import IS_DEBUG
import numpy as np


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

        with open(os.path.join(os.path.dirname(__file__),"save", "KNN_classification.pickle"), "rb") as f:
            self.model = pickle.load(f)


    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        # print(keyboard)
        
        if scene_info["status"] != "GAME_ALIVE":            
            return "RESET"
        user_x = scene_info["x"]
        user_y = scene_info["y"]
        user_angle = scene_info["angle"]
        competitor_y = scene_info["competitor_info"][0]["y"]
        user_gun_angle = scene_info["gun_angle"]
        
        x = np.array([user_x, user_y, user_angle, competitor_y, user_gun_angle]).reshape((1, -1))   
        y = self.model.predict(x)        
        command = y.tolist()

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
        self.data = {"scene_info":[], "command":[]}

    