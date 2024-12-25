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
                 title: str,
                 x_label: str,
                 y_label: str):
        self.x = []
        self.y = []
        self.axes = axes
        self.graphic = self.axes.plot(self.x,
                                      self.y)[0]
        self.graphic.figure.set_figheight(4)
        self.graphic.figure.set_figwidth(4)
        self.axes.set_xlabel(x_label, fontsize=11)
        self.axes.set_ylabel(y_label, fontsize=11)

    def update(self,
               x_element: int,
               y_element: int,
               label: str):
        self.x.append(x_element)
        self.y.append(y_element)
        self.graphic.remove()
        self.graphic = self.axes.plot(self.x,
                                      self.y,
                                      label=label)[0]
        self.axes.legend()

    def draw(self,
             x_elements: [int],
             y_elements: [int],
             color: str,
             label: str):
        self.axes.plot(x_elements,
                       y_elements,
                       color,
                       label=label)
        self.axes.legend()


class Plotter:
    height_graphic: Graphic
    speed_graphic: Graphic
    angle_graphic: Graphic
    mass_graphic: Graphic

    def __init__(self, is_si = True):
        plt.ion()

        _, ax = plt.subplots(nrows=2,
                             ncols=2)

        self.height_graphic = Graphic(ax[0, 0],
                                      'Высота',
                                      'Время (с)',
                                      'Высота (м)' if is_si else 'Отношение')
        self.speed_graphic = Graphic(ax[0, 1],
                                     'Скорость',
                                     'Время (с)',
                                     'Скорость (м/с)' if is_si else 'Отношение')
        self.angle_graphic = Graphic(ax[1, 0],
                                     'Угол',
                                     'Время (с)',
                                     'Угол (градусы)' if is_si else 'Отношение')
        self.mass_graphic = Graphic(ax[1, 1],
                                    'Масса',
                                    'Время (с)',
                                    'Масса (кг)' if is_si else 'Отношение')

    def update(self,
               time: int,
               height: int,
               speed: int,
               angle: int,
               mass: int,
               label: str):
        self.height_graphic.update(time,
                                   height,
                                   label)
        self.speed_graphic.update(time,
                                  speed,
                                  label)
        self.angle_graphic.update(time,
                                  angle,
                                  label)
        self.mass_graphic.update(time,
                                 mass,
                                 label)

    def draw_once(self,
                  times: [int],
                  data: ([int], [int], [int], [int]),
                  color: str,
                  label: str):
        self.height_graphic.draw(times, data[0], color, label)
        self.speed_graphic.draw(times, data[1], color, label)
        self.angle_graphic.draw(times, data[2], color, label)
        self.mass_graphic.draw(times, data[3], color, label)


    def pause(self,
              interval: float):
        plt.pause(interval)

    def save(self,
             name: str):
        plt.savefig(name)
