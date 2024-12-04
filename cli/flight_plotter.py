from varkt.collector import Collector
from varkt.config import Config
from varkt.vessel import Vessel


if __name__ == '__main__':
    vessel = Vessel('Sputnik-1')
    config = Config(1, 1)

    collector = Collector(vessel, config)
    collector.collect()
