class Timer:
    time: int
    interval: float

    def __init__(self,
                 interval: float):
        self.time = 0
        self.interval = interval

    def update(self):
        self.time += self.interval

    def time(self):
        return self.time
