import json

from .config import Config
from .plotting import Plotter


class Inaccuracy:
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
        inaccuracies = {'height': [],
                        'speed': [],
                        'angle': [],
                        'mass': []}
        for i in range(3, len(self.flight_data['height'])):
            height_inaccuracy = self.inaccuracy(self.flight_data['height'][i],
                                                self.model_data['height'][i])
            speed_inaccuracy = self.inaccuracy(self.flight_data['speed'][i],
                                               self.model_data['speed'][i])
            angle_inaccuracy = self.inaccuracy(self.flight_data['angle'][i],
                                               self.model_data['angle'][i])
            mass_inaccuracy = self.inaccuracy(self.flight_data['mass'][i],
                                              self.model_data['mass'][i])

            inaccuracies['height'].append(height_inaccuracy)
            inaccuracies['speed'].append(speed_inaccuracy)
            inaccuracies['angle'].append(angle_inaccuracy)
            inaccuracies['mass'].append(mass_inaccuracy)

        print(f'Среднее отклонение высоты: {sum(inaccuracies['height']) / len(inaccuracies['height'])}')
        print(f'Среднее отклонение скорости: {sum(inaccuracies['speed']) / len(inaccuracies['speed'])}')
        print(f'Среднее отклонение угла: {sum(inaccuracies['angle']) / len(inaccuracies['angle'])}')
        print(f'Среднее отклонение массы: {sum(inaccuracies['mass']) / len(inaccuracies['mass'])}')

        plotter = Plotter(False)
        plotter.draw_once(self.times[3:],
                          (
                              inaccuracies['height'],
                              inaccuracies['speed'],
                              inaccuracies['angle'],
                              inaccuracies['mass']
                          ),
                          'g',
                          'Погрешность')
        plotter.pause(5)
        plotter.save('inaccuracy.png')

        data = {}
        for i, time in enumerate(self.times[3:]):
            data[time] = {
                'height': inaccuracies['height'][i],
                'speed': inaccuracies['speed'][i],
                'angle': inaccuracies['angle'][i],
                'mass': inaccuracies['mass'][i]
            }

        with open('inaccuracy.json', 'w') as file:
            json.dump(data,
                      file)

    def inaccuracy(self,
                   first: float,
                   second: float):
        if second == 0:
            second = 0.001

        return first / second
