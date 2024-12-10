import json
import sys

from varkt.collector import Collector
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

    inaccuracy = Inaccuracy(flight_data,
                            model_data,
                            config)

    collector = Collector(inaccuracy,
                          config)
    collector.collect()
