from typing import Callable


class Neuron:
    def __init__(
        self,
        b: float,
        input_size: int,
        activation_function: Callable[[float], float],
        weight_init_function: Callable[[float], float]
    ) -> None:
        self.activation_function: Callable[[float], float] = activation_function
        self.weights: list[float] = [b]
        self.__init_weights(input_size, weight_init_function)

    def __init_weights(self, input_size: int, weight_init_function: Callable[[float], float]) -> None:
        for _ in range(input_size):
            weight_value = weight_init_function(_)
            self.weights.append(weight_value)

    def get_output(self, inputs: list[float]) -> float:
        output = self.weights[0]

        for input_value, weight in zip(inputs, self.weights[1:]):
            output += input_value * weight

        return self.activation_function(output)


class Perceptron:
    pass
