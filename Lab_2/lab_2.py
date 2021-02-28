from random import randint
from math import sqrt
from numpy.linalg import det
from beautifultable import BeautifulTable

"""Довірча ймовірність p = 0.9"""
romanovsky_table = {(2, 3, 4): 1.69, (5, 6, 7): 2.0, (8, 9): 2.17, (10, 11): 2.29,
                    (12, 13): 2.39, (14, 15, 16, 17): 2.49, (18, 19, 20): 2.62}

variant = {"n": 114, "x1min": -25, "x1max": 75, "x2min": 25, "x2max": 65}
y_min = (20 - variant["n"]) * 10
y_max = (30 - variant["n"]) * 10
x1 = [-1, -1, 1]
x2 = [-1, 1, -1]
nx1 = [variant["x1min"] if x1[i] == -1 else variant["x1max"] for i in range(3)]
nx2 = [variant["x2min"] if x2[i] == -1 else variant["x2max"] for i in range(3)]

m = 5
y_1 = [randint(y_min, y_max) for _ in range(m)]
y_2 = [randint(y_min, y_max) for _ in range(m)]
y_3 = [randint(y_min, y_max) for _ in range(m)]

y_average = [0, 0, 0]
y_dis = [0, 0, 0]
f_uv = [0, 0, 0]
sigma_uv = [0, 0, 0]
r_uv = [0, 0, 0]
main_divergence = 0
romanovsky_value = 0


def romanovsky_criterion():
    global y_average
    global y_dis
    global f_uv
    global sigma_uv
    global r_uv
    global main_divergence
    global romanovsky_value

    y_average = [sum(y_1)/m, sum(y_2)/m, sum(y_3)/m]
    y_dis = [0, 0, 0]

    for i in range(m):
        y_dis[0] += (y_1[i] - y_average[0]) ** 2
        y_dis[1] += (y_2[i] - y_average[1]) ** 2
        y_dis[2] += (y_3[i] - y_average[2]) ** 2

    for i in range(3):
        y_dis[i] /= m

    main_divergence = 2 * sqrt((m - 1)/(m * (m - 4)))
    uv_pairs = [[y_dis[0], y_dis[1]], [y_dis[1], y_dis[2]], [y_dis[2], y_dis[0]]]

    f_uv = list()
    sigma_uv = list()
    r_uv = list()
    for i in range(3):
        f_uv.append(max(uv_pairs[i]) / min(uv_pairs[i]))
        sigma_uv.append(f_uv[i] * (m - 2) / m)
        r_uv.append(abs(sigma_uv[i] - 1)/main_divergence)

    for key in romanovsky_table.keys():
        if m in key:
            romanovsky_value = romanovsky_table[key]
            break
    return max(r_uv) <= romanovsky_value


while not romanovsky_criterion():
    y_1.append(randint(y_min, y_max))
    y_2.append(randint(y_min, y_max))
    y_3.append(randint(y_min, y_max))
    m += 1


mx1, mx2, my = sum(x1) / 3, sum(x2) / 3, sum(y_average) / 3
a1, a2, a3, a11, a22 = 0, 0, 0, 0, 0

for i in range(3):
    a1 += x1[i] ** 2
    a2 += x1[i] * x2[i]
    a3 += x2[i] ** 2
    a11 += x1[i] * y_average[i]
    a22 += x2[i] * y_average[i]

a1, a2, a3, a11, a22 = a1 / 3, a2 / 3, a3 / 3, a11 / 3, a22/3

main_det = det([[1, mx1, mx2], [mx1, a1, a2], [mx2, a2, a3]])
B0 = det([[my, mx1, mx2], [a11, a1, a2], [a22, a2, a3]]) / main_det
B1 = det([[1, my, mx2], [mx1, a11, a2], [mx2, a22, a3]]) / main_det
B2 = det([[1, mx1, my], [mx1, a1, a11], [mx2, a2, a22]]) / main_det

dx1 = abs(variant["x1max"] - variant["x1min"]) / 2
dx2 = abs(variant["x2max"] - variant["x2min"]) / 2
x10 = (variant["x1max"] + variant["x1min"]) / 2
x20 = (variant["x2max"] + variant["x2min"]) / 2

A0 = B0 - B1 * x10 / dx1 - B2 * x20 / dx2
A1 = B1 / dx1
A2 = B2 / dx2

plan_m = BeautifulTable()
romanovsky_m = BeautifulTable()
rationed_checking_m = BeautifulTable()
natural_checking_m = BeautifulTable()

y_headers = [f"Y{i+1}" for i in range(m)]
plan_m.column_headers = ["№", "Rationed X1", "Rationed X2", *y_headers]
romanovsky_m.column_headers = ["№", "Average Y[j]", "Dispersion Y[j]", "Number uv", "F[uv]", "θ[uv]", "R[uv]"]
rationed_checking_m.column_headers = ["№", "Rationed X1", "Rationed X2", "Average Y[j]", "Experimental Y[j]"]
natural_checking_m.column_headers = ["№", "Natured X1", "Natured X2", "Average Y[j]", "Experimental Y[j]"]

y = {0: y_1, 1: y_2, 2: y_3}
uv = [12, 23, 31]
for i in range(3):
    plan_m.append_row([i+1, x1[i], x2[i], *y[i]])
    romanovsky_m.append_row([i+1, y_average[i], y_dis[i], uv[i], f_uv[i], sigma_uv[i], r_uv[i]])
    rationed_checking_m.append_row([i+1, x1[i], x2[i], y_average[i], B0 + B1 * x1[i] + B2 * x2[i]])
    natural_checking_m.append_row([i+1, nx1[i], nx2[i], y_average[i], A0 + A1 * nx1[i] + A2 * nx2[i]])

print(plan_m, "\n")
print(romanovsky_m)
print(f"Main Divergence: {main_divergence}")
print(f"Romanovsky Criterion: {romanovsky_value}", "\n")
print(f"y = {B0} + {B1} * x1 + {B2} * x2")
print(rationed_checking_m, "\n")
print(f"y = {A0} + {A1} * x1 + {A2} * x2")
print(natural_checking_m)
