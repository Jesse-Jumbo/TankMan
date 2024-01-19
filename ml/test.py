
from ml.env import *
import math
import numpy as np

class Bullet():
    def __init__(self) -> None:
        pass

    def is_wall_in_bullet_range(self, tank_pos, gun_angle, walls, detection_distance):
        for wall in walls:            
            if self.will_hit_target(tank_pos, gun_angle, {"x":wall["x"], "y":wall["y"]}, detection_distance):
                return True    
        return False

    def is_target_in_bullet_range(self, tank_pos, gun_angle, target_pos, detection_distance):
        return self.will_hit_target(tank_pos, gun_angle, target_pos, detection_distance)

    def will_hit_target(self, tank_pos, gun_angle, target_pos, detection_distance):    
        distance = math.sqrt((tank_pos["x"] - target_pos["x"]) ** 2 + (tank_pos["y"] - target_pos["y"]) **2)
        
        if detection_distance < distance:
            return False
        
        angle_rad = math.atan2(target_pos["y"] - tank_pos["y"], target_pos["x"] - tank_pos["x"])            
        gun_rad = np.radians(180 - gun_angle) 
        toarance_rad = math.atan2(WALL_WIDTH/2, distance)
        
        
        return abs(gun_rad - angle_rad) < toarance_rad        
    
