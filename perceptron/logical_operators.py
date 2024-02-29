from perceptron import Neuron

AND = Neuron(b=-0.5, input_size=2, activation_function=lambda x: x, weight_init_function=lambda x: 1)
OR = Neuron(b=0.5, input_size=2, activation_function=lambda x: x, weight_init_function=lambda x: 1)


def operator_and(a: int, b: int) -> int:
    result = AND.get_output([a, b])
    return int(bool(int(result)))


def operator_or(a: int, b: int) -> int:
    result = OR.get_output([a, b])
    return int(bool(int(result)))


def main():
    for a in (0, 1):
        for b in (0, 1):
            print(f'{a} AND {b} = {operator_and(a, b)}')

    print()

    for a in (0, 1):
        for b in (0, 1):
            print(f'{a} OR {b} = {operator_or(a, b)}')


if __name__ == '__main__':
    main()
