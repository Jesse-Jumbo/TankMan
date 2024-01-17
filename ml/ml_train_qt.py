"""
The template of the main script of the machine learning process
"""
import pygame
import os
import pickle
from datetime import datetime
import numpy as np
from ml.Environment import Environment as env
from ml.QT import QLearningTable
import pandas as pd


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

        self.env = env()
        self.action = self.env.action
        self.state = [self.env.observation]    
        self.state_ = [self.env.observation]         

        self.QT = QLearningTable(actions=list(range(self.env.n_actions)))
        
        folder_path = './ml/save'
        os.makedirs(folder_path, exist_ok=True)

        keep_training = False
        if keep_training:
            self.QT.q_table =pd.read_pickle('.\\ml\\save\\qtable.pickle')
        else:
            self.QT.q_table.to_pickle('.\\ml\\save\\qtable.pickle')

        self.action_mapping = [["NONE"], ["TURN_RIGHT"], ["FORWARD"], ["BACKWARD"], ["AIM_LEFT"], ["AIM_RIGHT"], ["SHOOT"]]            
         

    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        
        
        if scene_info["status"] != "GAME_ALIVE":            
            return "RESET"
        
        self.env.set_scene_info(scene_info)        
        observation, reward, done, info = self.env.step(self.action)


        self.state_ = [observation]
        action = self.QT.choose_action(str(self.state))
        
        self.QT.learn(str(self.state), self.action, reward, str(self.state_))

        self.state = self.state_
        self.action = action           
        command = self.action_mapping[action]
        
        return command


    def reset(self):
        """
        Reset the status
        """
        print(f"reset Game {self.side}")
        self.QT.q_table.to_pickle('.\\ml\\save\\qtable.pickle')

    