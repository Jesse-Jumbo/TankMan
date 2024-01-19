
from ml.env import *
import math
import numpy as np

class Bullet():
    def __init__(self) -> None:
        pass
    def is_wall_in_bullet_range(self, tank_pos, gun_angle, walls):
        is_wall_in_bullet_range = False
        
        
        for wall in walls:            
            if self.will_hit_target(tank_pos, gun_angle, {"x":wall["x"], "y":wall["y"]}):
                is_wall_in_bullet_range = True
                break
        
        return is_wall_in_bullet_range

    def will_hit_target(self, tank_pos, gun_angle, wall_pos):
        
        distance = math.sqrt((tank_pos["x"] - wall_pos["x"]) ** 2 + (tank_pos["y"] - wall_pos["y"]) **2)
        if BULLET_TRAVEL_DISTANCE < distance:
            return False
        
        angle_rad = math.atan2(wall_pos["y"] - tank_pos["y"], wall_pos["x"] - tank_pos["x"])
        
        angle_deg = math.degrees(angle_rad)
        # print("_______________________")
        # print("tank_pos",tank_pos)
        # print("wall_pos", wall_pos)
        # print("angle", angle_deg)
        # print("gun_angle", -gun_angle+180)
        
        gun_rad = np.radians(-gun_angle+180) 
        toarance_rad = math.atan2(WALL_WIDTH/2, distance)
        

        
        if abs(gun_rad - angle_rad) < toarance_rad:
            return True
        else:
            return False