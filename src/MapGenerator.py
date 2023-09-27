from os import path
import random
import math
# from .env import PLAYER_1_IMG_NO, PLAYER_2_IMG_NO, WALL_IMG_NO, BULLET_STATION_IMG_NO, OIL_STATION_IMG_NO, UNBREAK_WALL_IMG_NO

"""map data numbers"""
PLAYER_1_IMG_NO = 1
PLAYER_2_IMG_NO = 2
WALL_IMG_NO = 3
BULLET_STATION_IMG_NO = 4
OIL_STATION_IMG_NO = 5
UNBREAK_WALL_IMG_NO = 6



PLAYER_NUM = 1
OIL_NUM = 2
BULLET_NUM = 2
UNBREAK_WALL_NUM = 8
MAP_DIR = path.join(path.dirname(__file__), "..", "asset", 'maps')
MAP_VERSION = "1.9"
TILED_VERSION = "1.9.2"
TILE_COUNT = 6

class MapGenerator:

    def __init__(self, green_team_num : int, blue_team_num : int, width : int, height : int) -> None:

        self.green_team_num = green_team_num
        self.blue_team_num = blue_team_num

        #height should be a factor of 600
        #default is 20, 12

        self.width = width
        self.height = height

        self.height_per_tile = math.floor(600/self.height)
        self.width_per_tile = self.height_per_tile

        self.screen_width = self.width * self.height_per_tile
        self.screen_height = 700

    def get_neighbour(self, x : int, y : int) -> list:
        neighbour = []
        if x > 0:
            neighbour.append((x-1, y))
        if x < self.width-1:
            neighbour.append((x+1, y))
        if y > 0:
            neighbour.append((x, y-1))
        if y < self.height-1:
            neighbour.append((x, y+1))
        return neighbour


    def getTileSize(self) -> int:
        return self.height_per_tile
    
    def getScreeenSize(self) -> tuple:
        return self.screen_width, self.screen_height


    def pos2index(self, x : int, y : int) -> int:
        return y * (self.width * 2 + 1) + x * 2

    def mirrored_pos(self, x : int, y : int) -> tuple:
        return self.width - x - 1, self.height - y - 1

    
    def random_pos(self, map_arr) -> tuple:
        random_x, random_y = random.randint(1, self.width-2), random.randint(1, self.height-2)
        mir_x, mir_y = self.mirrored_pos(random_x, random_y)
        while map_arr[random_y][random_x] != 0 or map_arr[mir_y][mir_x] != 0:
            random_x, random_y = random.randint(1, self.width-2), random.randint(1, self.height-2)
            mir_x, mir_y = self.mirrored_pos(random_x, random_y)

        return random_x, random_y
    
    def random_pos_no_neighbour(self, map_arr) -> tuple:
        rand_x, rand_y = self.random_pos(map_arr)
        while True:
            neighbour = self.get_neighbour(rand_x, rand_y)
            fail = False
            for x, y in neighbour:
                if map_arr[y][x] != 0:
                    fail = True
            if fail:
                rand_x, rand_y = self.random_pos(map_arr)
            else:
                break
        return rand_x, rand_y

    def generate_map_str(self) -> str:

        #generate default map[y][x]
        map_arr = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        for x in range(self.width):
            map_arr[0][x] = WALL_IMG_NO
            map_arr[self.height-1][x] = WALL_IMG_NO
        
        for y in range(self.height):
            map_arr[y][0] = WALL_IMG_NO
            map_arr[y][self.width-1] = WALL_IMG_NO

        if self.width % 2 == 1:
            for y in range(1, self.height-1):
                map_arr[y][self.width//2] = WALL_IMG_NO
        else:
            for y in range(1, self.height):
                if y < math.ceil(self.height/2):
                    map_arr[y][self.width//2-1] = WALL_IMG_NO
                else:
                    map_arr[y][self.width//2] = WALL_IMG_NO

        #add unbreakable wall
        for _ in range(UNBREAK_WALL_NUM):
            rand_x, rand_y = self.random_pos_no_neighbour(map_arr)
            mir_x, mir_y = self.mirrored_pos(rand_x, rand_y)
            map_arr[rand_y][rand_x] = UNBREAK_WALL_IMG_NO
            map_arr[mir_y][mir_x] = UNBREAK_WALL_IMG_NO

        #add player
        for _ in range(min(self.green_team_num, self.blue_team_num)):
            rand_x, rand_y = self.random_pos(map_arr)
            while rand_x < self.width // 2:
                rand_x, rand_y = self.random_pos(map_arr)
            mir_x, mir_y = self.mirrored_pos(rand_x, rand_y)

            map_arr[rand_y][rand_x] = PLAYER_1_IMG_NO
            map_arr[mir_y][mir_x] = PLAYER_2_IMG_NO

        #add remaining green team
        for _ in range(self.green_team_num - self.blue_team_num):
            rand_x, rand_y = self.random_pos(map_arr)
            while rand_x < self.width // 2:
                rand_x, rand_y = self.random_pos(map_arr)

            map_arr[rand_y][rand_x] = PLAYER_1_IMG_NO

        #add remaining blue team
        for _ in range(self.blue_team_num - self.green_team_num):
            rand_x, rand_y = self.random_pos(map_arr)
            while rand_x >= self.width // 2:
                rand_x, rand_y = self.random_pos(map_arr)

            map_arr[rand_y][rand_x] = PLAYER_2_IMG_NO
        
        #add bullet station
        for _ in range(BULLET_NUM):
            rand_x, rand_y = self.random_pos(map_arr)
            mir_x, mir_y = self.mirrored_pos(rand_x, rand_y)
            map_arr[rand_y][rand_x] = BULLET_STATION_IMG_NO
            map_arr[mir_y][mir_x] = BULLET_STATION_IMG_NO

        #add oil station
        for _ in range(OIL_NUM):
            rand_x, rand_y = self.random_pos(map_arr)
            mir_x, mir_y = self.mirrored_pos(rand_x, rand_y)
            map_arr[rand_y][rand_x] = OIL_STATION_IMG_NO
            map_arr[mir_y][mir_x] = OIL_STATION_IMG_NO

        map_str = ""
        
        for row in map_arr:
            for id in row:
                map_str += str(id) + ","
            map_str += "\n"
        map_str = map_str[:-2]

        return map_str
    
    def generate_map(self):
        map_name = f"map_{self.green_team_num}_v_{self.blue_team_num}.tmx"
        map_path = path.join(MAP_DIR, map_name)
        print(f'generate map at : {map_path}', flush=True)


        with open(map_path, "w") as file:
            #write map
            file.write(f"""\
<?xml version="1.0" encoding="UTF-8"?>
<map version="{MAP_VERSION}" tiledversion="{TILED_VERSION}" orientation="orthogonal" renderorder="right-down" width="{self.width}" height="{self.height}" tilewidth="{self.width_per_tile}" tileheight="{self.height_per_tile}" infinite="0" nextlayerid="2" nextobjectid="1">
 <tileset firstgid="1" name="TankManObj" tilewidth="{self.width_per_tile}" tileheight="{self.height_per_tile}" tilecount="{TILE_COUNT}" columns="{TILE_COUNT}">
  <image source="../image/TankManObj_new.png" width="{TILE_COUNT*50}" height="50"/>
 </tileset>
 <layer id="1" name="layer 1" width="{self.width}" height="{self.height}">
  <data encoding="csv">
{self.generate_map_str()}
  </data>
 </layer>
</map>
                """)
            
if __name__ == "__main__":
    map_generator = MapGenerator(1, 1, 20, 12)
    map_generator.generate_map()
    

