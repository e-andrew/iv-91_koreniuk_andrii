from random import randint
from beautifultable import BeautifulTable

FACTOR_MAX_SIZE = 20
A0, A1, A2, A3 = [randint(1, 50) for _ in range(4)]

x1 = [randint(0, FACTOR_MAX_SIZE) for _ in range(8)]
x2 = [randint(0, FACTOR_MAX_SIZE) for _ in range(8)]
x3 = [randint(0, FACTOR_MAX_SIZE) for _ in range(8)]
x0 = [(max(x1)+min(x1))/2, (max(x2)+min(x2))/2, (max(x3)+min(x3))/2]
dx = [max(x1) - x0[0], max(x2) - x0[1], max(x3) - x0[2]]
nx1 = list()
nx2 = list()
nx3 = list()
response_function = list()
y_et = A0 + A1 * x0[0] + A2 * x0[1] + A3 * x0[2]
criterion = list()

for i in range(8):
    nx1.append((x1[i] - x0[0])/dx[0])
    nx2.append((x2[i] - x0[1])/dx[1])
    nx3.append((x3[i] - x0[2])/dx[2])
    y = A0 + A1 * x1[i] + A2 * x2[i] + A3 * x3[i]
    response_function.append(y)
    criterion.append((y - y_et) ** 2)

opt = criterion.index(min(criterion))

plan_matrix = BeautifulTable()
plan_matrix.column_headers = ["№", "X1", "X2", "X3", "Нормоване X1", "Нормоване X2", "Нормоване X3",
                              "Значення Y", "Дані критерія вибору"]
for i in range(8):
    plan_matrix.append_row([i + 1, x1[i], x2[i], x3[i], nx1[i], nx2[i], nx3[i], response_function[i], criterion[i]])
plan_matrix.append_row(["x0", x0[0], x0[1], x0[2], "", "", "", y_et, ""])
plan_matrix.append_row(["dx", dx[0], dx[1], dx[2], "", "", "", "", ""])
print(plan_matrix)
print(f"Шуканий вираз функції відгуку: {A0} + {A1} * {x1[opt]} + {A2} * {x2[opt]} + {A3} * {x3[opt]} = {response_function[opt]}")
