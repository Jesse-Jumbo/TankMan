class DataCreator:
    def __init__(self):
        pass

    def create_image_progress_data(self, _id: str, x: int, y: int, width: int, height: int, angle: 0):
        return {"_id": _id, "x": x, "y": y, "width": width, "height": height, "angle": angle}

    def create_image_init_data(self, _id: str, width: int, height: int, path: str, url: str):
        return {"_id": _id, "width": width, "height": height, "path": path, "url": url}

    def create_text_data(self, content: str, x: int, y: int, color: str, font_style: str):
        return {"content": content, "x": x, "y": y, "color": color, "font_style": font_style}
