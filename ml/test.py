
from ml.env import *
import math
import numpy as np

class Bullet():
    def __init__(self) -> None:
        pass

    def is_wall_in_bullet_range(self, tank_pos, gun_angle, walls):
        for wall in walls:            
            if self.will_hit_target(tank_pos, gun_angle, {"x":wall["x"], "y":wall["y"]}):
                return True    
        return False

    def will_hit_target(self, tank_pos, gun_angle, wall_pos):    
        distance = math.sqrt((tank_pos["x"] - wall_pos["x"]) ** 2 + (tank_pos["y"] - wall_pos["y"]) **2)
        if BULLET_TRAVEL_DISTANCE < distance:
            return False
        
        angle_rad = math.atan2(wall_pos["y"] - tank_pos["y"], wall_pos["x"] - tank_pos["x"])            
        gun_rad = np.radians(180 - gun_angle) 
        toarance_rad = math.atan2(WALL_WIDTH/2, distance)
        
        
        return abs(gun_rad - angle_rad) < toarance_rad        
        