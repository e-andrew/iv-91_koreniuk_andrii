from beautifultable import BeautifulTable

SYSTEM_MARK_L = "Action: "
SYSTEM_MARK_V = "View: "

text = {0: "Розглянемо лінійне рівняння регресії без взаємодії факторів:\ny = b0 + b1·x1 + b2·x2 + b3·x3",
        1: "Розглянемо лінійне рівняння регресії із врахуванням взаємодії факторів:\n"
           "y = b0 + b1·x1 + b2·x2 + b3·x3 + b12·x1·x2 + b13·x1·x3 + b23·x2·x3 + b123·x1·x2·x3",
        2: "Отже, N = {0}, K = {1}, m = {2}.",
        3: "Складаємо матрицю планування і проведимо експерименти",
        4: "Розраховуємо натуральні значення коефіцієнтів.",
        5: "Розраховуємо кодовані значення коефіцієнтів.",
        6: "Рівняння регресії має вигляд (нат. знач. коеф.):\n" +
           "y = {0} + {1}·x1 + {2}·x2 + {3}·x3",
        7: "Рівняння регресії має вигляд (код. знач. коеф.):\n" +
           "y = {0} + {1}·x1 + {2}·x2 + {3}·x3",
        8: "Рівняння регресії має вигляд (нат. знач. коеф.):\n" +
           "y = {0} + {1}·x1 + {2}·x2 + {3}·x3 + {4}·x1·x2 + {5}·x1·x3 + {6}·x2·x3 + {7}·x1·x2·x3",
        9: "Рівняння регресії має вигляд (код. знач. коеф.):\n" +
           "y = {0} + {1}·x1 + {2}·x2 + {3}·x3 + {4}·x1·x2 + {5}·x1·x3 + {6}·x2·x3 + {7}·x1·x2·x3",
        10: "Перевіряємо однорідність дисперсії за критерієм Кохрена. f1 = {0}, f2 = {1}, Gp = {2}.",
        11: "Дисперсія однорідна.",
        12: "Дисперсія не однорідна. Збільшуємо m на 1.",
        13: "Перевіряємо нуль гіпотезу та корегуємо рівняння регресії:\n" +
            "f3 = {0}, t = {1}.",
        14: "Нове рівняння регресії має вигляд (нат. знач. коеф.):\n" +
            "y = {0} + {1}·x1 + {2}·x2 + {3}·x3",
        15: "Нове рівняння регресії має вигляд (код. знач. коеф.):\n" +
            "y = {0} + {1}·x1 + {2}·x2 + {3}·x3",
        16: "Нове рівняння регресії має вигляд (нат. знач. коеф.):\n" +
            "y = {0} + {1}·x1 + {2}·x2 + {3}·x3 + {4}·x1·x2 + {5}·x1·x3 + {6}·x2·x3 + {7}·x1·x2·x3",
        17: "Нове рівняння регресії має вигляд (код. знач. коеф.):\n" +
            "y = {0} + {1}·x1 + {2}·x2 + {3}·x3 + {4}·x1·x2 + {5}·x1·x3 + {6}·x2·x3 + {7}·x1·x2·x3",
        18: "Перевіряємо адекватність моделі.\n" +
            "f3 = {0}, f4 = {1}, Fp = {2}",
        19: "Модель адекватна оригіналу.",
        20: "Модель не адекватна оригіналу.",
        21: "Змінюємо рівняння регресії.",
        22: "Виводимо результати.",
        23: "Оскільки всі моделі не адекватні, то почнемо експерименти з початку.",
        24: "Перевірка критерія Кохрена займає: {0}",
        25: "Перевірка критерія Стьюдента займає: {0}",
        26: "Перевірка критерія Фішера займає: {0}"}


def get_text(key, par):
    return SYSTEM_MARK_L + text[key].format(*par)


views = {0: "Матриця планування експерименту (нат. знач. коеф., без взаємодії)",
         1: "Матриця планування експерименту (код. знач. коеф., без взаємодії)",
         2: "Матриця планування експерименту (нат. знач. коеф., із взаємодією)",
         3: "Матриця планування експерименту (код. знач. коеф., із взаємодією)",
         4: "Перевірка знайдених коефіцієнтів (нат. знач. коеф., без взаємодії)",
         5: "Перевірка знайдених коефіцієнтів (код. знач. коеф., без взаємодії)",
         6: "Перевірка знайдених коефіцієнтів (нат. знач. коеф., із взаємодією)",
         7: "Перевірка знайдених коефіцієнтів (код. знач. коеф., із взаємодією)"}


"""y = {0: y_1, 1: y_2, ...}"""
def show_linear_natural_plan_without_interaction(m, N, nx1, nx2, nx3, y):
    print(SYSTEM_MARK_V + views[0])
    natural_plan = BeautifulTable()
    y_headers = [f"Y{i + 1}" for i in range(m)]
    natural_plan.column_headers = ["№", "X1", "X2", "X3", *y_headers]
    for i in range(N):
        natural_plan.append_row([i + 1, nx1[i], nx2[i], nx3[i], *y[i]])
    print(natural_plan, "\n")


def show_linear_rationed_plan_without_interaction(m, N, x0, x1, x2, x3, y):
    print(SYSTEM_MARK_V + views[1])
    rationed_plan = BeautifulTable()
    y_headers = [f"Y{i + 1}" for i in range(m)]
    rationed_plan.column_headers = ["№", "X0", "X1", "X2", "X3", *y_headers]
    for i in range(N):
        rationed_plan.append_row([i + 1, x0[i], x1[i], x2[i], x3[i], *y[i]])
    print(rationed_plan, "\n")


def show_linear_natural_plan_with_interaction(m, N, nx1, nx2, nx3, y):
    print(SYSTEM_MARK_V + views[2])
    natural_plan = BeautifulTable()
    y_headers = [f"Y{i + 1}" for i in range(m)]
    natural_plan.column_headers = ["№", "X1", "X2", "X3", "X1·X2", "X1·X3", "X2·X3", "X1·X2·X3", *y_headers]
    for i in range(N):
        natural_plan.append_row([i+1, nx1[i], nx2[i], nx3[i], nx1[i]*nx2[i], nx1[i]*nx3[i], nx2[i]*nx3[i], nx1[i]*nx2[i]*nx3[i], *y[i]])
    print(natural_plan, "\n")


def show_linear_rationed_plan_with_interaction(m, N, x0, x1, x2, x3, y):
    print(SYSTEM_MARK_V + views[3])
    rationed_plan = BeautifulTable()
    y_headers = [f"Y{i + 1}" for i in range(m)]
    rationed_plan.column_headers = ["№", "X0", "X1", "X2", "X3", "X1·X2", "X1·X3", "X2·X3", "X1·X2·X3", *y_headers]
    for i in range(N):
        rationed_plan.append_row([i+1, x0[i], x1[i], x2[i], x3[i], x1[i]*x2[i], x1[i]*x3[i], x2[i]*x3[i], x1[i]*x2[i]*x3[i], *y[i]])
    print(rationed_plan, "\n")


def show_checking_of_linear_natural_plan_without_interaction(N, nx0, nx1, nx2, nx3, y_average, A):
    print(SYSTEM_MARK_V + views[4])
    natural_checking = BeautifulTable()
    natural_checking.column_headers = ["№", "N-red X1", "N-red X2", "N-red X3", "Average Y[j]", "Exp-tal Y[j]"]
    for i in range(N):
        y_exp = A[0] * nx0[i] + A[1] * nx1[i] + A[2] * nx2[i] + A[3] * nx3[i]
        natural_checking.append_row([i+1, nx1[i], nx2[i], nx3[i], y_average[i], y_exp])
    print(natural_checking, "\n")


def show_checking_of_linear_rationed_plan_without_interaction(N, x0, x1, x2, x3, y_average, B):
    print(SYSTEM_MARK_V + views[5])
    rationed_checking = BeautifulTable()
    rationed_checking.column_headers = ["№", "R-ned X0", "R-ned X1", "R-ned X2", "R-ned X3", "Average Y[j]",
                                          "Exp-tal Y[j]"]
    for i in range(N):
        y_exp = B[0] * x0[i] + B[1] * x1[i] + B[2] * x2[i] + B[3] * x3[i]
        rationed_checking.append_row([i+1, x0[i], x1[i], x2[i], x3[i], y_average[i], y_exp])
    print(rationed_checking, "\n")


def show_checking_of_linear_natural_plan_with_interaction(N, nx1, nx2, nx3, y_average, A):
    print(SYSTEM_MARK_V + views[6])
    natural_checking = BeautifulTable()
    natural_checking.column_headers = ["№", "X1", "X2", "X3", "X1·X2", "X1·X3", "X2·X3", "X1·X2·X3", "Average Y[j]", "Exp-tal Y[j]"]
    for i in range(N):
        x12 = nx1[i]*nx2[i]
        x13 = nx1[i]*nx3[i]
        x23 = nx2[i]*nx3[i]
        x123 = nx1[i]*nx2[i]*nx3[i]
        y_exp = A[0] + A[1]*nx1[i] + A[2]*nx2[i] + A[3]*nx3[i] + A[4]*x12 + A[5]*x13 + A[6]*x23 + A[7]*x123
        natural_checking.append_row([i+1, nx1[i], nx2[i], nx3[i], x12, x13, x23, x123, y_average[i], y_exp])
    print(natural_checking, "\n")


def show_checking_of_linear_rationed_plan_with_interaction(N, x0, x1, x2, x3, y_average, B):
    print(SYSTEM_MARK_V + views[7])
    rationed_checking = BeautifulTable()
    rationed_checking.column_headers = ["№", "X0", "X1", "X2", "X3", "X1·X2", "X1·X3", "X2·X3", "X1·X2·X3", "Average Y[j]",
                                       "Exp-tal Y[j]"]
    for i in range(N):
        x12 = x1[i] * x2[i]
        x13 = x1[i] * x3[i]
        x23 = x2[i] * x3[i]
        x123 = x1[i] * x2[i] * x3[i]
        y_exp = B[0] + B[1] * x1[i] + B[2] * x2[i] + B[3] * x3[i] + B[4] * x12 + B[5] * x13 + B[6] * x23 + B[7] * x123
        rationed_checking.append_row([i+1, x0[i], x1[i], x2[i], x3[i], x12, x13, x23, x123, y_average[i], y_exp])
    print(rationed_checking, "\n")
