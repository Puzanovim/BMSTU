from pydantic import BaseModel


class Rule(BaseModel):
    number: int
    input: list[int]
    output: int


class Graph:
    def __init__(self, rules: list[Rule]):
        self.rules = rules

    def search_from_input(self, vertices: list[int], target: int):
        # проверяем есть ли целевая вершина во входных данных (если да, то правило считается доказанным (закрытым)
        if target in vertices:
            return True, [], []

        found_solution = False              # инициализация флага решения
        closed_vertices = vertices.copy()   # списка закрытых вершин
        closed_rules = []                   # списка закрытых правил
        found_rules = True                  # инициализация флага найденных правил

        # пока не найдено решение И флаг найденных правил поднят
        while not found_solution and found_rules:
            found_rules = False  # опускаем флаг найденных правил

            # проходим по базе правил
            for rule in self.rules:
                # если правило в списке закрытых правил ИЛИ выходная вершина в списке закрытых вершин,
                # то пропускаем, переходим к следующему правилу
                if rule.number in closed_rules or rule.output in closed_vertices:
                    continue

                found_rules = True  # поднимаем флаг найденных правил

                # флаг того, что все входные вершины правила в списке закрытых
                input_vertices_closed = all(vertex in closed_vertices for vertex in rule.input)

                # если флаг закрытых входных вершин поднят, то отмечаем правило закрытым
                if input_vertices_closed:
                    # если целевая вершина в списке выходных вершин, то ставим флаг решения
                    if target == rule.output:
                        found_solution = True
                    else:
                        closed_vertices.append(rule.output)  # добавляем выходную вершину в список закрытых

                    closed_rules.append(rule.number)  # добавляем правило в список закрытых правил
                    print(f"Список закрытых вершин: ", closed_vertices)
                    print(f"Список закрытых правил: ", closed_rules)

        if found_solution:
            return found_solution, closed_vertices, closed_rules
        else:
            return found_solution, [], []


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
    solution, closed_vertices, closed_rules = graph.search_from_input(
        [1, 2, 13, 20, 22, 23, 41], 14
    )
    print(
        f'\n{"Путь найден" if solution else "Путь не найден"}\n'
        f'Пройденные вершины:\t{closed_vertices}\n'
        f'Примененные правила:\t{closed_rules}\n'
    )


if __name__ == "__main__":
    main()
