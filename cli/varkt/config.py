class Config:
    update_interval: float
    pause_interval: float

    def __init__(self, update_interval: float, pause_interval: float):
        self.update_interval = update_interval
        self.pause_interval = pause_interval

    def update_interval(self) -> float:
        return self.update_interval

    def pause_interval(self) -> float:
        return self.pause_interval
