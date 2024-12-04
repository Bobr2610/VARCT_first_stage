from varkt.collector import Collector
from varkt.config import Config
from varkt.model import Model


if __name__ == '__main__':
    model = Model()
    config = Config(1, 0.5)

    collector = Collector(model, config)
    collector.collect()
