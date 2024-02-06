import random
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


def get_probabilistic_value(
        i: int, j: int, a: int, b: int, c: int, d: int, e: int, f: int,
        u0: int, f0: float, betta: float, x0: int, z0: int, dx: int, k: float, F0: int,
) -> float:
    if j == 0:
        value = func(i, j, f0, betta, x0, z0) * dx ** 2 / (4 * F0)
        print(f'[{i}, {j}] is left border. This value will be {value}')
        return value
    elif get_border_condition(i, j, a, b, c, d, e, f):
        print(f'[{i}, {j}] is border. This value will be {u0}')
        return u0
    else:
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
        print(f'Choice for [{i}, {j}] is {choice}. New [i, j] = [{new_i}, {new_j}]')
        return (
                func(i, j, f0, betta, x0, z0) * dx ** 2 / (-4 * k)
                +
                get_probabilistic_value(new_i, new_j, a, b, c, d, e, f, u0, f0, betta, x0, z0, dx, k, F0)
        )


def main() -> None:
    # const
    u0 = 300
    F0 = 30

    # user input

    a = int(input('Введите длину внешней границы по оси x (a) (по умолчанию 5): ') or 5)
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

    N = int(input('Введите количество подсчитывания цепочки случайной величины (по умолчанию 100): ') or 100)

    dx = 1

    probabilistic_values = zeros([b, a])
    for j in range(a):
        for i in range(b):
            if c < j < d and e < i < f:
                continue
            else:
                count = 0
                sum_probabilistic_values = 0
                while count < N:
                    sum_probabilistic_values += get_probabilistic_value(
                        i, j, a, b, c, d, e, f, u0, f0, betta, x0, z0, dx, k, F0
                    )
                    count += 1
                probabilistic_values[i, j] = sum_probabilistic_values / N

    print(f'Значения функции U:\n{probabilistic_values}')


if __name__ == '__main__':
    main()
