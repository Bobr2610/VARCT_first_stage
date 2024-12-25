import math

import numpy as np
import scipy

from .config import Config
from .logging import logging

class Model:

    config: Config

    m_0 = 53 * 10 ** 3 # масса ракет вначале
    m_1 = 34 * 10 ** 3 # масса первой ступени с топливом
    m_2 = 18.5 * 10 ** 3 # масса второй ступени с топливом
    t_1 = 60 # время работы первой ступени
    t_2 = 450 # время работы второй ступени
    I_1 = 1582 # удельный импульс первой ступени (с)
    I_2 = 383 # удельный импульс второй ступени (с)
    g = scipy.constants.g
    p_1_min = 161.2
    p_1_max = 161.2
    p_2_min = 37
    p_2_max = 37
    G = 6.67 * 10 ** -11
    M_e = 5.29 * 10 ** 22
    H_e = 600 * 10 ** 3

    dt = 1

    database = []
    results = []

    def time_db(self):
        return self.database[-1][0]

    def height_db(self):
        return self.database[-1][1]

    def speed_db(self):
        return self.database[-1][2]

    def angle_db(self):
        return self.database[-1][3]

    def mass_db(self):
        return self.database[-1][4]

    def x_db(self):
        return self.database[-1][5]

    def y_db(self):
        return self.database[-1][6]

    def speed_x_db(self):
        return self.database[-1][7]

    def speed_y_db(self):
        return self.database[-1][8]

    def __init__(self,
                 config):
        self.config = config

        self.results = self.modeling()
        for i in range(len(self.results)):
            self.results[i][2] = 90 - self.results[i][2] * (180 / np.pi) # перевод радиан в градусы

    def modeling(self):
        time = 0

        height = 0
        speed = 0
        angle = 0
        mass = self.m_0

        x = 0
        y = self.H_e
        speed_x = 0
        speed_y = 0


        while time < self.config.data['plotting_time']:
            self.database.append([time, height, speed, angle, mass, x, y, speed_x, speed_y])

            time += self.dt

            speed_x += self.speed_x(time) * self.dt
            speed_y += self.speed_y(time) * self.dt
            speed = math.sqrt(speed_x ** 2 + speed_y ** 2)
            x += self.speed_x_db() * self.dt
            y += self.speed_y_db() * self.dt
            height = self.y_db() - self.H_e
            angle = self.angle(time)
            mass = self.mass(time)

        return [row[1:5] for row in self.database]

    @logging('speed_x')
    def speed_x(self,
                time):
        return (self.P(time) - self.R()) * math.sin(self.angle_db()) / self.mass_db()

    @logging('speed_y')
    def speed_y(self,
                time):
        return ((self.P(time) - self.R()) * math.cos(self.angle_db()) - self.gravitation(time)) / self.mass_db()

    @logging('angle')
    def angle(self,
              time):
        if time < 16:
            return 0
        elif 16 <= time < 66:
            return (time - 16) * (71 * (np.pi / 180) / 49)
        elif 66 <= time < 200:
            return (71 * np.pi / 180) + (time - 66) * (19 * (np.pi / 180) / 134)
        else:
            return np.pi / 2

    @logging('mass')
    def mass(self,
             time):
        return self.m_0 - self.mass_1(time) - self.mass_2(time)

    # t_i - время работы i-ой ступени
    # m_i - масса i-ой ступени
    @logging('mass_1')
    def mass_1(self,
               time):
        if time >= self.t_1:
            return self.m_1

        return scipy.integrate.quad(self.V_f1, 0, time)[0]

    @logging('mass_2')
    def mass_2(self,
               time):
        if time >= self.t_2:
            return self.m_2

        return scipy.integrate.quad(self.V_f2, 0, time)[0]

    @logging('V_f1')
    def V_f1(self,
             time):
        return self.P_1(time) / (self.I_1 * self.g)

    @logging('V_f2')
    def V_f2(self,
             time):
        return self.P_2(time) / (self.I_2 * self.g)

    @logging('P_1')
    def P_1(self,
            time):
        if time >= self.t_1:
            return 0

        return (self.p_1_min + (self.p_1_max - self.p_1_min) / self.t_1 * time) * 10 ** 3

    @logging('P_2')
    def P_2(self,
            time):
        if time >= self.t_2:
            return 0

        return (self.p_2_min + (self.p_2_max - self.p_2_min) / self.t_2 * time) * 10 ** 3

    @logging('P')
    def P(self,
          time):
        return (self.P_1(time) + self.P_2(time)) * time

    @logging('gravitation')
    def gravitation(self, time):
        return (self.G * (self.mass_db() * self.M_e)) / (self.y_db() ** 2)

    temperature_table = [
        [[0, 11], -6.5, 288, 1030 * 10 ** 2],
        [[11, 20], 0.0, 216, 229.8 * 10 ** 2],
        [[20, 32], 1.0, 216, 55.3 * 10 ** 2],
        [[32, 47], 2.8, 227, 8.7 * 10 ** 2],
        [[47, 51], 0.0, 270, 1.1 * 10 ** 2],
        [[51, 71], -2.8, 270, 0.6 * 10 ** 2],
        [[71, 85], -2.0, 216, 0.03 * 10 ** 2]
    ]

    def get_temperature_row(self,
                            height):
        for row in self.temperature_table:
            H_r, _, _, _ = row

            if H_r[0] <= height < H_r[1]:
                return row

    @logging('temperature')
    def temperature(self,
                    height):
        if 0 <= height <= 3_000:
            temperature = 288.2 - 3.2 * height * 1e-3
        elif 3_000 <= height <= 11_000:
            temperature = 268.7 - 6.5 * (height * 1e-3 - 3)
        elif 11_000 <= height <= 20_000:
            temperature = 216.7
        elif 20_000 <= height <= 32_000:
            temperature = 216.7 + (height * 1e-3 - 20)
        elif 32_000 <= height <= 40_000:
            temperature = 228.5 + 2.75 * (height * 1e-3 - 32)
        elif 40_000 <= height <= 50_000:
            temperature = 250.4 + 2 * (height * 1e-3 - 40)
        elif 50_000 <= height <= 60_000:
            temperature = 270.7 - 2.3 * (height * 1e-3 - 50)
        elif 60_000 <= height <= 80_000:
            temperature = 247 - 2.45 * (height * 1e-3 - 60)
        elif 80_000 <= height <= 100_000:
            temperature = 198.6 - 0.1 * (height * 1e-3 - 80)
        elif 100_000 <= height <= 150_000:
            temperature = 196.6 + 8.62 * (height * 1e-3 - 100)
        else:
            temperature = 627.6

        return temperature

    @logging('pressure')
    def pressure(self,
                 height):
        H_r, L_i, T_i, P_i = self.get_temperature_row(height)

        if L_i != 0.0:
            return P_i * ((T_i / (T_i + L_i * (height - H_r[0]))) ** (34.163 / L_i))
        else:
            return P_i * math.exp((-34.163 * (height - H_r[0])) / T_i)

    @logging('plotnost')
    def plotnost(self,
                 height):
        M = 28.98
        R = 8.31

        return (self.pressure(height) * M) / (R * self.temperature(height))

    @logging('C_x')
    def C_x(self,
            speed,
            height):
        T = self.temperature(height)
        v_s = 20.055 * ((T + 273.15) ** 0.5)
        M = speed / v_s

        if M < 1:
            return 0.2
        elif 1 <= M < 1.5:
            return (M - 1) * (0.5 - 0.3)
        else:
            return 0.45

    @logging('R')
    def R(self):
        p_e = 101_325
        nu = 0.029
        area = 1.95 ** 2 * np.pi
        c_f = 0.42

        height = self.height_db()
        speed = self.speed_db()

        temperature = self.temperature(height)
        pressure = p_e * math.exp(-nu * self.g * height / (scipy.constants.R * temperature))
        env_density = nu * pressure / (scipy.constants.R * temperature)
        resistance = area * env_density * (speed ** 2) * 0.5 * c_f

        return resistance

    def data(self,
             time: int):
        return self.results[time]

    def pause(self,
              interval: float):
        return

    def is_end(self,
               time: int) -> bool:
        return time >= self.config.data['plotting_time']


# import math
#
# import numpy as np
# import scipy.constants
#
# from .config import Config
# from .data_source import DataSource
#
#
# class Model(DataSource):
#     config: Config
#
#     G = scipy.constants.G #
#     M_1 = 53 * 10 ** 3
#     M_2 = 18.9 * 10 ** 3
#     m_1 = 34 * 10 ** 3
#     m_2 = 18.5 * 10 ** 3
#     m_1_ = 2380
#     m_2_ = 12.7 * 10 ** 3
#     m_2__ = 1480
#     I_1 = 1582
#     I_2 = 383
#     T_1 = 161.2
#     T_2 = 37
#     M_e = 5.97 * 10 ** 24
#     t_1 = 60
#     t_2 = 64
#     t_3 = 525
#     t_4 = 560
#     t_p_1 = 14
#     t_p_2 = 65
#     t_p_3 = 260
#     t_p_4 = 535
#     g = scipy.constants.g
#
#     def __init__(self,
#                  config: Config):
#         self.config = config
#
#         self.database = self.modeling()
#
#     def engine_power_1(self,
#                        time):
#         return self.T_1
#
#     def engine_power_2(self,
#                        time):
#         return self.T_2
#
#     def acceleration_x(self,
#                        time):
#         partial =  ((time < self.t_1) * self.engine_power_2(time) +
#                     (time >= self.t_1) * self.engine_power_1(time)) * math.sin(self.angle(time))
#
#         return partial / self.mass(time)
#
#     def acceleration_y(self,
#                        time):
#         partial = ((time >= self.t_1) * self.engine_power_2(time) +
#                    (time < self.t_1) * self.engine_power_1(time)) * math.cos(self.angle(time))
#
#         return partial / self.mass(time) - self.g
#
#     def mass(self,
#              time):#,
#              #height):
#         first = ((time < self.t_1) *
#                  (self.M_1 -
#                   (self.m_1 - self.m_1_) / self.t_1 * time -
#                   (self.m_2 - self.m_2_) / self.t_1 * time))
#
#         second = ((time >= self.t_1) *
#                   (self.M_2 - (self.m_2_ - self.m_2__) / self.t_2 * time))
#
#         return first + second
#
#     def angle(self,
#               time):
#         first = (time < self.t_p_1) * 0
#         second = ((self.t_p_1 <= time <= self.t_p_2) *
#                   (7 * np.pi / 18 * (time - self.t_p_1) / (self.t_p_2 - self.t_p_1)))
#         third = ((self.t_p_2 < time <= self.t_p_3) *
#                  (7 * np.pi / 18))
#         four = ((self.t_p_3 <= time <= self.t_p_4) *
#                 (7 * np.pi / 18 + np.pi / 30 * (time - self.t_p_3) / (self.t_p_4 - self.t_p_3)))
#
#         return first + second + third + four
#
#     def speed(self,
#               time):
#         return ((self.acceleration_x(time) * time) ** 2 +
#                 (self.acceleration_y(time) * time) ** 2) ** 0.5
#
#     def modeling(self):
#         dt = 1
#
#         database = []
#         time = 0
#         while time <= self.config.data['plotting_time']:
#             speed = self.speed(time)
#             height = scipy.integrate.quad(lambda t: self.speed(time), 0, time)[0]
#             angle = self.angle(time)
#             mass = self.mass(time)
#
#             print(time, height, speed, 180 / np.pi * angle, mass)
#             database.append([time, height, speed, 180 / np.pi * angle, mass])
#
#             time += dt
#
#         return database
#
#     def data(self,
#              time: int):
#         return self.database[time][1:]
#
#     def pause(self,
#               interval: float):
#         return
#
#     def is_end(self,
#                time: int) -> bool:
#         return time >= self.config.data['plotting_time']

# class Model(DataSource):
#     config: Config
#
#     # m_start = 267_000
#     m_start = 55000
#     m_0 = 500
#     m_0_1 = 172_000
#     m_0_2 = 94_000
#     m_1_1 = 13_600
#     m_1_2 = 7_495
#     i_1_e = 252
#     i_1_v = 308
#     i_2_e = 243
#     i_2_v = 309
#     f_t_1_e = 1583.55 * 1000
#     f_t_1_v = 1583.55 * 1000
#     f_t_2_e = 363.02 * 1000
#     f_t_2_v = 363.02 * 1000
#     # f_t_1_e = 3_216
#     # f_t_1_v = 3_924
#     # f_t_2_e = 735.5
#     # f_t_2_v = 921
#     t_0 = 315
#     t_p_1 = 16
#     t_p_2 = 113
#     t_1 = 120
#     t_2 = 280
#     t_full = 280
#     m_1 = 1300
#     m_2 = 308.5
#     phi = np.pi / 180
#
#     G = scipy.constants.gravitational_constant
#     H = 8500 # TODO
#     earth_mass = 5.97 * 10 ** 24
#     karman_line = 100000
#     h_c = 6371 * 10 ** 3
#     c_d = 0.3
#     r_0 = 1.23
#     a = 26.5
#     v_0_x = 0
#     v_0_y = 0
#     r_0_x = 0
#     r_0_y = 6371 * 10 ** 3
#
#     n = 2
#     k = 0.9
#
#     # prev_r = (r_0_x ** 2 + r_0_y ** 2) ** 0.5
#
#     plotting_time: int
#
#     def __init__(self,
#                  config: Config):
#         self.config = config
#
#     # r(t)
#     def gravitation(self,
#                     time: int):
#         return self.G * self.mass(time) * self.earth_mass / self.r(time) ** 2
#
#     # NORM
#     def drag(self,
#              time: int):
#         return 0
#         # ro = self.r_0 * math.e ** (-self.height(time) / self.H)
#         #
#         # return 1 / 2 * ro * self.c_d * self.a * self.speed(time) ** 2
#
#     # NORM
#     def engine(self,
#                time):
#         f_engine = 0
#
#         if time < self.t_p_2:
#             f_engine += (self.f_t_2_e + self.f_t_2_v) / 2
#             # if self.height(time) < self.karman_line:
#             #     f_engine += self.f_t_2_e
#             # else:
#             #     f_engine += self.f_t_2_v
#
#         if time < self.t_p_1:
#             f_engine += (self.f_t_1_e + self.f_t_1_v) / 2
#             # if self.height(time) < self.karman_line:
#             #     f_engine += self.f_t_1_e
#             # else:
#             #     f_engine += self.f_t_1_v
#
#         return f_engine
#
#     # r(t)
#     def powers_x(self,
#                  time: int):
#         phi = arctan(self.r_y(time) / self.r_x(time))
#         # phi = self.angle(time)
#
#         first = math.cos(self.angle(time)) * self.engine(time)
#         second = math.cos(phi) * (self.gravitation(time) + self.drag(time))
#
#         return first - second
#
#     # r(t)
#     def powers_y(self,
#                  time: int):
#         phi = arctan(self.r_y(time) / self.r_x(time))
#         # phi = self.angle(time)
#
#         first = math.sin(self.angle(time)) * self.engine(time)
#         second = math.sin(phi) * (self.gravitation(time) + self.drag(time))
#
#         return first - second
#
#     def r_x(self,
#             time: int):
#         # return self.r_0_x + self.speed_x(time) * time + 1 / 2 * self.acceleration_x(time) * time ** 2
#         return (self.r_0_x
#                 + derivative(self.r_x, time, dx=1e-6, n=1) * time
#                 + 1 / 2 * derivative(self.r_x, time, dx=1e-6, n=2) * time ** 2)
#
#     def r_y(self,
#             time: int):
#         return (self.r_0_x
#                 + derivative(self.r_y, time, dx=1e-6, n=1) * time
#                 + 1 / 2 * derivative(self.r_y, time, dx=1e-6, n=2) * time ** 2)
#
#         # return self.r_0_y + self.speed_y(time) * time + 1 / 2 * self.acceleration_y(time) * time ** 2
#
#     def r(self,
#           time: int):
#         return (self.r_x(time) ** 2 + self.r_y(time) ** 2) ** 0.5 + self.h_c
#
#     def speed_x(self,
#                 time: int):
#         def f(x):
#             return x ** 2 + 1
#
#         derivative(f, 5, dx=1e-6)
#
#         return self.v_0_x + self.acceleration_x(time) * time
#
#     def speed_y(self,
#                 time: int):
#         return self.v_0_y + self.acceleration_y(time) * time
#
#     def acceleration_x(self,
#                        time: int):
#         return self.powers_x(time) / self.mass(time)
#
#     def acceleration_y(self,
#                        time: int):
#         return self.powers_y(time) / self.mass(time)
#
#     # r(t)
#     def height(self,
#                time: int):
#         return self.r(time) - self.h_c
#
#     def speed(self,
#               time: int):
#         return (self.speed_x(time) ** 2 + self.speed_y(time) ** 2) ** 0.5
#
#     # NORM
#     def angle(self,
#               time: int):
#         first = (time < self.t_p_1) * np.pi / 2
#         second_first = self.t_p_1 <= time <= self.t_p_2
#         second_second = np.pi / 2 - np.pi / 2 * ((time - self.t_p_1) / (self.t_p_2 - self.t_p_1))
#         second = second_first * second_second
#         third = (time > self.t_p_2) * 0
#
#         return first + second + third
#
#     # NORM
#     def mass(self,
#              time: int):
#         return (self.m_start -
#                 (time < self.t_1) * self.m_1 * time -
#                 (self.t_1 <= time < self.t_2) * self.m_2 * time -
#                 (time >= self.t_1) * self.m_0_1 -
#                 (time >= self.t_2) * (self.m_0_2 - self.m_1_2))
#
#     height_ = 0
#     speed_ = 0
#     angle_ = np.pi / 2
#     mass_ = m_start
#     gravitation_ = 0
#     drag_ = 0
#     powers_x_ = 0
#     powers_y_ = 0
#     phi_ = np.pi / 180
#     r_x_ = 0
#     r_y_ = 0
#     r_ = h_c
#     engine_ = 0
#     acceleration_x_ = 0
#     acceleration_y_ = 0
#     speed_x_ = 0
#     speed_y_ = 0
#     # NORM
#     def data(self,
#              time: int) -> (float, float, float, float):
#         if time == 0:
#             return 0, 0, np.pi / 2, self.m_start
#
#         self.angle_ = self.angle(time)
#         self.mass_ = self.mass(time)
#
#         self.gravitation_ = self.G * self.mass_ * self.earth_mass / self.r_ ** 2
#         self.drag_ = 1 / 2 * self.r_0 * math.exp(-self.height_ / self.H) * self.c_d * self.a * self.speed_ ** 2
#
#         self.engine_ = 0
#         if self.height_ < self.karman_line:
#             if time < self.t_p_1:
#                 self.engine_ += self.f_t_1_e
#             if time < self.t_p_2:
#                 self.engine_ += self.f_t_2_e
#         else:
#             if time < self.t_p_1:
#                 self.engine_ += self.f_t_1_v
#             if time < self.t_p_2:
#                 self.engine_ += self.f_t_2_v
#
#         self.powers_x_ = (math.cos(self.angle_) * self.engine_ -
#                           math.cos(self.phi_) * (self.gravitation_ + self.drag_))
#         self.powers_y_ = (math.sin(self.angle_) * self.engine_ -
#                           math.sin(self.phi_) * (self.gravitation_ + self.drag_))
#
#         self.acceleration_x_ = self.powers_x_ / self.mass_
#         self.acceleration_y_ = self.powers_y_ / self.mass_
#
#         self.speed_x_ = self.v_0_x + self.acceleration_x_ * time
#         self.speed_y_ = self.v_0_y + self.acceleration_y_ * time
#         self.speed_ = (self.speed_x_ ** 2 + self.speed_y_ ** 2) ** 0.5
#
#         self.r_x_ = self.r_0_x + self.speed_x_ * time + 1 / 2 * self.acceleration_x_ * time ** 2
#         self.r_y_ = self.r_0_y + self.speed_y_ * time + 1 / 2 * self.acceleration_y_ * time ** 2
#         self.r_ = (self.r_x_ ** 2 + self.r_y_ ** 2) ** 0.5 + self.h_c
#         print(self.speed_, self.height_, self.r_)
#
#         self.height_ = self.r_ - self.h_c
#
#         self.phi_ = arctan(self.r_y_ / self.r_x_)
#
#         return self.height_, self.speed_, 180 / np.pi * self.angle_, self.mass_
#
#     # NORM
#     def pause(self,
#               interval: float):
#         pass
#
#     # NORM
#     def is_end(self,
#                time: int) -> bool:
#         return time >= self.config.data['plotting_time']

# class Model(DataSource):
#     config: Config
#
#     m_start = 267_000
#     m_0 = 500
#     m_0_1 = 172_000
#     m_0_2 = 94_000
#     m_1_1 = 13_600
#     m_1_2 = 7_495
#     i_1_e = 252
#     i_1_v = 308
#     i_2_e = 243
#     i_2_v = 309
#     f_t_1_e = 3_216
#     f_t_1_v = 3_924
#     f_t_2_e = 735.5
#     f_t_2_v = 921
#     t_0 = 315
#     t_p_1 = 16
#     t_p_2 = 113
#     t_1 = 120
#     t_2 = 280
#     t_full = 280
#     m_1 = 1300
#     m_2 = 308.5
#     phi = np.pi / 180
#
#     n = 2
#     k = 0.9
#
#     plotting_time: int
#
#     def __init__(self,
#                  config: Config):
#         self.config = config
#
#     def height(self,
#                time: int):
#         return scipy.integrate.quad(lambda t: np.cos((t < self.t_p_1) * 0 +
#                                                      (self.t_p_1 <= t <= self.t_p_2) * self.k * (np.pi / 2) *
#                                                      ((t - self.t_p_1) / (self.t_p_2 - self.t_p_1)) +
#                                                      (t > self.t_p_2) * self.k * (np.pi / 2)) *
#                                               self.speed(t),
#                                     0,
#                                     time)[0]
#
#     def speed(self,
#               time: int):
#         i_i = lambda i: ((self.i_1_e + self.i_1_v) / 2) if i == 1 else ((self.i_2_e + self.i_2_v) / 2)
#         m_i = lambda i: self.m_1 if i == 1 else self.m_2
#         m_0_i = lambda i: self.m_0_1 if i == 1 else self.m_0_2
#         m_1_i = lambda i: self.m_1_1 if i == 1 else self.m_1_2
#         t_i = lambda i: self.t_1 if i == 1 else self.t_2
#
#         partial = 0
#         for i in range(1, self.n + 1):
#             partial_1 = time > sum([t_i(j) for j in range(1, i)])
#
#             sub_expression_up = self.m_0 + sum([m_0_i(j) for j in range(i, self.n + 1)])
#             sub_expression_down = (self.m_0 +
#                                    max(m_1_i(i), m_0_i(i) - m_i(i) * (time - sum([t_i(j) for j in range(1, i)]))) +
#                                    sum([m_0_i(j) for j in range(i + 1, self.n + 1)]))
#             partial_2 = scipy.constants.g * i_i(i) * np.log(sub_expression_up / sub_expression_down)
#
#             partial += partial_1 * partial_2
#
#         return partial - scipy.integrate.quad(lambda t: scipy.constants.g * (-np.cos(self.angle(t))), 0, time)[0]
#
#     def angle(self,
#               time: int):
#         return ((time < self.t_p_1) * np.pi +
#                 (self.t_p_1 <= time <= self.t_p_2) *
#                 max(np.pi / 2 + self.phi,
#                     np.pi - (np.pi / 2) * ((time - self.t_p_1) / (self.t_p_2 - self.t_p_1))) +
#                 (time > self.t_p_2) * (np.pi / 2 + self.phi))
#
#     def mass(self,
#              time: int):
#         return (self.m_start -
#                 (time < self.t_1) * self.m_1 * time -
#                 (self.t_1 <= time < self.t_2) * self.m_2 * time -
#                 (time >= self.t_1) * self.m_0_1 -
#                 (time >= self.t_2) * (self.m_0_2 - self.m_1_2))
#
#     def data(self,
#              time: int) -> (float, float, float, float):
#         n_angle = ((time < self.t_p_1) * 0 +
#                    (self.t_p_1 <= time <= self.t_p_2) * (np.pi / 2) * ((time - self.t_p_1) / (self.t_p_2 - self.t_p_1)) +
#                    (time > self.t_p_2) * (np.pi / 2))
#
#         return self.height(time), self.speed(time), 90 - n_angle, self.mass(time)
#
#     def pause(self,
#               interval: float):
#         pass
#
#     def is_end(self,
#                time: int) -> bool:
#         return time >= self.config.data['plotting_time']
