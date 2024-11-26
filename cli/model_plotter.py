from libs.collector import Collector
from libs.config import Config
from libs.model import Model


if __name__ == '__main__':
    model = Model()
    config = Config(1, 0)

    collector = Collector(model, config)
    collector.collect()
