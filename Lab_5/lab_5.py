from experiment import Experiment
from linear_without_interaction import LinearWithoutInteractionModel
from linear_with_interaction import LinearWithInteractionModel
from square_central_orthogonal import SquareCentralOrthogonalModel
from configuration import *
from copy import deepcopy
import logs

x = list()
nx = list()


def get_factor_lines(x, N):
    lines = list()
    for i in range(N):
        lines.append([x[0][i], x[1][i], x[2][i], x[3][i]])
    return lines


def extend_view(step, view, N):
    if step == 2:
        for i in range(N):
            view[i].append(view[i][1] * view[i][2])
            view[i].append(view[i][1] * view[i][3])
            view[i].append(view[i][2] * view[i][3])
            view[i].append(view[i][1] * view[i][2] * view[i][3])
    elif step == 3:
        for i in range(N):
            view[i].append(view[i][1] * view[i][1])
            view[i].append(view[i][2] * view[i][2])
            view[i].append(view[i][3] * view[i][3])


def linear_model_without_interaction():
    global x
    global nx
    logs.comment(0, [])
    N, K, m = 4, 4, 3
    logs.comment(3, [N, K, m])

    x = [deepcopy(x0), deepcopy(x1), deepcopy(x2), deepcopy(x3)]
    nx = [deepcopy(nx0), deepcopy(nx1), deepcopy(nx2), deepcopy(nx3)]

    logs.comment(4, [])
    # Складання плану експерименту
    x_lines = get_factor_lines(x, N)
    nx_lines = get_factor_lines(nx, N)

    # Виконання експерименту
    experiment = Experiment(y_min, y_max, m, N, q)
    lm_without = LinearWithoutInteractionModel(K, N)
    experiment.do()

    # Перевірка критерія Кохрена
    experiment.check_kohren()
    logs.comment(13, [experiment.m, experiment.f1, experiment.f2, experiment.Gp])
    logs.show_plan(0, 0, nx_lines, experiment)
    logs.show_plan(1, 0, x_lines, experiment)

    # Пошук коефіцієнтів
    logs.comment(5, [])
    lm_without.find_nature_cfs(nx, experiment.y_average)
    logs.comment(7, [round(el, 4) for el in lm_without.A])

    logs.comment(6, [])
    lm_without.find_encoded_cfs(x, experiment.y_average)
    logs.comment(8, [round(el, 4) for el in lm_without.B])

    logs.show_natured_checking_matrix(6, 0, nx_lines, lm_without, experiment)
    logs.show_encoded_checking_matrix(7, 0, x_lines, lm_without, experiment)

    # Перевірка критерія Стьюдента
    experiment.check_student(lm_without.K, lm_without.A, lm_without.B)
    logs.comment(14, [experiment.f3, [round(el, 4) for el in experiment.t]])
    logs.comment(15, [round(el, 4) for el in lm_without.A])
    logs.comment(16, [round(el, 4) for el in lm_without.B])

    # Перевірка критерія Фішера
    is_suitable = experiment.check_fisher(lm_without, nx_lines)
    logs.comment(21, [experiment.f3, experiment.f4, experiment.Fp])

    # Передача даних
    if is_suitable:
        logs.comment(22, [])
        logs.comment(25, [])
        logs.show_natured_checking_matrix(6, 0, nx_lines, lm_without, experiment)
        logs.show_encoded_checking_matrix(7, 0, x_lines, lm_without, experiment)
        del x, nx
    else:
        logs.comment(23, [])
        logs.comment(24, [])

    # Видалення зайвого
    del lm_without, experiment
    return is_suitable


def linear_model_with_interaction():
    global x
    global nx
    logs.comment(1, [])
    N, K, m = 8, 8, 3
    logs.comment(3, [N, K, m])

    x[0].extend(sp_x0)
    x[1].extend(sp_x1)
    x[2].extend(sp_x2)
    x[3].extend(sp_x3)
    nx[0].extend(sp_nx0)
    nx[1].extend(sp_nx1)
    nx[2].extend(sp_nx2)
    nx[3].extend(sp_nx3)

    logs.comment(4, [])
    # Складання плану експерименту
    x_lines = get_factor_lines(x, N)
    nx_lines = get_factor_lines(nx, N)
    x_views = deepcopy(x_lines)
    nx_views = deepcopy(nx_lines)

    extend_view(2, x_views, N)
    extend_view(2, nx_views, N)

    # Виконання експерименту
    experiment = Experiment(y_min, y_max, m, N, q)
    lm_with = LinearWithInteractionModel(K, N)
    experiment.do()

    # Перевірка критерія Кохрена
    experiment.check_kohren()
    logs.comment(13, [experiment.m, experiment.f1, experiment.f2, experiment.Gp])
    logs.show_plan(2, 1, nx_views, experiment)
    logs.show_plan(3, 1, x_views, experiment)

    # Пошук коефіцієнтів
    logs.comment(5, [])
    lm_with.find_nature_cfs(nx, experiment.y_average)
    logs.comment(9, [round(el, 4) for el in lm_with.A])

    logs.comment(6, [])
    lm_with.find_encoded_cfs(x, experiment.y_average)
    logs.comment(10, [round(el, 4) for el in lm_with.B])

    logs.show_natured_checking_matrix(8, 1, nx_views, lm_with, experiment)
    logs.show_encoded_checking_matrix(9, 1, x_views, lm_with, experiment)

    # Перевірка критерія Стьюдента
    experiment.check_student(lm_with.K, lm_with.A, lm_with.B)
    logs.comment(14, [experiment.f3, [round(el, 4) for el in experiment.t]])
    logs.comment(17, [round(el, 4) for el in lm_with.A])
    logs.comment(18, [round(el, 4) for el in lm_with.B])

    # Перевірка критерія Фішера
    is_suitable = experiment.check_fisher(lm_with, nx_lines)
    logs.comment(21, [experiment.f3, experiment.f4, experiment.Fp])

    # Передача даних
    if is_suitable:
        logs.comment(22, [])
        logs.comment(25, [])
        logs.show_natured_checking_matrix(8, 1, nx_views, lm_with, experiment)
        logs.show_encoded_checking_matrix(9, 1, x_views, lm_with, experiment)
        del x, nx
    else:
        logs.comment(23, [])
        logs.comment(24, [])

    # Видалення зайвого
    del x_views, nx_views, lm_with, experiment
    return is_suitable


def square_central_orthogonal_model():
    global x
    global nx
    logs.comment(2, [])
    N, K, m = 15, 11, 3
    logs.comment(3, [N, K, m])

    x[0].extend(tp_x0)
    x[1].extend(tp_x1)
    x[2].extend(tp_x2)
    x[3].extend(tp_x3)
    nx[0].extend(tp_nx0)
    nx[1].extend(tp_nx1)
    nx[2].extend(tp_nx2)
    nx[3].extend(tp_nx3)

    logs.comment(4, [])
    # Складання плану експерименту
    x_lines = get_factor_lines(x, N)
    nx_lines = get_factor_lines(nx, N)
    x_views = deepcopy(x_lines)
    nx_views = deepcopy(nx_lines)

    extend_view(2, x_views, N)
    extend_view(2, nx_views, N)
    extend_view(3, x_views, N)
    extend_view(3, nx_views, N)

    # Виконання експерименту
    experiment = Experiment(y_min, y_max, m, N, q)
    sq_co = SquareCentralOrthogonalModel(K, N)
    experiment.do()

    # Перевірка критерія Кохрена
    experiment.check_kohren()
    logs.comment(13, [experiment.m, experiment.f1, experiment.f2, experiment.Gp])
    logs.show_plan(4, 2, nx_views, experiment)
    logs.show_plan(5, 2, x_views, experiment)

    # Пошук коефіцієнтів
    logs.comment(5, [])
    sq_co.find_nature_cfs(experiment.m, nx, experiment.y)
    logs.comment(11, [round(el, 4) for el in sq_co.A])

    logs.comment(6, [])
    sq_co.find_encoded_cfs(experiment.m, x, experiment.y)
    logs.comment(12, [round(el, 4) for el in sq_co.B])

    logs.show_natured_checking_matrix(10, 2, nx_views, sq_co, experiment)
    logs.show_encoded_checking_matrix(11, 2, x_views, sq_co, experiment)
    # Перевірка критерія Стьюдента
    experiment.check_student(sq_co.K, sq_co.A, sq_co.B)
    logs.comment(14, [experiment.f3, [round(el, 4) for el in experiment.t]])
    logs.comment(19, [round(el, 4) for el in sq_co.A])
    logs.comment(20, [round(el, 4) for el in sq_co.B])

    # Перевірка критерія Фішера
    is_suitable = experiment.check_fisher(sq_co, nx_lines)
    logs.comment(21, [experiment.f3, experiment.f4, experiment.Fp])

    # Передача даних
    if is_suitable:
        logs.comment(22, [])
        logs.comment(25, [])
        logs.show_natured_checking_matrix(10, 2, nx_views, sq_co, experiment)
        logs.show_encoded_checking_matrix(11, 2, x_views, sq_co, experiment)
        del x, nx
    else:
        logs.comment(23, [])
        logs.comment(24, [])

    # Видалення зайвого
    del x_views, nx_views, sq_co, experiment
    return is_suitable


def main():
    while True:
        if linear_model_without_interaction():
            break
        elif linear_model_with_interaction():
            break
        elif square_central_orthogonal_model():
            break
        logs.comment(26, [])


if __name__ == "__main__":
    main()
