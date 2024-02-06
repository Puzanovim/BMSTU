import itertools

import numpy as np
from scipy import spatial

import time
import matplotlib.pyplot as plt
import pandas as pd


class ACO:
    def __init__(self, func, num_cities, num_ants, num_iters, distance_matrix, alpha=1, beta=0.5, rho=0.1):
        self.func_count_distance_route = func
        self.num_cities = num_cities
        self.num_ants = num_ants
        self.num_iters = num_iters
        self.alpha = alpha  # коэффициент важности феромонов в выборе пути
        self.beta = beta  # коэффициент значимости расстояния
        self.rho = rho  # скорость испарения феромонов
        self.distance_matrix = distance_matrix

        # матрица вероятностей
        self.prob_matrix_distance = 1 / (distance_matrix + 1e-10 * np.eye(num_cities, num_cities))

        self.pheromones = np.ones((num_cities, num_cities))
        self.ants_to_route = np.zeros((num_ants, num_cities)).astype(int)

        # фиксирование лучших поколений
        self.generation_best_routes = []
        self.generation_best_sum_routes = []
        self.best_history_routes = self.generation_best_routes
        self.best_history_sum_routes = self.generation_best_sum_routes

    def start(self):
        for i in range(self.num_iters):
            # вероятность перехода без нормализации
            prob_matrix = (self.pheromones ** self.alpha) + 1 / (self.prob_matrix_distance ** self.beta)
            # запускаем каждого муравья
            for num_ant in range(self.num_ants):
                # точка начала пути
                self.ants_to_route[num_ant, 0] = 0
                # цикл по количеству городов, которое нужно посетить
                for city in range(self.num_cities - 1):
                    # записываем пройденные города в табу лист
                    taboo_set = set(self.ants_to_route[num_ant, :city + 1])
                    # создаем список не посещенных городов
                    allow_list = list(set(range(self.num_cities)) - taboo_set)

                    # вероятность перехода из текущего города в разрешенные
                    prob = prob_matrix[self.ants_to_route[num_ant, city], allow_list]
                    prob = prob / prob.sum() # нормализация вероятности
                    next_point = np.random.choice(allow_list, size=1, p=prob)[0]
                    self.ants_to_route[num_ant, city + 1] = next_point

            # рассчет расстояний, пройденных муравьями путей
            sum_routes = np.array([self.func_count_distance_route(ant_route, self.distance_matrix) for ant_route in self.ants_to_route])

            # фиксация лучшего решения
            index_best = sum_routes.argmin()
            best_route, best_sum_route = self.ants_to_route[index_best, :].copy(), sum_routes[index_best].copy()
            self.generation_best_routes.append(best_route)
            self.generation_best_sum_routes.append(best_sum_route)

            # вычисление изменения феромона
            delta_tau = np.zeros((self.num_cities, self.num_cities))

            for num_ant in range(self.num_ants):
                for city in range(self.num_cities - 1):

                    # муравьи переходят из города city1 в город city2
                    city1 = self.ants_to_route[num_ant, city]
                    city2 = self.ants_to_route[num_ant, city + 1]
                    delta_tau[city1, city2] += 1 / sum_routes[num_ant]

                # переход из последнего города в первый
                city1 = self.ants_to_route[num_ant, self.num_cities - 1]
                city2 = self.ants_to_route[num_ant, 0]
                delta_tau[city1, city2] += 1 / sum_routes[num_ant]

            self.pheromones = (1 - self.rho) * self.pheromones + delta_tau

        best_generation_index = np.array(self.generation_best_sum_routes).argmin()
        best_route = self.generation_best_routes[best_generation_index]
        best_sum_route = self.generation_best_sum_routes[best_generation_index]

        return best_route, best_sum_route


def calculate_distance(route, distance_matrix):
    num_cities = route.shape[0]
    return sum([
        distance_matrix[route[city], route[(city + 1) % num_cities]]
        for city in range(num_cities)
    ])



def classic_alg(num_cities, distance_matrix):
    res = list(set(itertools.permutations(list(range(num_cities)))))
    sums = {}
    for r in res:
        r_sum = 0
        for i in range(len(r) - 1):
            r_sum += distance_matrix[r[i], r[i+1]]
        r_sum += distance_matrix[r[-1], r[0]]
        sums[r] = r_sum
    min_sum = 10000000
    min_r = []
    for k, v in sums.items():
        if v < min_sum:
            min_sum = v
            min_r = k

    return min_sum, min_r



def ant_alg(aco):
    best_route, best_sum_route = aco.start()
    return best_route, best_sum_route


def main():
    num_cities = 10
    num_ants = 40
    num_iters = 30

    print(f'Num cities: {num_cities}')
    # генерируем координаты городов
    cities_coordinates = np.random.rand(num_cities, 2)

    # вычисляем матрицу расстояний между городами
    distance_matrix = spatial.distance.cdist(cities_coordinates, cities_coordinates, metric='euclidean')

    start_time = time.monotonic()
    min_sum, min_r = classic_alg(num_cities, distance_matrix)
    print("time of execution Classic: %s seconds" % round(abs(time.monotonic() - start_time), 3))
    print(min_r, round(min_sum, 3))

    # создание объекта алгоритма муравьиной колонии
    aco = ACO(
        func=calculate_distance,
        num_cities=num_cities,
        num_ants=num_ants,
        num_iters=num_iters,
        distance_matrix=distance_matrix
    )

    start_time = time.monotonic()
    best_route, best_sum_route = ant_alg(aco)
    print("time of execution Ants: %s seconds" % round(abs(time.monotonic() - start_time), 3))
    print(best_route, round(best_sum_route, 3))


    # Вывод результатов на экран
    fig, ax = plt.subplots(1, 2)
    best_points = np.concatenate([best_route, [best_route[0]]])
    best_points_coordinate = cities_coordinates[best_points, :]

    for index in range(0, len(best_points)):
        ax[0].annotate(best_points[index], (best_points_coordinate[index, 0], best_points_coordinate[index, 1]))

    ax[0].plot(best_points_coordinate[:, 0], best_points_coordinate[:, 1], 'o-r')
    pd.DataFrame(aco.best_history_sum_routes).cummin().plot(
        ax=ax[1], xlabel='Номер итерации', ylabel='Минимальная сумма пути',
        title='Минимальная сумма пути на каждой итерации', legend=False
    )

    plt.rcParams['figure.figsize'] = [30, 15]
    plt.show()




if __name__ == '__main__':
    main()


