class Config:
    update_interval: float
    pause_interval: float
    plotter_name: str

    def __init__(self,
                 update_interval: float,
                 pause_interval: float,
                 plotter_name: str):
        self.update_interval = update_interval
        self.pause_interval = pause_interval
        self.plotter_name = plotter_name

    def update_interval(self) -> float:
        return self.update_interval

    def pause_interval(self) -> float:
        return self.pause_interval

    def plotter_name(self) -> str:
        return self.plotter_name
