import numpy as np
import scipy

from .data_source import DataSource


class Model(DataSource):
    # m_start = 267_000
    m_0 = 500
    m_0_1 = 172_000
    m_0_2 = 94_000
    m_1_1 = 13_600
    m_1_2 = 7_495
    i_1_e = 252
    i_1_v = 308
    i_2_e = 243
    i_2_v = 309
    # f_t_1_e = 3_216
    # f_t_1_v = 3_924
    # f_t_2_e = 735.5
    # f_t_2_v = 921
    # g = 9.81
    t_0 = 315
    t_p_1 = 16
    t_p_2 = 113
    t_1 = 122
    t_2 = 280
    # t_full = 280
    m_1 = 1300
    m_2 = 308.5
    phi = np.pi / 180
    n = 2
    k = 0.9

    plotting_time: int

    def __init__(self,
                 plotting_time: int):
        self.plotting_time = plotting_time

    def height(self,
               time: int):
        return scipy.integrate.quad(lambda t: np.cos((t < self.t_p_1) * 0 +
                                                     (self.t_p_1 <= t <= self.t_p_2) * self.k * (np.pi / 2) *
                                                     ((t - self.t_p_1) / (self.t_p_2 - self.t_p_1)) +
                                                     (t > self.t_p_2) * self.k * (np.pi / 2)) *
                                              self.speed(t),
                                    0,
                                    time)[0]

    def speed(self,
              time: int):
        i_i = lambda i: ((self.i_1_e + self.i_1_v) / 2) if i == 1 else ((self.i_2_e + self.i_2_v) / 2)
        m_i = lambda i: self.m_1 if i == 1 else self.m_2
        m_0_i = lambda i: self.m_0_1 if i == 1 else self.m_0_2
        m_1_i = lambda i: self.m_1_1 if i == 1 else self.m_1_2
        t_i = lambda i: self.t_1 if i == 1 else self.t_2

        partial = 0
        for i in range(1, self.n + 1):
            partial_1 = time > sum([t_i(j) for j in range(1, i)])

            sub_expression_up = self.m_0 + sum([m_0_i(j) for j in range(i, self.n + 1)])
            sub_expression_down = (self.m_0 +
                                   max(m_1_i(i), m_0_i(i) - m_i(i) * (time - sum([t_i(j) for j in range(1, i)]))) +
                                   sum([m_0_i(j) for j in range(i + 1, self.n + 1)]))
            partial_2 = scipy.constants.g * i_i(i) * np.log(sub_expression_up / sub_expression_down)

            partial += partial_1 * partial_2

        return partial - scipy.integrate.quad(lambda t: scipy.constants.g * (-np.cos(self.angle(t))), 0, time)[0]

    def angle(self,
              time: int):
        return ((time < self.t_p_1) * np.pi +
                (self.t_p_1 <= time <= self.t_p_2) *
                max(np.pi / 2 + self.phi,
                    np.pi - (np.pi / 2) * ((time - self.t_p_1) / (self.t_p_2 - self.t_p_1))) +
                (time > self.t_p_2) * (np.pi / 2 + self.phi))

    prev_mass = m_0_1 + m_0_2
    prev_time = 0
    def fuel(self,
             time: int):
        m_v = 0
        if time <= self.t_1:
            m_v += self.m_1
        if time <= self.t_2:
            m_v += self.m_2

        self.prev_mass -= (time - self.prev_time) * m_v
        self.prev_time = time
        return self.prev_mass

    def data(self,
             time: int) -> (float, float, float, float):
        n_angle = ((time < self.t_p_1) * 0 +
                   (self.t_p_1 <= time <= self.t_p_2) * (np.pi / 2) * ((time - self.t_p_1) / (self.t_p_2 - self.t_p_1)) +
                   (time > self.t_p_2) * (np.pi / 2))

        return self.height(time), self.speed(time), 90 - n_angle, self.fuel(time)

    def pause(self,
              interval: float):
        pass

    def is_end(self,
               time: int) -> bool:
        return time >= self.plotting_time
