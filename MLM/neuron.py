class Neuron:
    def __init__(self, inputs_count):
        self.weights = 2 * np.random.random(inputs_count) - 1
        self.delta = 0
        self.output = 0

    def _weights_to_input(self, inputs):
        return np.dot(self.weights[:-1], inputs) + self.weights[-1]

    def get_output(self, inputs, activation_func):
        return activation_func(self._weights_to_input(inputs), False)

    def update_weights(self, inputs, alpha):
        for j in range(len(inputs)):
            self.weights[j] += alpha * self.delta * inputs[j]
        self.weights[-1] += alpha * self.delta

class Perceptron:
    def __init__(self, layers_size: Tuple):
        self.layers = []
        previous_layer_size = layers_size[0]
        for layer_size in layers_size:
            self.layers.append(
                [Neuron(previous_layer_size + 1) for _ in range(layer_size)]
            )
            previous_layer_size = layer_size

    def _get_output(self, input_data, activation_func):
        if len(input_data) != len(self.layers[0]):
            raise Exception

        layer_input = input_data

        for layer in self.layers[1:]:
            layer_output = []
            for neuron in layer:
                layer_output.append(neuron.get_output(layer_input, activation_func))
            layer_input = layer_output

        return layer_input

    def _calculate_error_neurons(self, expected, activation_func):
        # Проходим по сети в обратную сторону
        for i in reversed(range(len(self.layers))):
            layer = self.layers[i]
            errors = []

            if i != len(self.layers) - 1:
                for j in range(len(layer)):
                    error = 0.0
                    for neuron in self.layers[i + 1]:
                        error += (neuron.weights[j] * neuron.delta)
                    errors.append(error)
            else:
                for j in range(len(layer)):
                    neuron = layer[j]
                    errors.append(expected[j] - neuron.output)

            # Нормализация ошибки производной от функции активации
            for j in range(len(layer)):
                neuron = layer[j]
                neuron.delta = errors[j] * activation_func(neuron.output, True)

    def _update_neurons_weights(self, inputs, alpha):
        for i in range(len(self.layers)):
            if i == 0:
                layer_input = inputs
            else:
                layer_input = [neuron.output for neuron in self.layers[i - 1]]

            for neuron in self.layers[i]:
                neuron.update_weights(layer_input, alpha)

    def train(
        self, X_train, Y_train, X_test, Y_test, alpha, epochs, activation_func
    ):
        epochs_errors = []
        for epoch in range(epochs):
            train_error = 0
            test_error = 0

            for i in range(len(X_train)):
                outputs = self._get_output(X_train[i], activation_func)
                self._calculate_error_neurons(Y_train[i], activation_func)
                self._update_neurons_weights(X_train[i], alpha)

                # train_error += mean_squared_error(Y_train[i], outputs)
                train_error += math.sqrt(sum([(Y_train[i][j] - outputs[j]) ** 2 for j in range(len(Y_train[i]))]) / len(outputs))

            for i in range(len(X_test)):
                outputs = self._get_output(X_test[i], activation_func)
                # test_error += mean_squared_error(Y_test[i], outputs)
                train_error += math.sqrt(sum([(Y_test[i][j] - outputs[j]) ** 2 for j in range(len(Y_test[i]))]) / len(outputs))

            epochs_errors.append([train_error / len(X_train), test_error / len(X_test)])
        return epochs_errors

    def predict(self, input_data, activation_func):
        return self._get_output(input_data, activation_func)