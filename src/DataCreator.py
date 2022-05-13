class DataCreator:
    def __init__(self):
        self.id = "id"
        self.x = "x"
        self.y = "y"
        self.width = "width"
        self.height = "height"
        self.angle = "angle"
        self.path = "path"
        self.url = "url"
        self.content = "content"
        self.color = "color"
        self.font_style = "font_style"

    # 不確定是否要存在
    def create_image_progress_data(self, _id: str, x: int, y: int, width: int, height: int, angle: 0):
        return {self.id: _id, self.x: x, self.y: y, self.width: width, self.height: height, self.angle: angle}

    def create_image_init_data(self, _id: str, width: int, height: int, path: str, url: str):
        return {self.id: _id, self.width: width, self.height: height, self.path: path, self.url: url}

    def create_text_data(self, content: str, x: int, y: int, color: str, font_style: str):
        return {self.content: content, self.x: x, self.y: y, self.color: color, self.font_style: font_style}
