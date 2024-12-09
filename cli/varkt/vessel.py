from time import sleep

import krpc
import krpc.services.spacecenter

from .data_source import DataSource


class Vessel(DataSource):
    connection: krpc.Client
    vessel: krpc.services.spacecenter.Vessel
    body: krpc.services.spacecenter.CelestialBody
    plotting_time: int

    def __init__(self,
                 name: str,
                 plotting_time: int):
        self.connection = krpc.connect(name=name)
        self.vessel = self.connection.space_center.active_vessel
        self.body = self.vessel.orbit.body
        self.plotting_time = plotting_time

    def data(self,
             time: int):
        height = self.vessel.flight(self.body.orbital_reference_frame).mean_altitude
        speed = self.vessel.flight(self.body.orbital_reference_frame).speed
        angle = self.vessel.flight(self.vessel.surface_reference_frame).pitch

        fuel = 0
        for stage in range(self.vessel.control.current_stage + 1):
            for part in self.vessel.parts.in_decouple_stage(stage):
                for resource in part.resources.all:
                    if resource.name == 'SolidFuel' or resource.name == 'LiquidFuel':
                        fuel += resource.amount

        return height, speed, angle, fuel

    def pause(self,
              interval: int):
        sleep(interval)

    def is_end(self,
               time: int) -> bool:
        return time >= self.plotting_time
