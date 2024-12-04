import numpy as np
import scipy

from .data_source import DataSource


class Model(DataSource):
    m_start = 267_000
    m_0 = 500
    m_0_1 = 172_000
    m_0_2 = 94_000
    m_1_1 = 13_600
    m_1_2 = 7_495
    i_1_e = 252
    i_1_v = 308
    i_2_e = 243
    i_2_v = 309
    f_t_1_e = 3_216
    f_t_1_v = 3_924
    f_t_2_e = 735.5
    f_t_2_v = 921
    g = 9.81
    t_0 = 295
    t_p_1 = 16
    t_p_2 = 113
    t_1 = 122
    t_2 = 280
    t_full = 280
    m_1 = 1300
    m_2 = 308.5
    phi = np.pi / 180
    n = 2
    k = 0 # TODO

    def height_formula(self):
        pass

    def speed_formula(self):
        pass

    def angle_formula(self):
        pass

    def mass_formula(self):
        pass

    def height(self, time: int):
        vertical_angle = lambda t: ((t < self.t_p_1) * 0
                                    + (self.t_p_1 <= t <= self.t_p_2) * self.k * (np.pi / 2)
                                    * ((t - self.t_p_1) / (self.t_p_2 - self.t_p_1))
                                    + (t > self.t_p_2) * self.k * (np.pi / 2))

        result = scipy.integrate.quad(lambda t: np.cos(vertical_angle(t)) * self.speed(t), 0, time)

        return result[0]

    def speed(self, time: int):
        i_i = lambda i: (self.i_1_e + self.i_1_v) / 2 if i == 1 else (self.i_2_e + self.i_2_v) / 2
        m_i = lambda i: self.m_1 if i == 1 else self.m_2
        m_0_i = lambda i: self.m_0_1 if i == 1 else self.m_0_2
        m_1_i = lambda i: self.m_1_1 if i == 1 else self.m_1_2
        m_0_j = lambda j: self.m_0_1 if j == 1 else self.m_0_2
        t_j = lambda j: self.t_1 if j == 1 else self.t_2

        first = 0
        for i in range(1, self.n + 1):
            partial_1 = (time > sum([t_j(j) for j in range(1, i)]))
            sub_expression_up = self.m_0 + sum([m_0_j(j) for j in range(i, self.n + 1)])
            sub_expression_down = (self.m_0 +
                                   max(m_1_i(i), m_0_i(i) - m_i(i) * (time - sum([t_j(j) for j in range(1, i)]))) +
                                   sum([m_0_j(j) for j in range(i + 1, self.n + 1)]))
            partial_2 = i_i(i) * np.log(sub_expression_up / sub_expression_down)
            first += partial_1 * partial_2

        second = scipy.integrate.quad(lambda t: scipy.constants.g * (-np.cos(self.angle(t))), 0, time)[0]

        return first - second

    def angle(self, time: int):
        first = (time < self.t_p_1) * np.pi
        second = ((self.t_p_1 <= time <= self.t_p_2)
                  * max(np.pi / 2 + self.phi,
                        np.pi - (np.pi / 2) * ((time - self.t_p_1) / (self.t_p_2 - self.t_p_1))))
        third = (time > self.t_p_2) * (np.pi / 2 + self.phi)

        return first + second + third

    def mass(self, time: int):
        return 0

    def data(self, time: int):
        return -self.height(time), -self.speed(time), self.angle(time), self.mass(time)

    def pause(self, interval: int):
        pass

# from sympy import *
#
# from .data_source import DataSource
#
#
# class Model(DataSource):
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
#     g = 9.81
#     t_0 = 295
#     t_p_1 = 16
#     t_p_2 = 113
#     t_1 = 122
#     t_2 = 280
#     t_full = 280
#     m_1 = 1300
#     m_2 = 308.5
#     phi = pi / 180
#     n = 2
#     k = 0 # TODO
#
#     def height_formula(self):
#         k = Symbol('k')
#         t_p_1 = Symbol('t_p_1')
#         t_p_2 = Symbol('t_p_2')
#
#         t = Symbol('t')
#
#         # v = Function('v')(t)  # Функция скорости
#
#         # H(x, a) =
#         # 1, x > 0
#         # a, x == 0
#         # 0, x < 0
#         #
#         # a > b => H(a - b, 0)
#         # a < b => 1 - H(a - b, 0)
#         # a >= b => H(a - b, 1)
#         # a <= b => 1 - H(a - b, 1)
#         # a <= b <= c => (a <= b) + (b <= c) >= 2 => (1 - H(a - b, 1) + 1 - H(b - c, 1)) >= 2 => 2 - (H(a - b, 1) + H(b - c, 1)) >= 2 =>
#         # => H(a - b, 1) + H(b - c, 1) <= 0 => 1 - H(H(a - b, 1) + H(b - c, 1), 1)
#
#         # sub_formula = Piecewise((S(0), t < t_p_1),
#         #                         (k * (pi / 2) * ((t - t_p_1) / (t_p_2 - t_p_1)), (t_p_1 <= t) & (t <= t_p_2)),
#         #                         (k * (pi / 2), t > t_p_2))
#
#         first = (1 - Heaviside(t - t_p_1, 0)) * 0
#         second = ((1 - Heaviside(Heaviside(t_p_1 - t, 1) + Heaviside(t - t_p_2, 1), 1))
#                   * k
#                   * (pi / 2)
#                   * ((t - t_p_1) / (t_p_2 - t_p_1)))
#         third = (Heaviside(t - t_p_2, 0)
#                  * k
#                  * (pi / 2))
#
#         sub_formula = first + second + third
#
#         return integrate(cos(sub_formula) * self.speed_formula(),
#                          (t, 0, t))
#
#     def speed_formula(self):
#         g = Symbol('g')
#         i_1 = Symbol('i_1')
#         i_2 = Symbol('i_2')
#         m_0 = Symbol('m_0')
#         m_1 = Symbol('m_1')
#         m_2 = Symbol('m_2')
#         m_0_1 = Symbol('m_0_1')
#         m_0_2 = Symbol('m_0_2')
#         m_1_1 = Symbol('m_1_1')
#         m_1_2 = Symbol('m_1_2')
#         n = Symbol('n')
#         t_1 = Symbol('t_1')
#         t_2 = Symbol('t_2')
#
#         i = Symbol('i')
#         j = Symbol('j')
#
#         t = Symbol('t')
#
#         piecewise_i_i = Piecewise((i_1, Eq(i, 1)),
#                                   (i_2, Eq(i, 2)),
#                                   (0, True))
#         piecewise_m_i = Piecewise((m_1, Eq(i, 1)),
#                                   (m_2, Eq(i, 2)),
#                                   (0, True))
#         piecewise_m_0_i = Piecewise((m_0_1, Eq(i, 1)),
#                                     (m_0_2, Eq(i, 2)),
#                                     (0, True))
#         piecewise_m_1_i = Piecewise((m_1_1, Eq(i, 1)),
#                                     (m_1_2, Eq(i, 2)),
#                                     (0, True))
#         piecewise_m_0_j = Piecewise((m_0_1, Eq(j, 1)),
#                                     (m_0_2, Eq(j, 2)),
#                                     (0, True))
#         piecewise_t_j = Piecewise((t_1, Eq(j, 1)),
#                                   (t_2, Eq(j, 2)),
#                                   (0, True))
#
#         first_first = Heaviside(t - summation(piecewise_t_j,
#                                               (j, 1, i - 1)),
#                                 0)
#         first_second_ln_expr_up = m_0 + summation(piecewise_m_0_j,
#                                                   (j, i, n))
#         first_second_ln_expr_down = (m_0
#                                      + Max(piecewise_m_1_i,
#                                            piecewise_m_0_i - piecewise_m_i * (t - summation(piecewise_t_j,
#                                                                                             (j, 1, i - 1))))
#                                      + summation(piecewise_m_0_j,
#                                                  (j, i + 1, n)))
#         first_second_ln_expr = first_second_ln_expr_up / first_second_ln_expr_down
#         first_second = piecewise_i_i * ln(first_second_ln_expr)
#         first = summation(first_first * first_second,
#                           (i, 1, n))
#
#         second = integrate(g * (-cos(self.angle_formula())), (t, 0, t))
#
#         return first - second
#
#     def angle_formula(self):
#         t_p_1 = Symbol('t_p_1')
#         t_p_2 = Symbol('t_p_2')
#         phi = Symbol('phi')
#
#         t = Symbol('t')
#
#         first = (1 - Heaviside(t - t_p_1, 0)) * pi
#         second_first = (1 - Heaviside(Heaviside(t_p_1 - t, 1) + Heaviside(t - t_p_2, 1), 1))
#         second_second = Max(pi / 2 + phi,
#                             pi - (pi / 2) * ((t - t_p_1) / (t_p_2 - t_p_1)))
#         second = second_first * second_second
#         third = Heaviside(t - t_p_2, 0) * (pi / 2 + phi)
#
#         return first + second + third
#
#     def mass_formula(self):
#         pass
#
#     def height(self, time: int):
#         g = Symbol('g')
#         i_1 = Symbol('i_1')
#         i_2 = Symbol('i_2')
#         m_0 = Symbol('m_0')
#         m_1 = Symbol('m_1')
#         m_2 = Symbol('m_2')
#         m_0_1 = Symbol('m_0_1')
#         m_0_2 = Symbol('m_0_2')
#         m_1_1 = Symbol('m_1_1')
#         m_1_2 = Symbol('m_1_2')
#         n = Symbol('n')
#         t_1 = Symbol('t_1')
#         t_2 = Symbol('t_2')
#
#         t_p_1 = Symbol('t_p_1')
#         t_p_2 = Symbol('t_p_2')
#         phi = Symbol('phi')
#
#         k = Symbol('k')
#
#         t = Symbol('t')
#
#         return self.height_formula().subs({
#             g: self.g,
#             i_1: (self.i_1_e + self.i_1_v) / 2,
#             i_2: (self.i_2_e + self.i_2_v) / 2,
#             m_0: self.m_0,
#             m_1: self.m_1,
#             m_2: self.m_2,
#             m_0_1: self.m_0_1,
#             m_0_2: self.m_0_2,
#             m_1_1: self.m_1_1,
#             m_1_2: self.m_1_2,
#             n: self.n,
#             t_1: self.t_1,
#             t_2: self.t_2,
#
#             t_p_1: self.t_p_1,
#             t_p_2: self.t_p_2,
#             phi: self.phi,
#
#             k: self.k,
#
#             t: time
#         })
#
#     def speed(self, time: int):
#         g = Symbol('g')
#         i_1 = Symbol('i_1')
#         i_2 = Symbol('i_2')
#         m_0 = Symbol('m_0')
#         m_1 = Symbol('m_1')
#         m_2 = Symbol('m_2')
#         m_0_1 = Symbol('m_0_1')
#         m_0_2 = Symbol('m_0_2')
#         m_1_1 = Symbol('m_1_1')
#         m_1_2 = Symbol('m_1_2')
#         n = Symbol('n')
#         t_1 = Symbol('t_1')
#         t_2 = Symbol('t_2')
#
#         t_p_1 = Symbol('t_p_1')
#         t_p_2 = Symbol('t_p_2')
#         phi = Symbol('phi')
#
#         t = Symbol('t')
#
#         return self.speed_formula().subs({
#             g: self.g,
#             i_1: (self.i_1_e + self.i_1_v) / 2,
#             i_2: (self.i_2_e + self.i_2_v) / 2,
#             m_0: self.m_0,
#             m_1: self.m_1,
#             m_2: self.m_2,
#             m_0_1: self.m_0_1,
#             m_0_2: self.m_0_2,
#             m_1_1: self.m_1_1,
#             m_1_2: self.m_1_2,
#             n: self.n,
#             t_1: self.t_1,
#             t_2: self.t_2,
#
#             t_p_1: self.t_p_1,
#             t_p_2: self.t_p_2,
#             phi: self.phi,
#
#             t: time
#         })
#
#         # first = 0
#         # for i in range(1, self.n + 1):
#         #     t_j_sum = 0
#         #     for j in range(1, i):
#         #         if j == 1:
#         #             t_j_sum += self.t_1
#         #         elif j == 2:
#         #             t_j_sum += self.t_2
#         #
#         #     i_i = self.g * (((self.i_1_e + self.i_1_v) / 2) if i == 1 else ((self.i_2_e + self.i_2_v) / 2))
#         #     m_0_j_sum_up = 0
#         #     for j in range(i, self.n + 1):
#         #         if i == 1:
#         #             m_0_j_sum_up += self.m_0_1
#         #         elif i == 2:
#         #             m_0_j_sum_up += self.m_0_2
#         #     m_1_i = self.m_1_1 if i == 1 else self.m_1_2
#         #     m_0_i = self.m_0_1 if i == 1 else self.m_0_2
#         #     m_i = self.m_1 if i == 1 else self.m_2
#         #     t_j_sum = 0
#         #     for j in range(1, i):
#         #         if j == 1:
#         #             t_j_sum += self.t_1
#         #         elif j == 2:
#         #             t_j_sum += self.t_2
#         #     m_0_j_sum_down = 0
#         #     for j in range(i + 1, self.n + 1):
#         #         if j == 1:
#         #             m_0_j_sum_down += self.m_0_1
#         #         elif j == 2:
#         #             m_0_j_sum_down += self.m_0_2
#         #
#         #     first_first = time > t_j_sum
#         #
#         #     first_second_up = self.m_0 + m_0_j_sum_up
#         #     first_second_down = self.m_0 + max(m_1_i, m_0_i - m_i * (time - t_j_sum)) + m_0_j_sum_down
#         #     first_second = i_i * ln(first_second_up / first_second_down)
#         #
#         #     first += first_first * first_second
#         #
#         # t = Symbol('t')
#         # second_first = (t < self.t_p_1) * math.pi
#         # second_second_1 = (self.t_p_1 <= t <= self.t_p_2)
#         # second_second_2 = max(math.pi / 2 + self.phi, math.pi - (math.pi / 2) * ((t - self.t_p_1) / (self.t_p_2 - self.t_p_1)))
#         # second_second = second_second_1 * second_second_2
#         # second_third = (t > self.t_p_2) * (math.pi / 2 + self.phi)
#         #
#         # second = integrate(self.g * (-cos(second_first + second_second + second_third)), (t, 0, time))
#         #
#         # return first - second
#
#     def angle(self, time: int):
#         t_p_1 = Symbol('t_p_1')
#         t_p_2 = Symbol('t_p_2')
#         phi = Symbol('phi')
#
#         t = Symbol('t')
#
#         return self.angle_formula().subs({
#             t_p_1: self.t_p_1,
#             t_p_2: self.t_p_2,
#             phi: self.phi,
#
#             t: time
#         })
#
#     def mass(self, time: int):
#         pass
#
#     def data(self, time: int):
#         return self.height(time), self.speed(time), self.angle(time), self.mass(time)
#
#     def pause(self, interval: int):
#         pass
