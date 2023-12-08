from pydantic import BaseModel


class Rule(BaseModel):
    number: int
    input: list[int]
    output: int


class Graph:
    def __init__(self, rules: list[Rule]):
        self.rules = rules

        self.closed_vertices = []       # список закрытых вершин
        self.closed_rules = []          # список закрытых правил

        self.opened_vertices = []       # список открытых вершин
        self.opened_rules = []          # список открытых правил

        self.not_closed_vertices = []   # список недоказуемых вершин
        self.not_closed_rules = []      # список недоказуемых правил

        self.found_solution = False     # флаг решения

    def print_info(self, title: str):
        print()
        print(title)
        print(f"Список закрытых вершин: ", self.closed_vertices)
        print(f"Список закрытых правил: ", self.closed_rules)

        print(f"Список открытых вершин: ", self.opened_vertices)
        print(f"Список открытых правил: ", self.opened_rules)

        print(f"Список недоказуемых вершин: ", self.not_closed_vertices)
        print(f"Список недоказуемых правил: ", self.not_closed_rules)
        print()

    def search_from_target(self, vertices, target):
        self.opened_vertices.append(target)     # Добавляем целевую вершину в список открытых вершин (в голову стека)
        self.closed_vertices = vertices.copy()  # Заносим входные данные (вершины) в список доказанных вершин

        sub_target = self.opened_vertices[-1]  # берем вершину из головы стека

        # Пока не найдено решение И не закончились открытые вершины
        while not self.found_solution and (len(self.opened_vertices) != 0):
            self.print_info(f'Текущая подцель {sub_target}')

            end_vertex = True       # инициализируем флаг конечной вершины (по умолчанию True, опустим, если есть правила)
            closed_rule = True      # инициализируем флаг доказанного правила (по умолчанию True, опустим, если есть недоказанная вершина)
            next_current = False    # инициализируем флаг перехода к новой переменной

            # Проходим по базе правил
            for rule in self.rules:
                # Если выходная вершина правила не является подцелью ИЛИ правило в списке недоказуемых,
                # то пропускаем данное правило
                if rule.output != sub_target or rule.number in self.not_closed_rules:
                    continue

                print(f'Номер текущего правила {rule.number}')
                end_vertex = False  # опускаем флаг конечной вершины

                # Проходим по входным вершинам текущего правила
                for node in rule.input:
                    print(f'Вершина {node}', end=' ')

                    # Если номер текущего правила не в списке открытых и не в недоказуемых,
                    # то добавляем правило в список открытых
                    if (
                        rule.number not in self.opened_rules
                        and
                        rule.number not in self.not_closed_rules
                    ):
                        self.opened_rules.append(rule.number)

                    # Если входная вершина в списке запрещенных,
                    # то удаляем текущее правило из списка открытых и добавляем в недоказуемые правила
                    if node in self.not_closed_vertices:
                        self.not_closed_rules.append(self.opened_rules.pop())

                    # Если вершина в списке доказанных
                    if node in self.closed_vertices:
                        print('- вершина в списке доказанных')
                    else:
                        if node in self.not_closed_vertices:
                            print('- вершина в списке запрещенных')
                        else:
                            print('- вершина не в списке доказанных')
                        closed_rule = False  # опускаем флаг доказанного правила

                        # Если входная вершина текущего правила не в списке открытых И не в списке недоказуемых
                        if node not in self.opened_vertices and node not in self.not_closed_vertices:
                            self.opened_vertices.append(node)  # добавляем входную вершину в список открытых вершин

                        sub_target = self.opened_vertices[-1]  # берем следующую подцель
                        next_current = True                 # поднимаем флаг перехода к новой подцели
                        break

                # Если правило доказано
                if closed_rule:
                    print('Все вершины текущего правила доказаны. Правило доказано')

                    # добавляем правило и его выходную вершину в список доказанных
                    if len(self.opened_vertices) != 0:
                        self.closed_vertices.append(self.opened_vertices.pop())
                        if len(self.opened_rules) != 0:
                            self.closed_rules.append(self.opened_rules.pop())

                    self.print_info('Списки после добавления доказанного правила и вершин в список доказанных')

                    # Если список открытых вершин не пуст,
                    # то берем следующую подцель
                    if len(self.opened_vertices) != 0 and len(self.opened_rules) != 0:
                        sub_target = self.opened_vertices[-1]   # берем следующую подцель
                        next_current = True                     # поднимаем флаг перехода к новой подцели
                    else:
                        # Проверяем есть ли целевая вершина в списке доказанных
                        if target in self.closed_vertices:
                            print('Целевая вершина в списке доказанных')
                            self.found_solution = True  # поднимаем флаг решения
                            break
                        else:
                            print("Список открытых вершин пуст")
                            break

                if next_current:
                    break

            # Если это конечная вершина
            if end_vertex:
                print('Это конечная вершина, у нее нет потомков, возвращаемся к предыдущей вершине')

                # Добавляем вершину и правило в запрещенные
                if len(self.opened_vertices) != 0:
                    # Добавляем эту вершину в список не доказанных
                    self.not_closed_vertices.append(self.opened_vertices.pop())

                    if len(self.opened_rules) != 0:
                        # Добавляем номер правила в список не доказанных
                        self.not_closed_rules.append(self.opened_rules.pop())

                self.print_info('Бектрекинг')

                if len(self.opened_vertices) != 0:
                    sub_target = self.opened_vertices[-1]  # берем следующую подцель
                else:
                    print("Список открытых вершин пуст")

        if self.found_solution:
            print('Путь найден')
        else:
            print('Путь не найден')

        return self.found_solution, self.closed_vertices, self.closed_rules


def main():
    rules = [
        Rule(number=104,    input=[8, 31],         output=3),
        Rule(number=101,    input=[1, 2],          output=3),
        Rule(number=103,    input=[5, 6],          output=4),
        Rule(number=102,    input=[3, 2, 4],       output=7),
        Rule(number=105,    input=[7, 9],          output=14),
        Rule(number=106,    input=[4, 18, 11],     output=9),
        Rule(number=107,    input=[12, 13],        output=11),
        Rule(number=114,    input=[22, 23],        output=12),
        Rule(number=111,    input=[10, 11],        output=9),
        Rule(number=110,    input=[9, 21],         output=14),
        Rule(number=113,    input=[12, 20],        output=10),
        Rule(number=108,    input=[21, 15],        output=33),
        Rule(number=112,    input=[10, 19],        output=21),
        Rule(number=115,    input=[19, 41],        output=21),
        Rule(number=109,    input=[13, 20, 41],    output=19)
    ]

    graph = Graph(rules)
    solution, closed_vertices, closed_rules = graph.search_from_target([1, 2, 13, 20, 22, 23, 41], 14)
    # solution, closed_vertices, closed_rules = graph.search_from_target([5, 6, 18, 12, 13, 21], 14)
    print(
        f'\n{"Путь найден" if solution else "Путь не найден"}\n'
        f'Пройденные вершины:\t\t{closed_vertices}\n'
        f'Примененные правила:\t{closed_rules}\n'
    )


if __name__ == "__main__":
    main()
