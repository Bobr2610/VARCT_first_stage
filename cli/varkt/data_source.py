class DataSource:

    def data(self,
             time: int) -> (float, float, float, float):
        pass

    def pause(self,
              interval: float):
        pass

    def is_end(self,
               time: int) -> bool:
        pass
