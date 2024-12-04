class Config:
    update_interval: float
    pause_interval: float
    file: str

    def __init__(self,
                 update_interval: float,
                 pause_interval: float,
                 file: str):
        self.update_interval = update_interval
        self.pause_interval = pause_interval
        self.file = file

    def update_interval(self) -> float:
        return self.update_interval

    def pause_interval(self) -> float:
        return self.pause_interval

    def file(self) -> str:
        return self.file
