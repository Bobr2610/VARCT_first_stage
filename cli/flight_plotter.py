from libs.collector import Collector
from libs.config import Config
from libs.vessel import Vessel


if __name__ == '__main__':
    vessel = Vessel('Sputnik-1')
    config = Config(1, 1)

    collector = Collector(vessel, config)
    collector.collect()
