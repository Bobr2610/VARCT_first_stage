from .config import Config
from .data_source import DataSource
from .plotting import Plotter
from .timer import Timer


class Collector:
    data_source: DataSource
    config: Config

    def __init__(self, data_source: DataSource, config: Config):
        self.data_source = data_source
        self.config = config

    def collect(self):
        plotter = Plotter()
        timer = Timer(self.config.update_interval)

        while True:
            plotter.update(timer.time, *self.data_source.data(timer.time))
            plotter.pause(self.config.pause_interval)

            timer.update()

            self.data_source.pause(self.config.pause_interval)
