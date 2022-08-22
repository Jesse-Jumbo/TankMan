import pytmx


# Map 讀取地圖資料
class TiledMap:
    def __init__(self, filepath: str):
        tm = pytmx.TiledMap(filepath)
        self.tile_width = tm.tilewidth
        self.tile_height = tm.tileheight
        self.width = tm.width
        self.height = tm.height
        self.map_width = self.tile_width * self.width
        self.map_height = self.tile_height * self.height
        self.tmx_data = tm

    def create_init_obj(self, img_no: int, class_name, **kwargs) -> dict:
        obj_no = 0
        for layer in self.tmx_data.visible_layers:
            for x, y, gid, in layer:
                if isinstance(layer, pytmx.TiledTileLayer):
                    if gid != 0:  # 0代表空格，無圖塊
                        if layer.parent.tiledgidmap[gid] == img_no:
                            img_id = layer.parent.tiledgidmap[gid]
                            obj_no += 1
                            img_info = {"_id": img_id, "_no": obj_no,
                                        "x": x * self.tile_width, "y": y * self.tile_height,
                                        "width": self.tile_width, "height": self.tile_height}
                            obj = class_name(img_info, **kwargs)
                            return obj

    def create_init_obj_list(self, img_no: list or str, class_name, **kwargs) -> list:
        if type(img_no) != list:
            img_no = list(map(int, [img_no]))
        obj_result = []
        obj_no = 0
        for layer in self.tmx_data.visible_layers:
            for x, y, gid, in layer:
                if isinstance(layer, pytmx.TiledTileLayer):
                    if gid != 0:  # 0代表空格，無圖塊
                        if layer.parent.tiledgidmap[gid] in img_no:
                            img_id = layer.parent.tiledgidmap[gid]
                            obj_no += 1
                            img_info = {"_id": img_id, "_no": obj_no,
                                        "x": x * self.tile_width, "y": y * self.tile_height,
                                        "width": self.tile_width, "height": self.tile_height}
                            obj_result.append(class_name(img_info, **kwargs))
        return obj_result
