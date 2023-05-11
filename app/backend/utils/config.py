DEFAULT_MIN_INTERVAL = 3


class Config:
    def __init__(self):
        self.yolo_enabled = False
        self.min_interval = int(DEFAULT_MIN_INTERVAL)


config = Config()
