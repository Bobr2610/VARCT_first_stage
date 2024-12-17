from time import sleep

import krpc
import krpc.services.spacecenter

from .config import Config
from .data_source import DataSource


class Vessel(DataSource):
    config: Config

    connection: krpc.Client
    vessel: krpc.services.spacecenter.Vessel
    body: krpc.services.spacecenter.CelestialBody

    def __init__(self,
                 config: Config):
        self.config = config

        self.connection = krpc.connect(name=self.config.data['host'])
        self.vessel = self.connection.space_center.active_vessel
        self.body = self.vessel.orbit.body

    def data(self,
             time: int):
        height = self.vessel.flight(self.body.orbital_reference_frame).mean_altitude
        speed = self.vessel.flight(self.body.orbital_reference_frame).speed
        angle = self.vessel.flight(self.vessel.surface_reference_frame).pitch
        mass = self.vessel.mass

        return height, speed, angle, mass

    def pause(self,
              interval: int):
        sleep(interval)

    def is_end(self,
               time: int) -> bool:
        return time >= self.config.data['plotting_time']
