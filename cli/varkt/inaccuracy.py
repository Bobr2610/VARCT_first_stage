from .config import Config
from .data_source import DataSource


class Inaccuracy(DataSource):
    config: Config

    def __init__(self,
                 flight_data,
                 model_data,
                 config: Config):
        self.config = config

        self.flight_data = flight_data
        self.model_data = model_data

    def data(self,
             time: int) -> (float, float, float, float):
        flight_time = self.flight_data[str(time)]
        model_time = self.model_data[str(time)]

        result = []
        for data_type in ['height', 'speed', 'angle', 'fuel']:
            result.append(self.inaccuracy(flight_time[data_type], model_time[data_type]))

        return tuple(result)

    def inaccuracy(self,
                   first: float,
                   second: float):
        if second == 0:
            second = 0.001

        return first / second

    def pause(self,
              interval: float):
        return

    def is_end(self,
               time: int) -> bool:
        return time >= self.config.data['plotting_time']


