from random import randint
from copy import deepcopy
from math import ceil, floor, sqrt
from numpy.linalg import det
import criterions as cr
from beautifultable import BeautifulTable

"""Довірча ймовірність p = 0.95 (критерій значимості 0.05)"""
variant = {"n": 114, "x1min": -25, "x1max": 75, "x2min": 25, "x2max": 65, "x3min": 25, "x3max": 40}
N = 4
K = 4

x_min_average = (variant["x1min"] + variant["x2min"] + variant["x3min"]) / 3
x_max_average = (variant["x1max"] + variant["x2max"] + variant["x3max"]) / 3
y_min = ceil(200 + x_min_average)
y_max = floor(200 + x_max_average)

x0 = [1, 1, 1, 1]
x1 = [-1, -1, 1, 1]
x2 = [-1, 1, -1, 1]
x3 = [-1, 1, 1, -1]

nx0 = [1, 1, 1, 1]
nx1 = [variant["x1min"] if x1[i] == -1 else variant["x1max"] for i in range(N)]
nx2 = [variant["x2min"] if x2[i] == -1 else variant["x2max"] for i in range(N)]
nx3 = [variant["x3min"] if x3[i] == -1 else variant["x3max"] for i in range(N)]

m = 3
y_1 = [randint(y_min, y_max) for _ in range(m)]
y_2 = [randint(y_min, y_max) for _ in range(m)]
y_3 = [randint(y_min, y_max) for _ in range(m)]
y_4 = [randint(y_min, y_max) for _ in range(m)]

ext_data = []


def check_model_suitability():
    global ext_data

    y_average = [sum(y_1)/m, sum(y_2)/m, sum(y_3)/m, sum(y_4)/m]

    #Перевірка критерія Кохрена
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
    if not cr.check_kohren(f1, f2, Gp):
        return False

    # Пошук коефіцієнтів
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

    B = [0, 0, 0, 0]
    for i in range(N):
        B[0] += y_average[i] * x0[i]
        B[1] += y_average[i] * x1[i]
        B[2] += y_average[i] * x2[i]
        B[3] += y_average[i] * x3[i]
    for i in range(K):
        B[i] /= N

    Ac = deepcopy(A)
    Bc = deepcopy(B)

    # Перевірка критерія Стьюдента
    S2B = sum(S2_dis) / N
    S2_B = S2B / (N * m)
    S_B = sqrt(S2_B)
    t = [0, 0, 0, 0]
    for i in range(K):
        t[i] = abs(B[i]) / S_B
    f3 = f1 * f2
    d = K
    for i in range(K):
        if not cr.check_student(f3, t[i]):
            B[i] = 0
            A[i] = 0
            d -= 1

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
    if not cr.check_phisher(f3, f4, Fp):
        return False

    ext_data = [Ac, Bc, A, B, y_average, [f1, f2, f3, f4], Gp, t, Fp]
    return True


while not check_model_suitability():
    y_1.append(randint(y_min, y_max))
    y_2.append(randint(y_min, y_max))
    y_3.append(randint(y_min, y_max))
    y_4.append(randint(y_min, y_max))
    m += 1

Ac = ext_data[0]
Bc = ext_data[1]
A = ext_data[2]
B = ext_data[3]
y_average = ext_data[4]
f = ext_data[5]
Gp = ext_data[6]
t = ext_data[7]
Fp = ext_data[8]
y = {0: y_1, 1: y_2, 2: y_3, 3: y_4}

natural_plan = BeautifulTable()
rationed_plan = BeautifulTable()
natural_checking_m = BeautifulTable()
rationed_checking_m = BeautifulTable()
new_natural_checking_m = BeautifulTable()
new_rationed_checking_m = BeautifulTable()

y_headers = [f"Y{i+1}" for i in range(m)]
natural_plan.column_headers = ["№", "N-red X1", "N-red X2", "N-red X3", *y_headers]
rationed_plan.column_headers = ["№", "R-ned X0", "R-ned X1", "R-ned X2", "R-ned X3", *y_headers]
natural_checking_m.column_headers = ["№", "N-red X1", "N-red X2", "N-red X3", "Average Y[j]", "Exp-tal Y[j]"]
rationed_checking_m.column_headers = ["№", "R-ned X0", "R-ned X1", "R-ned X2", "R-ned X3", "Average Y[j]", "Exp-tal Y[j]"]
new_natural_checking_m.column_headers = ["№", "N-red X1", "N-red X2", "N-red X3", "Average Y[j]", "Exp-tal Y[j]"]
new_rationed_checking_m.column_headers = ["№", "R-ned X0", "R-ned X1", "R-ned X2", "R-ned X3", "Average Y[j]", "Exp-tal Y[j]"]

for i in range(N):
    natural_plan.append_row([i+1, nx1[i], nx2[i], nx3[i], *y[i]])
    rationed_plan.append_row([i+1, x0[i], x1[i], x2[i], x3[i], *y[i]])
    natural_checking_m.append_row([i+1, nx1[i], nx2[i], nx3[i], y_average[i], nx0[i] * Ac[0] + Ac[1] * nx1[i] + Ac[2] * nx2[i] + Ac[3] * nx3[i]])
    rationed_checking_m.append_row([i+1, x0[i], x1[i], x2[i], x3[i], y_average[i], x0[i] * Bc[0] + Bc[1] * x1[i] + Bc[2] * x2[i] + Bc[3] * x3[i]])
    new_natural_checking_m.append_row([i+1, nx1[i], nx2[i], nx3[i], y_average[i], nx0[i] * A[0] + A[1] * nx1[i] + A[2] * nx2[i] + A[3] * nx3[i]])
    new_rationed_checking_m.append_row([i+1, x0[i], x1[i], x2[i], x3[i], y_average[i], x0[i] * B[0] + B[1] * x1[i] + B[2] * x2[i] + B[3] * x3[i]])

print("Матриця планування експерименту (натуральні значення коефіцієнтів)")
print(natural_plan, "\n")

print("Рівняння регресії до перевірки значущості коефіцієнтів (натуральних)")
print(f"{Ac[0]} + {Ac[1]} * x1 + {Ac[2]} * x2 + {Ac[3]} * x3", "\n")

print("Зробимо перевірку при натуральних значеннях коефіцієнтів")
print(natural_checking_m, "\n")

print("Матриця планування експерименту (кодовані значення коефіцієнтів)")
print(rationed_plan, "\n")

print("Рівняння регресії до перевірки значущості коефіцієнтів (кодованих)")
print(f"{Bc[0]} + {Bc[1]} * x1 + {Bc[2]} * x2 + {Bc[3]} * x3", "\n")

print("Зробимо перевірку при кодованих значеннях коефіцієнтів")
print(rationed_checking_m, "\n")

print(f"Cтупені свободи:")
print(f"* f1 = {f[0]}")
print(f"* f2 = {f[1]}")
print(f"* f3 = {f[2]}")
print(f"* f4 = {f[3]}")
print("Експериментальне значення критеріїв:")
print(f"* Кохрена - Gp = {Gp}")
print(f"* Стьюдента - t = {t}")
print(f"* Фішера - Fp = {Fp}", "\n")

print("Нове рівняння регресії (натуральні значення коефіцієнтів)")
print(f"{A[0]} + {A[1]} * x1 + {A[2]} * x2 + {A[3]} * x3", "\n")

print("Зробимо перевірку при нових натуральних значеннях коефіцієнтів")
print(new_natural_checking_m, "\n")

print("Нове рівняння регресії (кодовані значення коефіцієнтів)")
print(f"{B[0]} + {B[1]} * x1 + {B[2]} * x2 + {B[3]} * x3", "\n")

print("Зробимо перевірку при нових кодованих значеннях коефіцієнтів")
print(new_rationed_checking_m)
