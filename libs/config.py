class Config:
    update_interval: int
    pause_interval: int

    def __init__(self, update_interval: int, pause_interval: int):
        self.update_interval = update_interval
        self.pause_interval = pause_interval

    def update_interval(self):
        return self.update_interval

    def pause_interval(self):
        return self.pause_interval
