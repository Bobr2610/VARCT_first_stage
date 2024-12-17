from .config import Config
from .plotting import Plotter

class Difference:
    config: Config
    times: [int]
    flight_data: ([int], [int], [int], [int])
    model_data: ([int], [int], [int], [int])

    def __init__(self,
                 config: Config,
                 times: [int],
                 flight_data: ([int], [int], [int], [int]),
                 model_data: ([int], [int], [int], [int])):
        self.config = config
        self.times = times
        self.flight_data = flight_data
        self.model_data = model_data

    def draw(self):
        plotter = Plotter()
        plotter.draw_once(self.times,
                          (
                              self.flight_data['height'],
                              self.flight_data['speed'],
                              self.flight_data['angle'],
                              self.flight_data['mass']
                          ),
                          'g')
        plotter.draw_once(self.times,
                          (
                              self.model_data['height'],
                              self.model_data['speed'],
                              self.model_data['angle'],
                              self.model_data['mass']
                          ),
                          'b')
        plotter.pause(5)
        plotter.save('difference.png')
