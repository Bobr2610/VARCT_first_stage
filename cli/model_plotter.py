from varkt.collector import Collector
from varkt.config import Config
from varkt.model import Model


if __name__ == '__main__':
    model = Model()
    config = Config(20, 0.1)

    collector = Collector(model, config)
    collector.collect()
