class Timer:
    time: int
    interval: int

    def __init__(self, interval: int):
        self.time = 0
        self.interval = interval

    def update(self):
        self.time += self.interval

    def time(self):
        return self.time
