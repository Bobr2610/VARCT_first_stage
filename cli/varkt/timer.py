from .config import Config


class Timer:
    config: Config

    time: int

    def __init__(self,
                 config: Config):
        self.config = config

        self.time = 0

    def update(self):
        self.time += self.config.data['update_interval']

    def time(self):
        return self.time
