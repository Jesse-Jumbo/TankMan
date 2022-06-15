"""
The template of the main script of the machine learning process
"""

import pygame


class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.side = side
        print(f"Initial TankMan {side} ml script")
        self.time = 0

    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        # print(scene_info)
        # print(keyboard)
        if scene_info["status"] != "GAME_ALIVE":
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

            if pygame.K_SPACE in keyboard:
                command.append("SHOOT")
        else:
            if pygame.K_d in keyboard:
                command.append("TURN_RIGHT")
            elif pygame.K_a in keyboard:
                command.append("TURN_LEFT")
            elif pygame.K_w in keyboard:
                command.append("FORWARD")
            elif pygame.K_s in keyboard:
                command.append("BACKWARD")

            if pygame.K_f in keyboard:
                command.append("SHOOT")

        return command

    def reset(self):
        """
        Reset the status
        """
        print(f"reset TankMan {self.side}")
