import json


class Config:
    def __init__(self,
                 data):
        self.data = data

    @staticmethod
    def from_file(name: str):
        with open(name) as file:
            data = json.load(file)

        config = Config(data)

        return config
