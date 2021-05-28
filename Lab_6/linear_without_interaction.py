from numpy.linalg import det


class LinearWithoutInteractionModel:
    K = 0
    N = 0
    A = list()
    B = list()

    def __init__(self, K, N):
        self.K = K
        self.N = N

    def __del__(self):
        del self.K, self.N, self.A, self.B

    def find_nature_cfs(self, nx, y_average):
        """nx - матриця натуральних значень х"""
        mx1, mx2, mx3, my = sum(nx[1]) / self.N, sum(nx[2]) / self.N, sum(nx[3]) / self.N, sum(y_average) / self.N
        a11, a22, a33 = 0, 0, 0
        a12, a13, a23 = 0, 0, 0
        a1, a2, a3 = 0, 0, 0
        for i in range(self.N):
            a11 += nx[1][i] ** 2
            a22 += nx[2][i] ** 2
            a33 += nx[3][i] ** 2
            a12 += nx[1][i] * nx[2][i]
            a13 += nx[1][i] * nx[3][i]
            a23 += nx[2][i] * nx[3][i]
            a1 += y_average[i] * nx[1][i]
            a2 += y_average[i] * nx[2][i]
            a3 += y_average[i] * nx[3][i]
        a11, a22, a33 = a11 / self.N, a22 / self.N, a33 / self.N
        a12, a13, a23 = a12 / self.N, a13 / self.N, a23 / self.N
        a1, a2, a3 = a1 / self.N, a2 / self.N, a3 / self.N
        a21 = a12
        a31 = a13
        a32 = a23

        main_det = det([[1, mx1, mx2, mx3], [mx1, a11, a12, a13], [mx2, a21, a22, a23], [mx3, a31, a32, a33]])
        A0 = det([[my, mx1, mx2, mx3], [a1, a11, a12, a13], [a2, a21, a22, a23], [a3, a31, a32, a33]]) / main_det
        A1 = det([[1, my, mx2, mx3], [mx1, a1, a12, a13], [mx2, a2, a22, a23], [mx3, a3, a32, a33]]) / main_det
        A2 = det([[1, mx1, my, mx3], [mx1, a11, a1, a13], [mx2, a21, a2, a23], [mx3, a31, a3, a33]]) / main_det
        A3 = det([[1, mx1, mx2, my], [mx1, a11, a12, a1], [mx2, a21, a22, a2], [mx3, a31, a32, a3]]) / main_det
        self.A = [A0, A1, A2, A3]

    def find_encoded_cfs(self, x, y_average):
        """x - матриця натуральных значень факторів"""
        self.B = [0 for _ in range(self.K)]
        for i in range(self.N):
            self.B[0] += y_average[i] * x[0][i]
            self.B[1] += y_average[i] * x[1][i]
            self.B[2] += y_average[i] * x[2][i]
            self.B[3] += y_average[i] * x[3][i]

        for i in range(self.K):
            self.B[i] /= self.N

    def calculate_with_nature_cfs(self, nxl):
        """nxl - nature x line"""
        return self.A[0] * nxl[0] + self.A[1] * nxl[1] + self.A[2] * nxl[2] + self.A[3] * nxl[3]

    def calculate_with_encoded_cfs(self, xl):
        """xl - encoded x line"""
        return self.B[0] * xl[0] + self.B[1] * xl[1] + self.B[2] * xl[2] + self.B[3] * xl[3]
