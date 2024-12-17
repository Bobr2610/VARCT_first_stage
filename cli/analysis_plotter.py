import json
import sys

from varkt.difference import Difference
from varkt.config import Config
from varkt.inaccuracy import Inaccuracy

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Нет имени файла конфигурации!')

    config = Config.from_file(sys.argv[1])

    with open(config.data['flight_data_file']) as file:
        flight_data = json.load(file)

    with open(config.data['model_data_file']) as file:
        model_data = json.load(file)

    times = [int(time) for time in flight_data.keys()]
    flight = {'height': [flight_data[str(time)]['height'] for time in times],
              'speed': [flight_data[str(time)]['speed'] for time in times],
              'angle': [flight_data[str(time)]['angle'] for time in times],
              'mass': [flight_data[str(time)]['mass'] for time in times]}
    model = {'height': [model_data[str(time)]['height'] for time in times],
             'speed': [model_data[str(time)]['speed'] for time in times],
             'angle': [model_data[str(time)]['angle'] for time in times],
             'mass': [model_data[str(time)]['mass'] for time in times]}

    inaccuracy = Inaccuracy(config,
                            times,
                            flight,
                            model)
    inaccuracy.draw()

    difference = Difference(config,
                            times,
                            flight,
                            model)
    difference.draw()
