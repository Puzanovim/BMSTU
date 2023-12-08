from pydantic import BaseModel


class Rule(BaseModel):
    number: int
    input: list[int]
    output: int


class Graph:
    def __init__(self, rules: list[Rule]):
        self.rules = rules

        # Списки доказанных вершин и правил
        self.closed_vertices = []
        self.closed_rules = []

        # Списки открытых вершин и правил
        self.opened_vertices = []
        self.opened_rules = []

        # Списки недоказуемых вершин и правил
        self.not_closed_vertices = []
        self.not_closed_rules = []

        self.found_solution = False  # флаг решения

    def print_state(self, title: str) -> None:
        print(title)
        print(f"Список закрытых вершин: ", self.closed_vertices)
        print(f"Список закрытых правил: ", self.closed_rules)

        print(f"Список открытых вершин: ", self.opened_vertices)
        print(f"Список открытых правил: ", self.opened_rules)

        print(f"Список не доказанных вершин: ", self.not_closed_vertices)
        print(f"Список не доказанных правил: ", self.not_closed_rules)
        print()

    def search_from_target(self, vertices: list[int], destination: int):
        self.opened_vertices.insert(0, destination)  # добавляем целевую вершину в стек открытых вершин
        self.closed_vertices = vertices.copy()  # входные данные помечаем доказанными вершинами

        # Достаем вершину из открытых (используется стек)
        current_vertex = self.opened_vertices[0]

        # Пока не найдено решение или не закончились открытые вершины
        while not self.found_solution and len(self.opened_vertices) != 0:
            self.print_state(f'Текущая подцель {current_vertex}')

            # инициируем флаги конечной вершины и доказанного правила
            end_vertex = True
            rule_is_closed = True

            # Проходим по базе правил
            for rule in self.rules:

                # Если выходная вершина правила не является подцелью или правило в списке закрытых,
                # то пропускаем данное правило
                if rule.output_node != current_vertex and rule.number in self.not_closed_rules:
                    continue

                print('Номер текущего правила ', rule.number)
                end_vertex = False  # отмечаем, что вершина не конечная

                # Смотрим входные вершины для текущего правила
                for node in rule.input_nodes:
                    print(f'Вершина {node}')

                    # Если номер текущего правила не в списке открытых и не в недоказуемых,
                    # то добавляем в список открытых
                    if (
                        rule.number not in self.opened_rules
                        and rule.number not in self.not_closed_rules
                    ):
                        self.opened_rules.insert(0, rule.number)

                    # Если входная вершина в списке недоказуемых,
                    # то удаляем текущее правило из списка открытых и добавляем в недоказуемые правила
                    if node in self.not_closed_vertices:
                        self.not_closed_rules.append(self.opened_rules.pop(0))

                    if node not in self.closed_vertices:
                        print('Вершина не в списке доказанных!')
                    rule_is_closed = False  # правило не доказано

                    # Если вершина текущего правила не в списке открытых, добавляем вершину в список открытых
                    if node not in self.opened_vertices and node not in self.not_closed_vertices:
                        self.opened_vertices.insert(0, node)

                        # Меняем подцель
                        current_vertex = self.opened_vertices[0]
                        # Переходим к раскрытию новой подцели
                        break

                    print('Вершина в списке доказанных!')

                # Если правило доказано
                if rule_is_closed:
                    print('Все вершины текущего правила доказаны! Правило доказано!')
                    if len(self.opened_vertices) != 0:

                        # Добавляем в список доказанных
                        self.closed_vertices.append(self.opened_vertices.pop(0))
                        if len(self.opened_rules) != 0:
                            self.closed_rules.append(self.opened_rules.pop(0))

                    self.print_state('Списки после добавления доказанного правила и вершин в список доказанных')

                    # Меняем подцель если список открытых вершин не пуст
                    if len(self.opened_vertices) != 0 and len(self.opened_rules) != 0:
                        current_vertex = self.opened_vertices[0]

                    # Список открытых вершин пуст
                    else:
                        # Проверяем есть ли целевая вершина в списке доказанных
                        if destination in self.closed_vertices:
                            print('Целевая вершина в спсике доказанных!')
                            self.found_solution = True  # меняем флаг решения
                            break

                        else:
                            print("Список открытых вершин пуст!")
                            break

                    print('\nТекущая подцель', current_vertex)

            # Если это конечная вершина (нет потомков)
            if end_vertex:
                print('Это конечная вершина, у нее нет потомков, возвращаемся к предыдущей вершине')

                if len(self.opened_vertices) != 0:
                    # Добавляем эту вершину в список не доказанных
                    self.not_closed_vertices.append(self.opened_vertices.pop(0))

                    if len(self.opened_rules) != 0:
                        # Добавляем номер правила в список не доказанных
                        self.not_closed_rules.append(self.opened_rules.pop(0))

                self.print_state('После бектрекинга')

                if len(self.opened_vertices) != 0:
                    # Меняем подцель
                    current_vertex = self.opened_vertices[0]
                else:
                    print("Список открытых вершин пуст")

        if self.found_solution:
            print('\nВершина найдена!')
            return self.found_solution, self.closed_vertices, self.closed_rules
        else:
            if len(self.opened_vertices) == 0:
                print('\nВершина НЕ найдена! Список открытых вершин пуст!')
                return self.found_solution, [], []


def main():
    rules = [
        Rule(104, [8, 31], 3),
        Rule(101, [1, 2], 3),
        Rule(103, [5, 6], 4),
        Rule(102, [3, 2, 4], 7),
        Rule(105, [7, 9], 14),
        Rule(106, [4, 18, 11], 9),
        Rule(107, [12, 13], 11),
        Rule(114, [22, 23], 12),
        Rule(111, [10, 11], 9),
        Rule(110, [9, 21], 14),
        Rule(113, [12, 20], 10),
        Rule(108, [21, 15], 33),
        Rule(112, [10, 19], 21),
        Rule(115, [19, 41], 21),
        Rule(109, [13, 20, 41], 19)
    ]

    graph = Graph(rules)
    # solution, closed_vertices, closed_rules = graph.search_from_target([5, 6, 2, 1, 18, 22, 23, 13], 14)
    solution, closed_vertices, closed_rules = graph.search_from_target([5, 6, 18, 12, 13, 21], 14)
    print(
        f'\n{"Путь найден" if solution else "Путь не найден"}\n'
        f'Пройденные вершины:\t{closed_vertices}\n'
        f'Примененные правила:\t{closed_rules}\n'
    )


if __name__ == "__main__":
    main()
