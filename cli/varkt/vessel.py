from time import sleep

import krpc
import krpc.services.spacecenter

from .data_source import DataSource


class Vessel(DataSource):
    connection: krpc.Client
    vessel: krpc.services.spacecenter.Vessel
    body: krpc.services.spacecenter.CelestialBody

    def __init__(self, name: str):
        self.connection = krpc.connect(name=name)
        self.vessel = self.connection.space_center.active_vessel
        self.body = self.vessel.orbit.body

    def data(self, time: int):
        height = self.vessel.flight(self.body.orbital_reference_frame).mean_altitude
        speed = self.vessel.flight(self.body.orbital_reference_frame).speed
        angle = self.vessel.flight(self.body.orbital_reference_frame).roll
        mass = self.vessel.mass
        resources = self.vessel.resources  # TODO: Удалить?

        return height, speed, angle, mass

    def pause(self, interval: int):
        sleep(interval)
