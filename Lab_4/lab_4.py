from random import randint
from math import ceil, floor, sqrt
from numpy.linalg import det
import criterions as cr
import logs


"""Довірча ймовірність p = 0.95 (критерій значимості 0.05)"""
variant = dict()

x_min_average = 0
x_max_average = 0
y_min = 0
y_max = 0

x0 = list()
x1 = list()
x2 = list()
x3 = list()

nx0 = list()
nx1 = list()
nx2 = list()
nx3 = list()

px0 = list()
px1 = list()
px2 = list()
px3 = list()

pnx0 = list()
pnx1 = list()
pnx2 = list()
pnx3 = list()

ext_data = list()


def basic_configuration():
    global variant
    global x_min_average
    global x_max_average
    global y_min
    global y_max
    global x0
    global x1
    global x2
    global x3
    global nx0
    global nx1
    global nx2
    global nx3
    global px0
    global px1
    global px2
    global px3
    global pnx0
    global pnx1
    global pnx2
    global pnx3

    variant = {"n": 114, "x1min": -15, "x1max": 30, "x2min": 5, "x2max": 40, "x3min": 5, "x3max": 25}
    x_min_average = (variant["x1min"] + variant["x2min"] + variant["x3min"]) / 3
    x_max_average = (variant["x1max"] + variant["x2max"] + variant["x3max"]) / 3
    y_min = ceil(200 + x_min_average)
    y_max = floor(200 + x_max_average)
    x0 = [1, 1, 1, 1]
    x1 = [-1, -1, 1, 1]
    x2 = [-1, 1, -1, 1]
    x3 = [1, -1, -1, 1]
    nx0 = [1, 1, 1, 1]
    N = 4
    nx1 = [variant["x1min"] if x1[i] == -1 else variant["x1max"] for i in range(N)]
    nx2 = [variant["x2min"] if x2[i] == -1 else variant["x2max"] for i in range(N)]
    nx3 = [variant["x3min"] if x3[i] == -1 else variant["x3max"] for i in range(N)]
    px0 = [1, 1, 1, 1]
    px1 = [-1, -1, 1, 1]
    px2 = [-1, 1, -1, 1]
    px3 = [-1, 1, 1, -1]
    pnx0 = [1, 1, 1, 1]
    pnx1 = [variant["x1min"] if px1[i] == -1 else variant["x1max"] for i in range(N)]
    pnx2 = [variant["x2min"] if px2[i] == -1 else variant["x2max"] for i in range(N)]
    pnx3 = [variant["x3min"] if px3[i] == -1 else variant["x3max"] for i in range(N)]


def linear_model_without_interaction():
    global ext_data
    print(logs.get_text(0, []))
    N = 4
    K = 4
    m = 3
    print(logs.get_text(2, [N, K, m]))
    print(logs.get_text(3, []))
    y_1 = [randint(y_min, y_max) for _ in range(m)]
    y_2 = [randint(y_min, y_max) for _ in range(m)]
    y_3 = [randint(y_min, y_max) for _ in range(m)]
    y_4 = [randint(y_min, y_max) for _ in range(m)]
    y_average = []
    S2_dis = []
    f1 = 0
    f2 = 0

    def check_uniformity_of_dispersion(m):
        nonlocal y_average
        nonlocal S2_dis
        nonlocal f1
        nonlocal f2

        y_average = [sum(y_1)/m, sum(y_2)/m, sum(y_3)/m, sum(y_4)/m]

        S2_dis = [0, 0, 0, 0]
        for i in range(m):
            S2_dis[0] += (y_1[i] - y_average[0]) ** 2
            S2_dis[1] += (y_2[i] - y_average[1]) ** 2
            S2_dis[2] += (y_3[i] - y_average[2]) ** 2
            S2_dis[3] += (y_4[i] - y_average[3]) ** 2
        for i in range(N):
            S2_dis[i] /= m

        Gp = max(S2_dis) / sum(S2_dis)
        f1 = m - 1
        f2 = N
        print(logs.get_text(10, [f1, f2, Gp]))
        return cr.check_kohren(f1, f2, Gp)

    while not check_uniformity_of_dispersion(m):
        print(logs.get_text(12, []))
        y_1.append(randint(y_min, y_max))
        y_2.append(randint(y_min, y_max))
        y_3.append(randint(y_min, y_max))
        y_4.append(randint(y_min, y_max))
        m += 1
        print(logs.get_text(12, []))
        print(logs.get_text(2, [N, K, m]))

    # Пошук коефіцієнтів
    print(logs.get_text(11, []))
    parameters = [m, N, nx1, nx2, nx3, {0: y_1, 1: y_2, 2: y_3, 3: y_4}]
    logs.show_linear_natural_plan_without_interaction(*parameters)

    parameters = [m, N, x0, x1, x2, x3, {0: y_1, 1: y_2, 2: y_3, 3: y_4}]
    logs.show_linear_rationed_plan_without_interaction(*parameters)

    print(logs.get_text(4, []))
    mx1, mx2, mx3, my = sum(nx1) / N, sum(nx2) / N, sum(nx3) / N, sum(y_average) / N
    a11, a22, a33 = 0, 0, 0
    a12, a13, a23 = 0, 0, 0
    a1, a2, a3 = 0, 0, 0
    for i in range(N):
        a11 += nx1[i] ** 2
        a22 += nx2[i] ** 2
        a33 += nx3[i] ** 2
        a12 += nx1[i] * nx2[i]
        a13 += nx1[i] * nx3[i]
        a23 += nx2[i] * nx3[i]
        a1 += y_average[i] * nx1[i]
        a2 += y_average[i] * nx2[i]
        a3 += y_average[i] * nx3[i]
    a11, a22, a33 = a11 / N, a22 / N, a33 / N
    a12, a13, a23 = a12 / N, a13 / N, a23 / N
    a1, a2, a3 = a1 / N, a2 / N, a3 / N
    a21 = a12
    a31 = a13
    a32 = a23

    main_det = det([[1, mx1, mx2, mx3], [mx1, a11, a12, a13], [mx2, a21, a22, a23], [mx3, a31, a32, a33]])
    A0 = det([[my, mx1, mx2, mx3], [a1, a11, a12, a13], [a2, a21, a22, a23], [a3, a31, a32, a33]]) / main_det
    A1 = det([[1, my, mx2, mx3], [mx1, a1, a12, a13], [mx2, a2, a22, a23], [mx3, a3, a32, a33]]) / main_det
    A2 = det([[1, mx1, my, mx3], [mx1, a11, a1, a13], [mx2, a21, a2, a23], [mx3, a31, a3, a33]]) / main_det
    A3 = det([[1, mx1, mx2, my], [mx1, a11, a12, a1], [mx2, a21, a22, a2], [mx3, a31, a32, a3]]) / main_det
    A = [A0, A1, A2, A3]

    print(logs.get_text(6, [round(el, 4) for el in A]))
    parameters = [N, nx0, nx1, nx2, nx3, y_average, A]
    logs.show_checking_of_linear_natural_plan_without_interaction(*parameters)

    print(logs.get_text(5, []))
    B = [0, 0, 0, 0]
    for i in range(N):
        B[0] += y_average[i] * x0[i]
        B[1] += y_average[i] * x1[i]
        B[2] += y_average[i] * x2[i]
        B[3] += y_average[i] * x3[i]
    for i in range(K):
        B[i] /= N

    print(logs.get_text(7, [round(el, 4) for el in B]))
    parameters = [N, x0, x1, x2, x3, y_average, B]
    logs.show_checking_of_linear_rationed_plan_without_interaction(*parameters)

    # Перевірка критерія Стьюдента
    S2B = sum(S2_dis) / N
    S2_B = S2B / (N * m)
    S_B = sqrt(S2_B)
    t = [0, 0, 0, 0]
    for i in range(K):
        t[i] = abs(B[i]) / S_B
    f3 = f1 * f2

    print(logs.get_text(13, [f3, [round(el, 4) for el in t]]))

    d = K
    for i in range(K):
        if not cr.check_student(f3, t[i]):
            B[i] = 0
            A[i] = 0
            d -= 1

    print(logs.get_text(14, [round(el, 4) for el in A]))
    print(logs.get_text(15, [round(el, 4) for el in B]))

    # Перевірка критерія Фішера
    y_for_phisher = [0 for _ in range(N)]
    for i in range(N):
        y_for_phisher[i] = nx0[i]*A[0] + nx1[i]*A[1] + nx2[i]*A[2] + nx3[i]*A[3]
    S2ad = 0
    for i in range(N):
        S2ad += (y_for_phisher[i] - y_average[i]) ** 2
    S2ad = m * S2ad / (N - d)
    f4 = N - d
    Fp = S2ad / S2B
    print(logs.get_text(18, [f3, f4, Fp]))
    ext_data = [N, y_average, A, B]
    return cr.check_phisher(f3, f4, Fp)


def linear_model_with_interaction():
    global ext_data
    print(logs.get_text(20, []))
    print(logs.get_text(21, []))
    print(logs.get_text(1, []))

    x0.extend(px0)
    x1.extend(px1)
    x2.extend(px2)
    x3.extend(px3)
    nx0.extend(pnx0)
    nx1.extend(pnx1)
    nx2.extend(pnx2)
    nx3.extend(pnx3)
    N = 8
    K = 8
    m = 3

    print(logs.get_text(2, [N, K, m]))
    print(logs.get_text(3, []))

    y_1 = [randint(y_min, y_max) for _ in range(m)]
    y_2 = [randint(y_min, y_max) for _ in range(m)]
    y_3 = [randint(y_min, y_max) for _ in range(m)]
    y_4 = [randint(y_min, y_max) for _ in range(m)]
    y_5 = [randint(y_min, y_max) for _ in range(m)]
    y_6 = [randint(y_min, y_max) for _ in range(m)]
    y_7 = [randint(y_min, y_max) for _ in range(m)]
    y_8 = [randint(y_min, y_max) for _ in range(m)]
    y_average = []
    S2_dis = []
    f1 = 0
    f2 = 0

    def check_uniformity_of_dispersion(m):
        nonlocal y_average
        nonlocal S2_dis
        nonlocal f1
        nonlocal f2

        y_average = [sum(y_1) / m, sum(y_2) / m, sum(y_3) / m, sum(y_4) / m,
                     sum(y_5) / m, sum(y_6) / m, sum(y_7) / m, sum(y_8) / m]

        S2_dis = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(m):
            S2_dis[0] += (y_1[i] - y_average[0]) ** 2
            S2_dis[1] += (y_2[i] - y_average[1]) ** 2
            S2_dis[2] += (y_3[i] - y_average[2]) ** 2
            S2_dis[3] += (y_4[i] - y_average[3]) ** 2
            S2_dis[4] += (y_5[i] - y_average[4]) ** 2
            S2_dis[5] += (y_6[i] - y_average[5]) ** 2
            S2_dis[6] += (y_7[i] - y_average[6]) ** 2
            S2_dis[7] += (y_8[i] - y_average[7]) ** 2
        for i in range(N):
            S2_dis[i] /= m

        Gp = max(S2_dis) / sum(S2_dis)
        f1 = m - 1
        f2 = N
        print(logs.get_text(10, [f1, f2, Gp]))
        return cr.check_kohren(f1, f2, Gp)

    while not check_uniformity_of_dispersion(m):
        print(logs.get_text(12, []))
        y_1.append(randint(y_min, y_max))
        y_2.append(randint(y_min, y_max))
        y_3.append(randint(y_min, y_max))
        y_4.append(randint(y_min, y_max))
        y_5.append(randint(y_min, y_max))
        y_6.append(randint(y_min, y_max))
        y_7.append(randint(y_min, y_max))
        y_8.append(randint(y_min, y_max))
        m += 1
        print(logs.get_text(2, [N, K, m]))

    # Пошук коефіцієнтів
    print(logs.get_text(11, []))
    parameters = [m, N, nx1, nx2, nx3, {0: y_1, 1: y_2, 2: y_3, 3: y_4, 4: y_5, 5: y_6, 6: y_7, 7: y_8}]
    logs.show_linear_natural_plan_with_interaction(*parameters)

    parameters = [m, N, x0, x1, x2, x3, {0: y_1, 1: y_2, 2: y_3, 3: y_4, 4: y_5, 5: y_6, 6: y_7, 7: y_8}]
    logs.show_linear_rationed_plan_with_interaction(*parameters)

    print(logs.get_text(4, []))
    m00, m10, m20, m30, m40, m50, m60, m70, k0 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    m01, m11, m21, m31, m41, m51, m61, m71, k1 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    m02, m12, m22, m32, m42, m52, m62, m72, k2 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    m03, m13, m23, m33, m43, m53, m63, m73, k3 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    m04, m14, m24, m34, m44, m54, m64, m74, k4 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    m05, m15, m25, m35, m45, m55, m65, m75, k5 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    m06, m16, m26, m36, m46, m56, m66, m76, k6 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    m07, m17, m27, m37, m47, m57, m67, m77, k7 = 0, 0, 0, 0, 0, 0, 0, 0, 0

    for i in range(N):
        m00 = N
        m10 += nx1[i]
        m20 += nx2[i]
        m30 += nx3[i]
        m40 += nx1[i] * nx2[i]
        m50 += nx1[i] * nx3[i]
        m60 += nx2[i] * nx3[i]
        m70 += nx1[i] * nx2[i] * nx3[i]
        k0 += y_average[i]
        m01 += nx1[i]
        m11 += nx1[i] ** 2
        m21 += nx1[i] * nx2[i]
        m31 += nx1[i] * nx3[i]
        m41 += (nx1[i] ** 2) * nx2[i]
        m51 += (nx1[i] ** 2) * nx3[i]
        m61 += nx1[i] * nx2[i] * nx3[i]
        m71 += (nx1[i] ** 2) * nx2[i] * nx3[i]
        k1 += y_average[i] * nx1[i]
        m02 += nx2[i]
        m12 += nx1[i] * nx2[i]
        m22 += nx2[i] ** 2
        m32 += nx2[i] * nx3[i]
        m42 += nx1[i] * (nx2[i] ** 2)
        m52 += nx1[i] * nx2[i] * nx3[i]
        m62 += (nx2[i] ** 2) * nx3[i]
        m72 += nx1[i] * (nx2[i] ** 2) * nx3[i]
        k2 += y_average[i] * nx2[i]
        m03 += nx3[i]
        m13 += nx1[i] * nx3[i]
        m23 += nx2[i] * nx3[i]
        m33 += nx3[i] ** 2
        m43 += nx1[i] * nx2[i] * nx3[i]
        m53 += nx1[i] * (nx3[i] ** 2)
        m63 += nx2[i] * (nx3[i] ** 2)
        m73 += nx1[i] * nx2[i] * (nx3[i] ** 2)
        k3 += y_average[i] * nx3[i]
        m04 += nx1[i] * nx2[i]
        m14 += (nx1[i] ** 2) * nx2[i]
        m24 += nx1[i] * (nx2[i] ** 2)
        m34 += nx1[i] * nx2[i] * nx3[i]
        m44 += (nx1[i] ** 2) * (nx2[i] ** 2)
        m54 += (nx1[i] ** 2) * nx2[i] * nx3[i]
        m64 += nx1[i] * (nx2[i] ** 2) * nx3[i]
        m74 += (nx1[i] ** 2) * (nx2[i] ** 2) * nx3[i]
        k4 += y_average[i] * nx1[i] * nx2[i]
        m05 += nx1[i] * nx3[i]
        m15 += (nx1[i] ** 2) * nx3[i]
        m25 += nx1[i] * nx2[i] * nx3[i]
        m35 += nx1[i] * (nx3[i] ** 2)
        m45 += (nx1[i] ** 2) * nx2[i] * nx3[i]
        m55 += (nx1[i] ** 2) * (nx3[i] ** 2)
        m65 += nx1[i] * nx2[i] * (nx3[i] ** 2)
        m75 += (nx1[i] ** 2) * nx2[i] * (nx3[i] ** 2)
        k5 += y_average[i] * nx1[i] * nx3[i]
        m06 += nx2[i] * nx3[i]
        m16 += nx1[i] * nx2[i] * nx3[i]
        m26 += (nx2[i] ** 2) * nx3[i]
        m36 += nx2[i] * (nx3[i] ** 2)
        m46 += nx1[i] * (nx2[i] ** 2) * nx3[i]
        m56 += nx1[i] * nx2[i] * (nx3[i] ** 2)
        m66 += (nx2[i] ** 2) * (nx3[i] ** 2)
        m76 += nx1[i] * (nx2[i] ** 2) * (nx3[i] ** 2)
        k6 += y_average[i] * nx2[i] * nx3[i]
        m07 += nx1[i] * nx2[i] * nx3[i]
        m17 += (nx1[i] ** 2) * nx2[i] * nx3[i]
        m27 += nx1[i] * (nx2[i] ** 2) * nx3[i]
        m37 += nx1[i] * nx2[i] * (nx3[i] ** 2)
        m47 += (nx1[i] ** 2) * (nx2[i] ** 2) * nx3[i]
        m57 += (nx1[i] ** 2) * nx2[i] * (nx3[i] ** 2)
        m67 += nx1[i] * (nx2[i] ** 2) * (nx3[i] ** 2)
        m77 += (nx1[i] ** 2) * (nx2[i] ** 2) * (nx3[i] ** 2)
        k7 += y_average[i] * nx1[i] * nx2[i] * nx3[i]

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

    A = [A0, A1, A2, A3, A4, A5, A6, A7]

    print(logs.get_text(8, [round(el, 4) for el in A]))
    parameters = [N, nx1, nx2, nx3, y_average, A]
    logs.show_checking_of_linear_natural_plan_with_interaction(*parameters)

    print(logs.get_text(5, []))

    B = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(N):
        B[0] += y_average[i] * x0[i]
        B[1] += y_average[i] * x1[i]
        B[2] += y_average[i] * x2[i]
        B[3] += y_average[i] * x3[i]
        B[4] += y_average[i] * x1[i] * x2[i]
        B[5] += y_average[i] * x1[i] * x3[i]
        B[6] += y_average[i] * x2[i] * x3[i]
        B[7] += y_average[i] * x1[i] * x2[i] * x3[i]
    for i in range(K):
        B[i] /= N

    print(logs.get_text(9, [round(el, 4) for el in B]))
    parameters = [N, x0, x1, x2, x3, y_average, B]
    logs.show_checking_of_linear_rationed_plan_with_interaction(*parameters)

    # Перевірка критерія Стьюдента
    S2B = sum(S2_dis) / N
    S2_B = S2B / (N * m)
    S_B = sqrt(S2_B)
    t = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(K):
        t[i] = abs(B[i]) / S_B
    f3 = f1 * f2

    print(logs.get_text(13, [f3, [round(el, 4) for el in t]]))

    d = K
    for i in range(K):
        if not cr.check_student(f3, t[i]):
            B[i] = 0
            A[i] = 0
            d -= 1

    print(logs.get_text(16, [round(el, 4) for el in A]))
    print(logs.get_text(17, [round(el, 4) for el in B]))
    # Перевірка критерія Фішера
    y_for_phisher = [0 for _ in range(N)]
    for i in range(N):
        y_for_phisher[i] = A[0] * nx0[i]  + A[1] * nx1[i] + A[2] * nx2[i] + A[3] * nx3[i] + A[4] * nx1[i] * nx2[i] + \
            A[5] * nx1[i] * nx3[i] + A[6] * nx2[i] * nx3[i] + A[7] * nx1[i] * nx2[i] * nx3[i]
    S2ad = 0
    for i in range(N):
        S2ad += (y_for_phisher[i] - y_average[i]) ** 2
    S2ad = m * S2ad / (N - d)
    f4 = N - d
    Fp = S2ad / S2B

    print(logs.get_text(18, [f3, f4, Fp]))
    ext_data = [N, y_average, A, B]
    return cr.check_phisher(f3, f4, Fp)


def view_result_without_interaction():
    print(logs.get_text(22, []))
    N = ext_data[0]
    y_average = ext_data[1]
    A = ext_data[2]
    B = ext_data[3]
    parameters = [N, nx0, nx1, nx2, nx3, y_average, A]
    logs.show_checking_of_linear_natural_plan_without_interaction(*parameters)
    parameters = [N, x0, x1, x2, x3, y_average, B]
    logs.show_checking_of_linear_rationed_plan_without_interaction(*parameters)


def view_result_with_interaction():
    print(logs.get_text(22, []))
    N = ext_data[0]
    y_average = ext_data[1]
    A = ext_data[2]
    B = ext_data[3]
    parameters = [N, nx1, nx2, nx3, y_average, A]
    logs.show_checking_of_linear_natural_plan_with_interaction(*parameters)
    parameters = [N, x0, x1, x2, x3, y_average, B]
    logs.show_checking_of_linear_rationed_plan_with_interaction(*parameters)


def main():
    while True:
        basic_configuration()
        if linear_model_without_interaction():
            print(logs.get_text(19, []))
            view_result_without_interaction()
            break
        elif linear_model_with_interaction():
            print(logs.get_text(19, []))
            view_result_with_interaction()
            break
        print(logs.get_text(23, []))


if __name__ == "__main__":
    main()
