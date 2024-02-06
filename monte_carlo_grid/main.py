import random
import time
from typing import List, Tuple

import numpy as np
from numpy import e as exp, zeros
from numpy.linalg import linalg
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.ndimage import gaussian_filter

# http://math.phys.msu.ru/data/27/OMM_Task02.pdf


def func(x: int, z: int, f0: float, betta: float, x0: int, z0: int) -> float:  # Функция правой части уравнения
    return f0 * (exp ** (-1 * betta * ((x - x0) ** 2) * ((z - z0) ** 2)))


def get_correct_number(i: int, j: int, a: int, b: int, c: int, d: int, e: int, f: int) -> int | None:
    if c < j < d and e < i < f:
        return None
    return i * a + j if -1 < i < b and -1 < j < a else None


def get_border_condition(i: int, j: int, a: int, b: int, c: int, d: int, e: int, f: int) -> bool:
    return (
            (j == c or j == d) and e <= i <= f
            or
            (i == e or i == f) and c <= j <= d
            or
            i == 0 or i == (b - 1) or j == 0 or j == (a - 1)
    )


def get_empty_columns(a: int, c: int, d: int, e: int, f: int) -> List[int]:
    empties = []
    for j in range(c + 1, d):
        for i in range(e + 1, f):
            empties.append(i * a + j)
    return empties


def get_new_i_j(i: int, j: int) -> Tuple[int, int]:
    new_i = i
    new_j = j
    choice = random.choices([1, 2, 3, 4], weights=[25, 25, 25, 25])[0]
    match choice:
        case 1:
            new_i = i - 1
        case 2:
            new_i = i + 1
        case 3:
            new_j = j - 1
        case 4:
            new_j = j + 1
        case _:
            raise Exception('Something wrong with random')
    return new_i, new_j


PASSED_COORDINATES = set()
TOTAL_COUNT = 0


def get_probabilistic_value(
        i: int, j: int, a: int, b: int, c: int, d: int, e: int, f: int,
        f0: float, betta: float, x0: int, z0: int, u0: int, k: float,
) -> [float, int]:
    passed_coordinates = set()
    sum_probabilistic_values = 0
    path_length = 1

    while not get_border_condition(i, j, a, b, c, d, e, f):
        sum_probabilistic_values += -0.9 * func(i, j, f0, betta, x0, z0) / k
        path_length += 1

        coordinates = get_new_i_j(i, j)
        count = 0

        while coordinates in passed_coordinates:
            coordinates = get_new_i_j(i, j)
            count += 1
            if count > 10:
                break

        i, j = coordinates
        passed_coordinates.add(coordinates)

    sum_probabilistic_values += u0
    return sum_probabilistic_values, path_length

    # if get_border_condition(i, j, a, b, c, d, e, f):
    #     PASSED_COORDINATES = set()
    #     TOTAL_COUNT += 1
    #     return u0, 1
    # else:
    #     coordinates = get_new_i_j(i, j)
    #     count = 0
    #
    #     while coordinates in PASSED_COORDINATES:
    #         coordinates = get_new_i_j(i, j)
    #         count += 1
    #         if count > 10:
    #             break
    #
    #     new_i, new_j = coordinates
    #     PASSED_COORDINATES.add(coordinates)
    #     func_value, length = get_probabilistic_value(new_i, new_j, a, b, c, d, e, f, f0, betta, x0, z0, u0, k)
    #     return  + func_value, length + 1


def get_matrix_a(a: int, b: int, c: int, d: int, e: int, f: int, n: int, not_empty_n: int) -> np.ndarray:
    not_empty_a = zeros([not_empty_n, n])

    index = -1

    for num in range(n):
        i = num // a
        j = num % a

        if c < j < d and e < i < f:
            continue
        else:
            index += 1

        not_empty_a[index, num] = 1

        if get_border_condition(i, j, a, b, c, d, e, f):
            continue

        left = get_correct_number(i, j - 1, a, b, c, d, e, f)
        right = get_correct_number(i, j + 1, a, b, c, d, e, f)
        top = get_correct_number(i - 1, j, a, b, c, d, e, f)
        bottom = get_correct_number(i + 1, j, a, b, c, d, e, f)

        if left is not None:
            not_empty_a[index, left] = -1 / 4
        if right is not None:
            not_empty_a[index, right] = -1 / 4
        if top is not None:
            not_empty_a[index, top] = -1 / 4
        if bottom is not None:
            not_empty_a[index, bottom] = -1 / 4

    not_empty_a = np.delete(not_empty_a, get_empty_columns(a, c, d, e, f), axis=1)
    return not_empty_a


def get_matrix_b(
        a: int, b: int, c: int, d: int, e: int, f: int, n: int, not_empty_n: int,
        u0: int, f0: float, betta: float, x0: int, z0: int, dx: int, k: float, F0: int,
) -> np.ndarray:
    not_empty_b = zeros([not_empty_n, 1])

    index = -1
    for num in range(n):
        i = num // a
        j = num % a

        if c < j < d and e < i < f:
            # если ячейка попадает за внутренние границы пропускаем
            continue
        else:
            index += 1

        # if j == 0:
        #     not_empty_b[index] = func(i, j, f0, betta, x0, z0) * dx ** 2 / (4 * F0)
        if get_border_condition(i, j, a, b, c, d, e, f):
            # если ячейка находится на границе приравниваем значение u0
            not_empty_b[index] = u0
        else:
            # если ячейка не находится на границе вычисляем функцию
            not_empty_b[index] = (func(i, j, f0, betta, x0, z0) * (dx ** 2)) / (-4 * k)
    return not_empty_b


def get_matrix_by(
        a: int, b: int, c: int, d: int, e: int, f: int,
        u0: int, f0: float, betta: float, x0: int, z0: int, dx: int, k: float, F0: int,
) -> np.ndarray:
    n = a * b
    empty_n = (d - 1 - c) * (f - 1 - e)
    not_empty_n = n - empty_n

    # получаем матрицу коэффициентов
    not_empty_a = get_matrix_a(a, b, c, d, e, f, n, not_empty_n)
    # получаем матрицу значений
    not_empty_b = get_matrix_b(a, b, c, d, e, f, n, not_empty_n, u0, f0, betta, x0, z0, dx, k, F0)

    u = linalg.solve(not_empty_a, not_empty_b).T

    u_index = 0
    total_u = zeros([b, a])
    for num in range(n):
        i = num // a
        j = num % a

        if c < j < d and e < i < f:
            total_u[i, j] = -273
        else:
            total_u[i, j] = u[0][u_index]
            u_index += 1

    return total_u


def get_matrix_by_statistical_method(
        a: int, b: int, c: int, d: int, e: int, f: int,
        u0: int, f0: float, betta: float, x0: int, z0: int, k: float, N: int,
) -> np.ndarray:
    probabilistic_values = zeros([b, a])

    for j in range(a):
        for i in range(b):
            if c < j < d and e < i < f:
                probabilistic_values[i, j] = -273
            # elif not( i == x0 and j == z0):
            #     continue
            else:
                count = 0
                sum_probabilistic_values = 0

                while count < N:
                    func_value, count_points = get_probabilistic_value(i, j, a, b, c, d, e, f, f0, betta, x0, z0, u0, k)
                    probabilistic_value = func_value
                    sum_probabilistic_values += probabilistic_value
                    count += 1

                    # if count % 50 == 0:
                    #     print(count, sum_probabilistic_values / count)

                probabilistic_values[i, j] = sum_probabilistic_values / N

        print(f'{(j + 1) * i} / {a * b} processed')

    return probabilistic_values


def enlarge_values(a, b, c, d, e, f, x0, z0, func):
    a = func(a)
    b = func(b)
    c = func(c)
    d = func(d)
    e = func(e)
    f = func(f)
    x0 = func(x0)
    z0 = func(z0)
    return a, b, c, d, e, f, x0, z0


def main() -> None:
    # const
    u0 = 300
    F0 = 30

    # user inputs

    a = int(input('Введите длину внешней границы по оси x (a) (по умолчанию 100): ') or 100)
    b = int(input('Введите длину внешней границы по оси z (b) (по умолчанию 100): ') or 100)
    c = int(input('Введите левую границу внутреннего прямоугольника по оси x (c) (по умолчанию 10): ') or 10)
    d = int(input('Введите правую границу внутреннего прямоугольника по оси x (d) (по умолчанию 50): ') or 50)
    e = int(input('Введите нижнюю границу внутреннего прямоугольника по оси z (e) (по умолчанию 10): ') or 10)
    f = int(input('Введите верхнюю границу внутреннего прямоугольника по оси z (f) (по умолчанию 60): ') or 60)

    x0 = int(input('Введите координату центра источника тепла по оси x (по умолчанию 70): ') or 70)
    z0 = int(input('Введите координату центра источника тепла по оси z (по умолчанию 80): ') or 80)

    f0 = float(input('Введите значение переменной f0 функции источника тепла (по умолчанию -200): ') or -120)
    betta = float(input('Введите значение переменной betta функции источника тепла (по умолчанию 0.01): ') or 0.01)

    k = float(input('Введите значение коэффициента k (по умолчанию 2): ') or 2)

    N = int(input('Введите количество подсчитывания цепочки случайной величины (по умолчанию 500): ') or 500)

    dx = 1

    # a, b, c, d, e, f, x0, z0 = enlarge_values(a, b, c, d, e, f, x0, z0, lambda x: int(x / 2))

    print(f'Values: ', a, b, c, d, e, f, x0, z0)
    # start_time = time.monotonic()
    # analytics_matrix = get_matrix_by(a, b, c, d, e, f, u0, f0, betta, x0, z0, dx, k, F0)
    # a_u_max = analytics_matrix.max()
    # print(f'Метод конечных разностей {f0}, {betta}, {k}: {a_u_max}. Spend time: {time.monotonic() - start_time}')

    start_time = time.monotonic()
    probabilistic_matrix = get_matrix_by_statistical_method(a, b, c, d, e, f, u0, f0, betta, x0, z0, k, N)
    p_u_max = probabilistic_matrix.max()
    print(f'Метод Монте-Карло {f0}, {betta}, {k}: {p_u_max}. Spend time: {time.monotonic() - start_time}')

    # print(f'Значения функции U, полученные аналитическим методом:\n{analytics_matrix}')
    # print(f'Значения функции U, полученные вероятностным методом:\n{probabilistic_matrix}')

    # plt.imshow(analytics_matrix)
    # plt.colorbar()
    # plt.show()
    #
    # plt.imshow(probabilistic_matrix)
    # plt.colorbar()
    # plt.show()

    # fig, ax = plt.subplots(figsize=(5, 5))
    # ax.set_title("Значения функции U, полученные методом конечных разностей", size=10)
    # sns.heatmap(analytics_matrix, vmin=-273, vmax=3000, cbar=True)
    # plt.show()

    # конечных разностей: 2942.5786400445586 t = 9.9 sec
    # Монте-Карло: 2934.8047468578625 t = 4.1 sec

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_title("Значения функции U, полученные методом Монте-Карло", size=10)
    sns.heatmap(probabilistic_matrix, cbar=True)
    plt.show()


if __name__ == '__main__':
    main()
