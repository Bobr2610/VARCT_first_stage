from .data_source import DataSource


class Inaccuracy(DataSource):
    def __init__(self,
                 flight_data,
                 model_data,
                 plotting_time):
        self.flight_data = flight_data
        self.model_data = model_data
        self.plotting_time = plotting_time

    def data(self,
             time: int) -> (float, float, float, float):
        flight_time = self.flight_data[str(time)]
        model_time = self.model_data[str(time)]

        flight_height, flight_speed, flight_angle, flight_mass = (flight_time['height'],
                                                                  flight_time['speed'],
                                                                  flight_time['angle'],
                                                                  flight_time['mass'])

        model_height, model_speed, model_angle, model_mass = (model_time['height'],
                                                              model_time['speed'],
                                                              model_time['angle'],
                                                              model_time['mass'])

        return (model_height / (0.001 if flight_height == 0 else flight_height),
                model_speed / (0.001 if flight_speed == 0 else flight_speed),
                model_angle / (0.001 if flight_angle == 0 else flight_angle),
                model_mass / (0.001 if flight_mass == 0 else flight_mass))


    def pause(self,
              interval: float):
        return

    def is_end(self,
               time: int) -> bool:
        return time >= self.plotting_time


