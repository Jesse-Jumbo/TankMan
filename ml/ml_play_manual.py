"""
The template of the main script of the machine learning process
"""

import pygame
from ml.test import *

class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        """
        Constructor

        @param ai_name A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.side = ai_name
        print(f"Initial Game {ai_name} ml script")
        self.time = 0

    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        # if scene_info["used_frame"] == 1:
        #     print(f"{self.side}_scene_info_{scene_info.keys()}")
        #     if scene_info["id"] == "1P":
        #         print(f'1P_competitor_info{scene_info["competitor_info"]}')
        #     else:
        #         print(f'2P_competitor_info{scene_info["competitor_info"]}')
        # print(keyboard)
        if scene_info["status"] != "GAME_ALIVE":
            # print(scene_info)
            return "RESET"

        command = []
        if self.side == "1P":
            if pygame.K_RIGHT in keyboard:
                command.append("TURN_RIGHT")
            elif pygame.K_LEFT in keyboard:
                command.append("TURN_LEFT")
            elif pygame.K_UP in keyboard:
                command.append("FORWARD")
            elif pygame.K_DOWN in keyboard:
                command.append("BACKWARD")

            if pygame.K_z in keyboard:
                command.append("AIM_LEFT")
            elif pygame.K_x in keyboard:
                command.append("AIM_RIGHT")

            if pygame.K_m in keyboard:
                command.append("SHOOT")
            # debug
            if pygame.K_b in keyboard:
                command.append("DEBUG")
            # paused
            if pygame.K_t in keyboard:
                command.append("PAUSED")
        elif self.side == "2P" or self.side == "4P":
            if pygame.K_d in keyboard:
                command.append("TURN_RIGHT")
            elif pygame.K_a in keyboard:
                command.append("TURN_LEFT")
            elif pygame.K_w in keyboard:
                command.append("FORWARD")
            elif pygame.K_s in keyboard:
                command.append("BACKWARD")

            if pygame.K_q in keyboard:
                command.append("AIM_LEFT")
            elif pygame.K_e in keyboard:
                command.append("AIM_RIGHT")

            if pygame.K_f in keyboard:
                command.append("SHOOT")
        bullet = Bullet()
        # print(scene_info["gun_angle"])
        # print(bullet.is_wall_in_bullet_range({"x": scene_info["x"], "y": scene_info["y"]}, scene_info["gun_angle"], scene_info["walls_info"], 200))
        if not command:
            command.append("NONE")
        
        return command

    def reset(self):
        """
        Reset the status
        """
        print(f"reset Game {self.side}")
