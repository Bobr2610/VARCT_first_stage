from varkt.collector import Collector
from varkt.config import Config
from varkt.vessel import Vessel


if __name__ == '__main__':
    vessel = Vessel('Sputnik-1',
                    400)
    config = Config(1,
                    1,
                    'flight')

    collector = Collector(vessel,
                          config)
    collector.collect()
