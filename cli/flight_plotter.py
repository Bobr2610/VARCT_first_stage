import sys

from varkt.collector import Collector
from varkt.config import Config
from varkt.vessel import Vessel


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Нет имени файла конфигурации!')

    config = Config.from_file(sys.argv[1])

    vessel = Vessel(config)

    collector = Collector(vessel,
                          config)
    collector.collect()
