import json

from varkt.collector import Collector
from varkt.config import Config
from varkt.inaccuracy import Inaccuracy

if __name__ == '__main__':
    with open('flight.json') as file:
        flight_json = json.load(file)

    with open('model.json') as file:
        model_json = json.load(file)

    inaccuracy = Inaccuracy(flight_json,
                            model_json,
                            400)
    config = Config(5,
                    0.1,
                    'inaccuracy')

    collector = Collector(inaccuracy, config)
    collector.collect()
