import pytmx


# Map 讀取地圖資料
class TiledMap:
    def __init__(self, filepath: str):
        print(filepath)
        tm = pytmx.load_pygame(filepath, pixealpha=True)
        self.width = tm.tilewidth
        self.height = tm.tileheight
        self.tmx_data = tm

    def create_obj_init_data(self, img_no_list: list):
        img_result = []
        obj_no = 0
        for layer in self.tmx_data.visible_layers:
            for x, y, gid, in layer:
                if isinstance(layer, pytmx.TiledTileLayer):
                    if gid != 0:  # 0代表空格，無圖塊
                        if layer.parent.tiledgidmap[gid] in img_no_list:
                            img_id = layer.parent.tiledgidmap[gid]
                            obj_no += 1
                            img_info = {"_id": img_id, "_no": obj_no,
                                        "x": x * self.width, "y": y * self.height,
                                        "width": self.width, "height": self.height}
                            img_result.append(img_info)
        return img_result
