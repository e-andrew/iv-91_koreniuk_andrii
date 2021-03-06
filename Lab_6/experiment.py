from copy import deepcopy
from random import randint
from math import sqrt, inf

import criterion_tables as ct


class Experiment:
    m = 0
    N = 0
    x_lines = list()
    y = list()
    y_average = list()
    S2_dis = list()
    f1, f2, f3, f4 = 0, 0, 0, 0
    Gp = 0
    t = list()
    Fp = 0
    d = 0
    s2b = 0

    def __init__(self, x_lines, m, N):
        self.x_lines = deepcopy(x_lines)
        self.m = m
        self.N = N

    def __del__(self):
        del self.m, self.N, self.x_lines
        del self.y, self.y_average, self.S2_dis
        del self.f1, self.f2, self.f3, self.f4
        del self.Gp, self.t, self.Fp, self.d, self.s2b

    def f(self, xl):
        return 7.7 * xl[0] + 2.8 * xl[1] + 0.5 * xl[2] + 2.6 * xl[3] + 5.0 * xl[1] * xl[2] + 0.3 * xl[1] * xl[3] + \
               9.3 * xl[2] * xl[3] + 4.1*xl[1]*xl[2]*xl[3] + 1.4*xl[1]*xl[1] + 0.3*xl[2]*xl[2] + 7.1*xl[3]*xl[3]

    def do(self):
        self.y = list()
        for i in range(self.N):
            self.y.append([self.f(self.x_lines[i]) + randint(0, 10) - 5 for _ in range(self.m)])

    def do_more(self):
        for i in range(self.N):
            self.y[i].append(self.f(self.x_lines[i]) + randint(0, 10) - 5)

    def check_kohren(self):
        self.y_average = [0 for _ in range(self.N)]
        for i in range(self.N):
            self.y_average[i] = sum(self.y[i]) / self.m

        self.S2_dis = [0 for _ in range(self.N)]
        for i in range(self.N):
            for j in range(self.m):
                self.S2_dis[i] += (self.y[i][j] - self.y_average[i]) ** 2
            self.S2_dis[i] /= self.m

        self.Gp = max(self.S2_dis) / sum(self.S2_dis)
        self.f1 = self.m - 1
        self.f2 = self.N
        if not(ct.compare_kohren_with_table_value(self.f1, self.f2, self.Gp)):
            self.m += 1
            self.do_more()
            return self.check_kohren()

    def check_student(self, K, A, B):
        self.s2b = sum(self.S2_dis) / self.N
        s2_b = self.s2b / (self.N * self.m)
        s_b = sqrt(s2_b)
        self.t = [0 for _ in range(K)]
        for i in range(K):
            self.t[i] = abs(B[i]) / s_b
        self.f3 = self.f1 * self.f2

        self.d = K
        for i in range(K):
            if not ct.compare_student_with_table_value(self.f3, self.t[i]):
                A[i] = 0
                B[i] = 0
                self.d -= 1

    def check_fisher(self, model, nx_lines):
        y_for_fisher = [0 for _ in range(self.N)]
        for i in range(self.N):
            y_for_fisher[i] = model.calculate_with_nature_cfs(nx_lines[i])
        s2ad = 0
        for i in range(self.N):
            s2ad += (y_for_fisher[i] - self.y_average[i]) ** 2

        if self.N - self.d > 0:
            s2ad = self.m * s2ad / (self.N - self.d)
        else:
            s2ad = inf

        self.f4 = self.N - self.d
        self.Fp = s2ad / self.s2b
        return ct.compare_phisher_with_table_value(self.f3, self.f4, self.Fp)
