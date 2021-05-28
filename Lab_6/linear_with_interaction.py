from numpy.linalg import det


class LinearWithInteractionModel:
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
        m00, m10, m20, m30, m40, m50, m60, m70, k0 = 0, 0, 0, 0, 0, 0, 0, 0, 0
        m01, m11, m21, m31, m41, m51, m61, m71, k1 = 0, 0, 0, 0, 0, 0, 0, 0, 0
        m02, m12, m22, m32, m42, m52, m62, m72, k2 = 0, 0, 0, 0, 0, 0, 0, 0, 0
        m03, m13, m23, m33, m43, m53, m63, m73, k3 = 0, 0, 0, 0, 0, 0, 0, 0, 0
        m04, m14, m24, m34, m44, m54, m64, m74, k4 = 0, 0, 0, 0, 0, 0, 0, 0, 0
        m05, m15, m25, m35, m45, m55, m65, m75, k5 = 0, 0, 0, 0, 0, 0, 0, 0, 0
        m06, m16, m26, m36, m46, m56, m66, m76, k6 = 0, 0, 0, 0, 0, 0, 0, 0, 0
        m07, m17, m27, m37, m47, m57, m67, m77, k7 = 0, 0, 0, 0, 0, 0, 0, 0, 0

        for i in range(self.N):
            m00 = self.N
            m10 += nx[1][i]
            m20 += nx[2][i]
            m30 += nx[3][i]
            m40 += nx[1][i] * nx[2][i]
            m50 += nx[1][i] * nx[3][i]
            m60 += nx[2][i] * nx[3][i]
            m70 += nx[1][i] * nx[2][i] * nx[3][i]
            k0 += y_average[i]
            m01 += nx[1][i]
            m11 += nx[1][i] ** 2
            m21 += nx[1][i] * nx[2][i]
            m31 += nx[1][i] * nx[3][i]
            m41 += (nx[1][i] ** 2) * nx[2][i]
            m51 += (nx[1][i] ** 2) * nx[3][i]
            m61 += nx[1][i] * nx[2][i] * nx[3][i]
            m71 += (nx[1][i] ** 2) * nx[2][i] * nx[3][i]
            k1 += y_average[i] * nx[1][i]
            m02 += nx[2][i]
            m12 += nx[1][i] * nx[2][i]
            m22 += nx[2][i] ** 2
            m32 += nx[2][i] * nx[3][i]
            m42 += nx[1][i] * (nx[2][i] ** 2)
            m52 += nx[1][i] * nx[2][i] * nx[3][i]
            m62 += (nx[2][i] ** 2) * nx[3][i]
            m72 += nx[1][i] * (nx[2][i] ** 2) * nx[3][i]
            k2 += y_average[i] * nx[2][i]
            m03 += nx[3][i]
            m13 += nx[1][i] * nx[3][i]
            m23 += nx[2][i] * nx[3][i]
            m33 += nx[3][i] ** 2
            m43 += nx[1][i] * nx[2][i] * nx[3][i]
            m53 += nx[1][i] * (nx[3][i] ** 2)
            m63 += nx[2][i] * (nx[3][i] ** 2)
            m73 += nx[1][i] * nx[2][i] * (nx[3][i] ** 2)
            k3 += y_average[i] * nx[3][i]
            m04 += nx[1][i] * nx[2][i]
            m14 += (nx[1][i] ** 2) * nx[2][i]
            m24 += nx[1][i] * (nx[2][i] ** 2)
            m34 += nx[1][i] * nx[2][i] * nx[3][i]
            m44 += (nx[1][i] ** 2) * (nx[2][i] ** 2)
            m54 += (nx[1][i] ** 2) * nx[2][i] * nx[3][i]
            m64 += nx[1][i] * (nx[2][i] ** 2) * nx[3][i]
            m74 += (nx[1][i] ** 2) * (nx[2][i] ** 2) * nx[3][i]
            k4 += y_average[i] * nx[1][i] * nx[2][i]
            m05 += nx[1][i] * nx[3][i]
            m15 += (nx[1][i] ** 2) * nx[3][i]
            m25 += nx[1][i] * nx[2][i] * nx[3][i]
            m35 += nx[1][i] * (nx[3][i] ** 2)
            m45 += (nx[1][i] ** 2) * nx[2][i] * nx[3][i]
            m55 += (nx[1][i] ** 2) * (nx[3][i] ** 2)
            m65 += nx[1][i] * nx[2][i] * (nx[3][i] ** 2)
            m75 += (nx[1][i] ** 2) * nx[2][i] * (nx[3][i] ** 2)
            k5 += y_average[i] * nx[1][i] * nx[3][i]
            m06 += nx[2][i] * nx[3][i]
            m16 += nx[1][i] * nx[2][i] * nx[3][i]
            m26 += (nx[2][i] ** 2) * nx[3][i]
            m36 += nx[2][i] * (nx[3][i] ** 2)
            m46 += nx[1][i] * (nx[2][i] ** 2) * nx[3][i]
            m56 += nx[1][i] * nx[2][i] * (nx[3][i] ** 2)
            m66 += (nx[2][i] ** 2) * (nx[3][i] ** 2)
            m76 += nx[1][i] * (nx[2][i] ** 2) * (nx[3][i] ** 2)
            k6 += y_average[i] * nx[2][i] * nx[3][i]
            m07 += nx[1][i] * nx[2][i] * nx[3][i]
            m17 += (nx[1][i] ** 2) * nx[2][i] * nx[3][i]
            m27 += nx[1][i] * (nx[2][i] ** 2) * nx[3][i]
            m37 += nx[1][i] * nx[2][i] * (nx[3][i] ** 2)
            m47 += (nx[1][i] ** 2) * (nx[2][i] ** 2) * nx[3][i]
            m57 += (nx[1][i] ** 2) * nx[2][i] * (nx[3][i] ** 2)
            m67 += nx[1][i] * (nx[2][i] ** 2) * (nx[3][i] ** 2)
            m77 += (nx[1][i] ** 2) * (nx[2][i] ** 2) * (nx[3][i] ** 2)
            k7 += y_average[i] * nx[1][i] * nx[2][i] * nx[3][i]

        main_det = det([
            [m00, m10, m20, m30, m40, m50, m60, m70],
            [m01, m11, m21, m31, m41, m51, m61, m71],
            [m02, m12, m22, m32, m42, m52, m62, m72],
            [m03, m13, m23, m33, m43, m53, m63, m73],
            [m04, m14, m24, m34, m44, m54, m64, m74],
            [m05, m15, m25, m35, m45, m55, m65, m75],
            [m06, m16, m26, m36, m46, m56, m66, m76],
            [m07, m17, m27, m37, m47, m57, m67, m77]])

        det0 = det([
            [k0, m10, m20, m30, m40, m50, m60, m70],
            [k1, m11, m21, m31, m41, m51, m61, m71],
            [k2, m12, m22, m32, m42, m52, m62, m72],
            [k3, m13, m23, m33, m43, m53, m63, m73],
            [k4, m14, m24, m34, m44, m54, m64, m74],
            [k5, m15, m25, m35, m45, m55, m65, m75],
            [k6, m16, m26, m36, m46, m56, m66, m76],
            [k7, m17, m27, m37, m47, m57, m67, m77]])

        det1 = det([
            [m00, k0, m20, m30, m40, m50, m60, m70],
            [m01, k1, m21, m31, m41, m51, m61, m71],
            [m02, k2, m22, m32, m42, m52, m62, m72],
            [m03, k3, m23, m33, m43, m53, m63, m73],
            [m04, k4, m24, m34, m44, m54, m64, m74],
            [m05, k5, m25, m35, m45, m55, m65, m75],
            [m06, k6, m26, m36, m46, m56, m66, m76],
            [m07, k7, m27, m37, m47, m57, m67, m77]])

        det2 = det([
            [m00, m10, k0, m30, m40, m50, m60, m70],
            [m01, m11, k1, m31, m41, m51, m61, m71],
            [m02, m12, k2, m32, m42, m52, m62, m72],
            [m03, m13, k3, m33, m43, m53, m63, m73],
            [m04, m14, k4, m34, m44, m54, m64, m74],
            [m05, m15, k5, m35, m45, m55, m65, m75],
            [m06, m16, k6, m36, m46, m56, m66, m76],
            [m07, m17, k7, m37, m47, m57, m67, m77]])

        det3 = det([
            [m00, m10, m20, k0, m40, m50, m60, m70],
            [m01, m11, m21, k1, m41, m51, m61, m71],
            [m02, m12, m22, k2, m42, m52, m62, m72],
            [m03, m13, m23, k3, m43, m53, m63, m73],
            [m04, m14, m24, k4, m44, m54, m64, m74],
            [m05, m15, m25, k5, m45, m55, m65, m75],
            [m06, m16, m26, k6, m46, m56, m66, m76],
            [m07, m17, m27, k7, m47, m57, m67, m77]])

        det4 = det([
            [m00, m10, m20, m30, k0, m50, m60, m70],
            [m01, m11, m21, m31, k1, m51, m61, m71],
            [m02, m12, m22, m32, k2, m52, m62, m72],
            [m03, m13, m23, m33, k3, m53, m63, m73],
            [m04, m14, m24, m34, k4, m54, m64, m74],
            [m05, m15, m25, m35, k5, m55, m65, m75],
            [m06, m16, m26, m36, k6, m56, m66, m76],
            [m07, m17, m27, m37, k7, m57, m67, m77]])

        det5 = det([
            [m00, m10, m20, m30, m40, k0, m60, m70],
            [m01, m11, m21, m31, m41, k1, m61, m71],
            [m02, m12, m22, m32, m42, k2, m62, m72],
            [m03, m13, m23, m33, m43, k3, m63, m73],
            [m04, m14, m24, m34, m44, k4, m64, m74],
            [m05, m15, m25, m35, m45, k5, m65, m75],
            [m06, m16, m26, m36, m46, k6, m66, m76],
            [m07, m17, m27, m37, m47, k7, m67, m77]])

        det6 = det([
            [m00, m10, m20, m30, m40, m50, k0, m70],
            [m01, m11, m21, m31, m41, m51, k1, m71],
            [m02, m12, m22, m32, m42, m52, k2, m72],
            [m03, m13, m23, m33, m43, m53, k3, m73],
            [m04, m14, m24, m34, m44, m54, k4, m74],
            [m05, m15, m25, m35, m45, m55, k5, m75],
            [m06, m16, m26, m36, m46, m56, k6, m76],
            [m07, m17, m27, m37, m47, m57, k7, m77]])

        det7 = det([
            [m00, m10, m20, m30, m40, m50, m60, k0],
            [m01, m11, m21, m31, m41, m51, m61, k1],
            [m02, m12, m22, m32, m42, m52, m62, k2],
            [m03, m13, m23, m33, m43, m53, m63, k3],
            [m04, m14, m24, m34, m44, m54, m64, k4],
            [m05, m15, m25, m35, m45, m55, m65, k5],
            [m06, m16, m26, m36, m46, m56, m66, k6],
            [m07, m17, m27, m37, m47, m57, m67, k7]])

        A0 = det0 / main_det
        A1 = det1 / main_det
        A2 = det2 / main_det
        A3 = det3 / main_det
        A4 = det4 / main_det
        A5 = det5 / main_det
        A6 = det6 / main_det
        A7 = det7 / main_det

        self.A = [A0, A1, A2, A3, A4, A5, A6, A7]

    def find_encoded_cfs(self, x, y_average):
        """x - матриця натуральных значень факторів"""
        self.B = [0 for _ in range(self.K)]
        for i in range(self.N):
            self.B[0] += y_average[i] * x[0][i]
            self.B[1] += y_average[i] * x[1][i]
            self.B[2] += y_average[i] * x[2][i]
            self.B[3] += y_average[i] * x[3][i]
            self.B[4] += y_average[i] * x[1][i] * x[2][i]
            self.B[5] += y_average[i] * x[1][i] * x[3][i]
            self.B[6] += y_average[i] * x[2][i] * x[3][i]
            self.B[7] += y_average[i] * x[1][i] * x[2][i] * x[3][i]
        for i in range(self.K):
            self.B[i] /= self.N

    def calculate_with_nature_cfs(self, nxl):
        """nxl - nature x line"""
        return self.A[0]*nxl[0] + self.A[1]*nxl[1] + self.A[2]*nxl[2] + self.A[3]*nxl[3] + \
               self.A[4]*nxl[1]*nxl[2] + self.A[5]*nxl[1]*nxl[3] + self.A[6]*nxl[2]*nxl[3] + \
               self.A[7]*nxl[1]*nxl[2]*nxl[3]

    def calculate_with_encoded_cfs(self, xl):
        """xl - encoded x line"""
        return self.B[0]*xl[0] + self.B[1]*xl[1] + self.B[2]*xl[2] + self.B[3]*xl[3] + \
               self.B[4]*xl[1]*xl[2] + self.B[5]*xl[1]*xl[3] + self.B[6]*xl[2]*xl[3] + \
               self.B[7]*xl[1]*xl[2]*xl[3]
