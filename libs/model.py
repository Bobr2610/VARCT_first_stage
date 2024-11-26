from data_source import DataSource


class Model(DataSource):

    def height(self):
        pass

    def speed(self):
        pass

    def angle(self):
        pass

    def mass(self):
        pass

    def data(self, time: int):
        return self.height(), self.speed(), self.angle(), self.mass()

    def pause(self, interval: int):
        pass
