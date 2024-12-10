import json

from .config import Config
from .data_source import DataSource
from .plotting import Plotter
from .timer import Timer


class Collector:
    data_source: DataSource
    config: Config

    def __init__(self,
                 data_source: DataSource,
                 config: Config):
        self.data_source = data_source
        self.config = config

    def collect(self):
        data = {}

        plotter = Plotter()
        timer = Timer(self.config)

        while not self.data_source.is_end(timer.time):
            record = self.data_source.data(timer.time)

            data[timer.time] = {
                'height': record[0],
                'speed': record[1],
                'angle': record[2],
                'fuel': record[3]
            }

            plotter.update(timer.time, *record)
            plotter.pause(self.config.data['pause_interval'])

            timer.update()

            self.data_source.pause(self.config.data['pause_interval'])

        with open(self.config.data['plotter_name'] + '.json', 'w') as file:
            json.dump(data,
                      file)

        plotter.save(self.config.data['plotter_name'] + '.png')
