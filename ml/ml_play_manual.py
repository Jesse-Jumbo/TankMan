"""
The template of the main script of the machine learning process
"""

import pygame


class MLPlay:
    def __init__(self):
        print("Initial ml script")

    def update(self, scene_info: dict, keyboard: list, *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        # print(scene_info)
        # print(keyboard)
        if keyboard is None:
            keyboard = []
            return "RESET"

        command = []

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

        return command

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
