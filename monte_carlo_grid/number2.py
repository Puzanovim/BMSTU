from typing import List

import numpy as np
from numpy import e as exp, zeros
from numpy.linalg import linalg

# http://math.phys.msu.ru/data/27/OMM_Task02.pdf


def func(x: int, z: int, f0: float, betta: float, x0: int, z0: int) -> float:  # Функция правой части уравнения
    return f0 * (exp ** (-1 * betta * ((x - x0) ** 2) * ((z - z0) ** 2)))


def get_correct_number(i: int, j: int, a: int, b: int, c: int, d: int, e: int, f: int) -> int | None:
    if c < j < d and e < i < f:
        return None
    return i * a + j if -1 < i < b and -1 < j < a else None


def get_border_condition(i: int, j: int, a: int, b: int, c: int, d: int, e: int, f: int) -> bool:
    return (
            j == (a - 1) or j == c or j == d
            or
            i == 0 or i == (b - 1) or i == e or i == f
    )


def get_empty_columns(a: int, c: int, d: int, e: int, f: int) -> List[int]:
    empties = []
    print(f'{a}: {c}-{d}, {e}-{f}')
    for j in range(c + 1, d):
        for i in range(e + 1, f):
            empties.append(i * a + j)
    return empties


def main() -> None:
    # const
    u0 = 300
    F0 = 30

    # user input

    a = int(input('Введите длину внешней границы по оси x (a) (по умолчанию 3): ') or 3)
    b = int(input('Введите длину внешней границы по оси z (b) (по умолчанию 3): ') or 3)
    c = int(input('Введите левую границу внутреннего прямоугольника по оси x (c) (по умолчанию 1): ') or 1) - 1
    d = int(input('Введите правую границу внутреннего прямоугольника по оси x (d) (по умолчанию 3): ') or 3) - 1
    e = int(input('Введите нижнюю границу внутреннего прямоугольника по оси z (e) (по умолчанию 1): ') or 1) - 1
    f = int(input('Введите верхнюю границу внутреннего прямоугольника по оси z (f) (по умолчанию 3): ') or 3) - 1

    x0 = int(input('Введите координату центра источника тепла по оси x (по умолчанию 0): ') or 0)
    z0 = int(input('Введите координату центра источника тепла по оси z (по умолчанию 0): ') or 0)

    f0 = float(input('Введите значение переменной f0 функции источника тепла (по умолчанию 1000): ') or 1000)
    betta = float(input('Введите значение переменной betta функции источника тепла (по умолчанию 0.01): ') or 0.01)

    k = float(input('Введите значение коэффициента k (по умолчанию 2): ') or 2)

    dx = 1

    n = a * b
    empty_n = (d - 1 - c) * (f - 1 - e)
    not_empty_n = n - empty_n

    A = zeros([n, n])  # Задание матрицы коэффициентов СЛАУ размерностью n x n
    B = zeros([n, 1])  # Задание матрицы-строки свободных членов СЛАУ размерностью 1 x n

    not_empty_A = zeros([not_empty_n, n])
    not_empty_B = zeros([not_empty_n, 1])

    index = -1
    for num in range(n):
        i = num // a
        j = num % a

        if c < j < d and e < i < f:
            continue
        else:
            index += 1

        if j == 0:
            B[num] = func(i, j, f0, betta, x0, z0) * dx ** 2 / (4 * F0)
            not_empty_B[index] = func(i, j, f0, betta, x0, z0) * dx ** 2 / (4 * F0)
        elif get_border_condition(i, j, a, b, c, d, e, f):
            B[num] = u0
            not_empty_B[index] = u0
        else:
            B[num] = func(i, j, f0, betta, x0, z0) * dx ** 2 / (-4 * k)
            not_empty_B[index] = func(i, j, f0, betta, x0, z0) * dx ** 2 / (-4 * k)

        print(f"num={num}, index={index} [{i}, {j}]: {B[num]} and {B[index]}")

    print(f'Матрица значений:\n{B}')
    print(f'Матрица без нулевых значений:\n{not_empty_B}')
    print()
    index = -1

    for num in range(n):
        i = num // a
        j = num % a

        if c < j < d and e < i < f:
            continue
        else:
            index += 1

        print(f'process num={num} [{i}, {j}]')

        A[num, num] = 1
        not_empty_A[index, num] = 1

        if get_border_condition(i, j, a, b, c, d, e, f):
            continue

        left = get_correct_number(i, j - 1, a, b, c, d, e, f)
        right = get_correct_number(i, j + 1, a, b, c, d, e, f)
        top = get_correct_number(i - 1, j, a, b, c, d, e, f)
        bottom = get_correct_number(i + 1, j, a, b, c, d, e, f)

        if left is not None:
            A[num, left] = -1 / 4
            not_empty_A[index, left] = -1 / 4
        if right is not None:
            A[num, right] = -1 / 4
            not_empty_A[index, right] = -1 / 4
        if top is not None:
            A[num, top] = -1 / 4
            not_empty_A[index, top] = -1 / 4
        if bottom is not None:
            A[num, bottom] = -1 / 4
            not_empty_A[index, bottom] = -1 / 4

    print()
    print(f'Матрица коэффициентов:\n{A}')
    print(f'Матрица коэффициентов без нулевых строк:\n{not_empty_A}')
    not_empty_A = np.delete(not_empty_A, get_empty_columns(a, c, d, e, f), 1)
    print(f'Матрица коэффициентов без нулевых строк:\n{not_empty_A}')

    u = linalg.solve(not_empty_A, not_empty_B).T
    print('\nRESULT\n')
    u_index = 0
    total_u = zeros([b, a])
    for num in range(n):
        i = num // a
        j = num % a

        if c < j < d and e < i < f:
            continue
        else:
            total_u[i, j] = u[0][u_index]
            u_index += 1

    print(f'Значения функции U:\n{total_u}')


if __name__ == '__main__':
    main()
