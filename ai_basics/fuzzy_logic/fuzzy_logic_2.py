import math
from typing import Tuple, Dict, List

from fuzzy_states import distance_states_to_fuzzifying, \
    a_states_to_fuzzifying, diff_a_states, DiffAccelerationStates, center_state


class SelfDriver:
    def __init__(self, benchmark_distance: float) -> None:
        self._benchmark_distance: float = benchmark_distance

        self._last_distances: Tuple[float, float] = (0, 0)
        self._coordinates: Tuple[float, float] = (0, 0)
        self._velocity: Tuple[float, float] = (0, 0)
        self._accelerations: Tuple[float, float] = (0, 0)

        self._states: Dict[DiffAccelerationStates, List[float]] = {}

    def _get_distance_to_leader(self, coordinates: Tuple[float, float]) -> float:
        x2, y2 = coordinates
        x1, y1 = self._coordinates
        return math.sqrt(((x2 - x1) ** 2 + (y2 - y1) ** 2))

    def _fuzzy_control(self, distance: float, acceleration: float) -> float:
        for state in list(DiffAccelerationStates):
            self._states[state] = []

        # fuzzifying process
        for distance_state, distance_fuzzifying in distance_states_to_fuzzifying.items():
            for acceleration_state, acceleration_fuzzifying in a_states_to_fuzzifying.items():
                if d := distance_fuzzifying(distance):
                    if a := acceleration_fuzzifying(acceleration):
                        diff_a_state = diff_a_states[(distance_state, acceleration_state)]
                        self._states[diff_a_state].append(min(d, a))

        max_states: Dict[DiffAccelerationStates, float] = {}
        for state, values in self._states.items():
            if not len(values):
                continue
            max_states[state] = max(values)

        self._states.clear()
        print(max_states)
        # defuzzifying process
        return sum([center_state(k) * v for k, v in max_states.items()]) / sum(max_states.values())

    def get_coordinates_of_point_n(self, x1, y1, x2, y2) -> Tuple[float, float]:
        """
        Вычисление координат точки на расстоянии необходимой дистанции от лидера на прямой автопилот - лидер
        :param x1: координата x автопилота
        :param y1: координата y автопилота
        :param x2: координата x лидера
        :param y2: координата y лидера
        :return:
        """
        dx = x1 - x2
        dy = y1 - y2
        try:
            b2 = (self._benchmark_distance ** 2) * (dy ** 2) / ((dx ** 2) + (dy ** 2))
        except ZeroDivisionError:
            b2 = 0
        b = math.sqrt(b2)
        try:
            a = b * dx / dy
        except ZeroDivisionError:
            a = 0

        a = abs(a)

        if x2 > x1:
            xn = x2 - a
        else:
            xn = x2 + a

        if y2 > y1:
            yn = y2 - b
        else:
            yn = y2 + b

        return round(xn, 2), round(yn, 2)

    def _update_self_driver_position(self, distances: Tuple[float, float]) -> None:
        """
        Вычисляется новое ускорение, новые координаты автопилота, и новая итоговая скорость автопилота
        :param diff_of_distance:
        :param coordinates:
        :return:
        """
        coordinates = []
        velocities = []
        accelerations = []

        for distance, acceleration, coordinate, v0, last_distance in zip(
                distances, self._accelerations, self._coordinates, self._velocity, self._last_distances
        ):
            diff_distance = distance - coordinate
            distance_acceleration = distance - last_distance

            acceleration_diff = self._fuzzy_control(diff_distance, distance_acceleration)
            print(f'INPUT DATA: {distance}, {coordinate} = {diff_distance}, da={distance_acceleration}, a={acceleration}, v={v0}. A Diff: {acceleration_diff}')

            new_acceleration = acceleration + acceleration_diff
            new_coordinate = coordinate + v0 + 1/2 * new_acceleration
            new_v = v0 + new_acceleration

            accelerations.append(round(new_acceleration, 2))
            coordinates.append(round(new_coordinate, 2))
            velocities.append(round(new_v, 2))


        self._last_distances = distances
        self._coordinates = tuple(coordinates)
        self._velocity = tuple(velocities)
        self._accelerations = tuple(accelerations)

        print(f'New position {self._coordinates} v={self._velocity} a={self._accelerations}, last={self._last_distances}')

    def keep_distance(self, coordinates: Tuple[float, float]) -> float:
        # вычисляем расстояние до лидера (скаляр)
        distance: float = self._get_distance_to_leader(coordinates)
        # вычисляем ошибку
        error: float = self._benchmark_distance - distance

        # вычисляем точку, на прямой автопилот-лидер, где должен был бы находиться автопилот, чтобы сохранить дистанцию
        distances: Tuple[float, float] = self.get_coordinates_of_point_n(
            x1=self._coordinates[0],
            y1=self._coordinates[1],
            x2=coordinates[0],
            y2=coordinates[1],
        )

        print(
            f'\n'
            f'Leader coordinates: {coordinates} '
            f'Self coordinates: {self._coordinates} '
            f'distance to leader: {distance} '
            f'error: {error} '
            f'target distance: {distances} '
            f'last distance: {self._last_distances}'
        )

        # обновляем ускорение, координаты и скорость автопилота
        self._update_self_driver_position(distances)
        # возвращаем квадратичную ошибку
        return error ** 2


def main():
    benchmark_distance = 2

    test_coordinates = [(0, i * 4) for i in range(1, 100)]
    # test_coordinates = [(0, 4),(0, 8),(0,11),(0,16),(0,20)]
    # test_coordinates = [(0, 4),(0, 8),(0,11),(0,16),(0,20),(0,25),(0,31),(0,38),(4,40),(10,38),(12,35)]
    average_error = 0.

    self_driver = SelfDriver(benchmark_distance)

    for i, coordinate in enumerate(test_coordinates):
        print(f'\nITERATION: {i}')
        average_error += self_driver.keep_distance(coordinate)

    total_error = average_error
    average_error /= len(test_coordinates)
    print(f'TOTAL ERROR: {total_error}, AVERAGE ERROR: {average_error}')



if __name__ == '__main__':
    main()