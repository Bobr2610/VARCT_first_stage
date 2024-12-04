from typing import List

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.lines import Line2D


class Graphic:
    x: List[int]
    y: List[int]
    axes: Axes
    graphic: Line2D

    def __init__(self,
                 axes: Axes,
                 title: str):
        self.x = []
        self.y = []
        self.axes = axes
        self.axes.set_title(title)
        self.graphic = self.axes.plot(self.x,
                                      self.y)[0]

    def update(self,
               x_element: int,
               y_element: int):
        self.x.append(x_element)
        self.y.append(y_element)
        self.graphic.remove()
        self.graphic = self.axes.plot(self.x,
                                      self.y)[0]


class Plotter:
    height_graphic: Graphic
    speed_graphic: Graphic
    angle_graphic: Graphic
    mass_graphic: Graphic

    def __init__(self):
        plt.ion()

        _, ax = plt.subplots(nrows=2,
                             ncols=2)

        self.height_graphic = Graphic(ax[0, 0],
                                      'height')
        self.speed_graphic = Graphic(ax[0, 1],
                                     'speed')
        self.angle_graphic = Graphic(ax[1, 0],
                                     'angle')
        self.mass_graphic = Graphic(ax[1, 1],
                                    'mass')

    def update(self,
               time: int,
               height: int,
               speed: int,
               angle: int,
               mass: int):
        self.height_graphic.update(time,
                                   height)
        self.speed_graphic.update(time,
                                  speed)
        self.angle_graphic.update(time,
                                  angle)
        self.mass_graphic.update(time,
                                 mass)

    def pause(self, interval: float):
        plt.pause(interval)
