import random


class MLPlay:
    def __init__(self):
        self.game_info = []
        self.player_2P_info = []
        self.player_1P_info = []
        print("Initial ml script")
        self.time = 0

    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """
        # print(scene_info)
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        self.time += 1
        if self.time % 30 == 0:
            command = random.randrange(9)
        else:
            command = None
        if command == 1:
            return ["TURN_RIGHT"]
        elif command == 2:
            return ["TURN_LEFT"]
        elif command == 3:
            return ["FORWARD"]
        elif command == 4:
            return ["BACKWARD"]
        elif command == 5:
            return ["TURN_RIGHT", "SHOOT"]
        elif command == 6:
            return ["TURN_LEFT", "SHOOT"]
        elif command == 7:
            return ["FORWARD", "SHOOT"]
        elif command == 8:
            return ["BACKWARD", "SHOOT"]
        elif command == 0:
            return ["SHOOT"]

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")

