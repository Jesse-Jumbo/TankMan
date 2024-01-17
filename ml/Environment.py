import math
from collections import OrderedDict

class Environment():
    def __init__(self) -> None:                                                                        
        self.action_mapping = [["NONE"], ["TURN_RIGHT"], ["FORWARD"], ["BACKWARD"], ["AIM_LEFT"], ["AIM_RIGHT"], ["SHOOT"]]
        self.n_actions = len(self.action_mapping)
        
        self.action = 0 
        self.observation = 0
        self.pre_reward = 0
    
    def set_scene_info(self, Scene_info: dict):
        """
        Stores the given scene information into the environment.

        Parameters:
        scene_info (dict): A dictionary containing environment information.
        """
        self.scene_info = Scene_info        
    
    def reset(self):
        """
        Resets the environment and returns the initial observation.

        Returns:
        observation: The initial state of the environment after reset.
        """
        observation = self.__get_obs(self.scene_info)

        return observation
    
    def step(self, action: int):   
        """
        Executes a given action in the environment and returns the resulting state.

        Parameters:
        action (int): The action to be performed, representing the squid's movement.

        Returns:
        observation: The current state of the environment after the action.
        reward (int): The reward obtained as a result of performing the action.
        done (bool): Indicates whether the game has ended (True if ended, False otherwise).
        info (dict): Additional information about the current state.
        """
        reward = 0
        observation = self.__get_obs(self.scene_info)                  
        
        reward = self.__get_reward(action, observation)
                
        done = self.scene_info["status"] != "GAME_ALIVE"            

        info = {}

        return observation, reward, done, info
    
    def __get_obs(self, scene_info):      
        FaceToUp = 0                 
        if scene_info["angle"] == 0:
            FaceToUp = "LEFT"       
        elif scene_info["angle"] == 45:     
            FaceToUp = "DOWNLEFT"
        elif scene_info["angle"] == 90:
            FaceToUp = "DOWN"
        elif scene_info["angle"] == 135:
            FaceToUp = "DOWNRIGHT"
        elif scene_info["angle"] == 180:
            FaceToUp = "RIGHT"
        elif scene_info["angle"] == 225:
            FaceToUp = "UPRIGHT"
        elif scene_info["angle"] == 270:
            FaceToUp = "UP"
        elif scene_info["angle"] == 315:
            FaceToUp = "UPLEFT"

        observation = {"FaceToUp": FaceToUp}
            
        return observation
        
        
    
    def __get_reward(self, action: int , observation: int):
        reward = 0
        if observation["FaceToUp"] != "UP":
            if self.action_mapping[action] == "TURN_RIGHT" :
                reward += 10
            else:
                reward -= 100
        elif observation["FaceToUp"] == "UP":
            if self.action_mapping[action] == "TURN_RIGHT":
                reward -= 100
            else:
                reward += 100

        print(f"reward: {reward:5d} obs: {observation} action: {self.action_mapping[action]}")

        return reward

    def __find_closest_wall(self, user_pos, walls):
        min_distance = float('inf')
        closest_wall = None

        for wall in walls:
            distance = self.__calculate_distance(user_pos, wall)
            if distance < min_distance:
                min_distance = distance
                closest_wall = wall

        return closest_wall
    
    def __calculate_distance(self, point1: list, point2: list)->float:        
        return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
    