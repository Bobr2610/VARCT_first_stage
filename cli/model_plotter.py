from varkt.collector import Collector
from varkt.config import Config
from varkt.model import Model


if __name__ == '__main__':
    model = Model(400)
    config = Config(5,
                    0.1,
                    'model')

    collector = Collector(model,
                          config)
    collector.collect()
