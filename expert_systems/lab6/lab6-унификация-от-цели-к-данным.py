import copy

from pydantic import BaseModel


class Term(BaseModel):
    variable: bool
    constant: bool


class Constant(Term, BaseModel):
    value: str | int
    variable: bool = False
    constant: bool = True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.value


class Variable(Term, BaseModel):
    name: str
    variable: bool = True
    constant: bool = False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name


class Atom(BaseModel):
    name: str
    terms: list[Term]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'{self.name} ({[str(x) for x in self.terms]})'


class Table(BaseModel):
    variables: dict = {}
    links: dict = {}
    const_links: dict = {}

    # Получение значение переменной
    def get_variable(self, variable: Variable):
        return self.variables[variable.name]

    def get_variable_links(self, variable: Variable):
        return self.links[self.variables[variable.name]]

    def __str__(self):
        return (
            f'Таблица подстановок: {self.variables}\n'
            f'Таблица связей переменных: {self.links.items()}\n'
            f'Таблица связей констант и переменных: '
            f'{[f"{variables}: {const}" for const, variables in self.const_links.items()]}'
        )


class Rule(BaseModel):
    input: list[Atom]
    output: Atom


def unification(table: Table, p1: Atom, p2: Atom, prints=False) -> bool:
    if prints:
        print(f'Получены атомы:\n1) {p1}\n2) {p2}\n')

    unification_flag: bool = True

    # Проверяем, равны ли имена p1,p2, если нет, то унификация не выполняется
    if p1.name != p2.name:
        if prints:
            print('Имена не совпадают')
        unification_flag = False
        return unification_flag

    # Проверяем, равна ли длина массивов термов атомов p1 и p2, если нет, то унификация не выполняется
    if len(p1.terms) != len(p2.terms):
        if prints:
            print('Длины массивов термов не совпадают')
        unification_flag = False
        return unification_flag

    t1: Term
    t2: Term
    original_table = copy.deepcopy(table)
    # Берем термы попарно из массивов термов атомов p1 и p2
    for i, (t1, t2) in enumerate(zip(p1.terms, p2.terms)):
        if prints:
            print(f'\n------ Пара термов №{i + 1} ---------')
        # t1 и t2 переменные
        if t1.variable and t2.variable:
            t1: Variable
            t2: Variable
            if prints:
                print(f't1 ({t1}) и t2 ({t2}) - переменные')

            # проверяем наличие термов в таблице подстановок
            t1_in_table = t1.name in table.variables
            t2_in_table = t2.name in table.variables
            if prints:
                print(f't1 {"есть" if t1_in_table else "нет"} в таблице подстановок')
                print(f't2 {"есть" if t2_in_table else "нет"} в таблице подстановок')

            # t1 и t2 нет в таблице подстановок
            if not t1_in_table and not t2_in_table:
                # связываем переменные
                table.links[t1.name] = [t2.name]
                table.links[t2.name] = [t1.name]
                table.variables[t1.name] = None
                table.variables[t2.name] = None

            # t1 нет в таблице, t2 есть в таблице подстановок
            elif not t1_in_table and t2_in_table:
                # связываем t1 c t2
                table.variables[t1.name] = table.variables[t2.name]
                table.links[t1.name] = [t2.name]
                try:
                    table.links[t2.name].append(t1.name)
                except KeyError:
                    table.links[t2.name] = [t1.name]

            # t1 есть в таблице, t2 нет в таблице подстановок
            elif t1_in_table and not t2_in_table:
                # связываем t2 c t1
                table.variables[t2.name] = table.variables[t1.name]
                try:
                    table.links[t1.name].append(t2.name)
                except KeyError:
                    table.links[t1.name] = [t2.name]
                table.links[t2.name] = [t1.name]

            # t1 и t2 есть в таблице подстановок
            elif t1_in_table and t2_in_table:
                table.links[t1.name].append(t2.name)
                table.links[t2.name].append(t1.name)

                if table.variables[t1.name] is None:
                    table.variables[t1.name] = table.variables[t2.name]
                elif table.variables[t2.name] is None:
                    table.variables[t2.name] = table.variables[t1.name]

                # если их значения различны, то унификация невозможна
                elif table.variables[t1.name] != table.variables[t2.name]:
                    unification_flag = False

            if prints:
                print(table)

            if not unification_flag:
                if prints:
                    print(
                        f"Переменные {t1} и {t2} отличаются: "
                        f"{table.get_variable(t1).value} != {table.get_variable(t2).value}"
                    )
                table.reset(original_table)
                return unification_flag

        # t1 переменная, t2 константа
        elif t1.variable and t2.constant:
            t1: Variable
            t2: Constant
            if prints:
                print(f't1 ({t1}) - переменная, t2 ({t2}) - константа')

            # Если переменной t1 нет в таблице подстановок или ее значение не определено
            if t1.name not in table.variables or table.variables[t1.name] is None:
                table.variables[t1.name] = t2.value  # присваиваем переменной t1 значение константы t2
                # обновляем связанные переменные
                for variable in table.links.get(t1.name, []):
                    if table.variables[variable] is not None and table.variables[variable] != t2.value:
                        unification_flag = False
                    else:
                        table.variables[variable] = t2.value

            # Переменная t1 есть в таблице подстановок
            else:
                # Если значение переменной t1 не равно значению константы t2, то унификация невозможна
                if table.variables[t1.name] != t2.value:
                    unification_flag = False

            # Добавляем связь константы t2 и переменной в таблицу связей
            if t2.value in table.const_links:
                table.const_links[t2.value].add(t1.name)
            else:
                table.const_links[t2.value] = {t1.name}

            if prints:
                print(table)

            if not unification_flag:
                if prints:
                    print(
                        f"Переменной {t1} уже соответствует другое значение константы: {table.get_variable(t1)} != {t2}"
                    )
                return unification_flag

        # t1 константа, t2 переменная
        elif t1.constant and t2.variable:
            t1: Constant
            t2: Variable
            if prints:
                print(f't1 ({t1}) - константа, t2 ({t2}) - переменная')

            if t2.name in table.variables and type(table.variables[t2.name]) is not str:
                if table.variables[t2.name].value != t1.value:
                    unification_flag = False

            # Если переменной t2 нет в таблице подстановок или ее значение не определено
            if t2.name not in table.variables or table.variables[t2.name] is None:
                table.variables[t2.name] = t1.value  # присваиваем переменной t2 значение константы t1
                # обновляем связанные переменные
                for variable in table.links.get(t2.name, []):
                    if table.variables[variable] is not None and table.variables[variable] != t1.value:
                        unification_flag = False
                    else:
                        table.variables[variable] = t1.value

            # Переменная t2 есть в таблице подстановок
            else:
                # Если значение переменной t2 не равно значению константы t1, то унификация невозможна
                if table.variables[t2.name] != t1.value:
                    unification_flag = False

            # Добавляем связь константы t2 и переменной в таблицу связей
            if t1.value in table.const_links:
                table.const_links[t1.value].add(t2.name)
            else:
                table.const_links[t1.value] = {t2.name}

            if prints:
                print(table)

            if not unification_flag:
                if prints:
                    print(
                        f"Переменной {t2} уже соответствует другое значение константы: {table.get_variable(t2)} != {t1}"
                    )
                return unification_flag

        # t1 и t2 константы
        elif t1.constant and t2.constant:
            t1: Constant
            t2: Constant
            if prints:
                print(f't1 ({t1.value}) и t2 ({t2.value}) - константы')
            if t1.value != t2.value:
                if prints:
                    print(f"Константы не равны: {t1.value} != {t2.value}")
                unification_flag = False
                return unification_flag

    if prints:
        print('\n-------- Функция унификации закончена -------\n')
    return unification_flag


class GraphSearcher:
    def __init__(self, rules: dict[int, Rule]):
        self.rules: dict[int, Rule] = rules
        self.table = None

        # Списки доказанных атомов и правил
        self.proven_atoms = list()
        self.proven_rules = list()

        # Списки открытых атомов и правил
        self.opened_atoms: list[Atom] = list()
        self.opened_rules: list[Rule] = list()
        self.used_atoms: list[Atom] = list()

        self.found = False  # флаг решения

    def search_from_target(self, input_atoms: list[Atom], target_atom: Atom):
        self.table = Table()

        # Добавляем целевой атом в список открытых атомов
        self.opened_atoms.insert(0, target_atom)
        # Заносим входные данные (атомы) в список доказанных атомов
        self.proven_atoms = list(input_atoms)

        # Подцель берем из головы И потомки записываются в голову, механизм СТЕКА
        current = self.opened_atoms[0]

        # Пока не найдено решение или не закончились атомы (потомки)
        while not self.found and len(self.opened_atoms) != 0:
            print('\nТекущая подцель', current)

            print(f"Список доказанных атомов: ", self.proven_atoms)
            print(f"Список доказанных правил: ", self.proven_rules)

            end_vertex = True  # Флаг все атомы доказаны
            prove_num = False  # Флаг доказанного номера правила
            check_unif = True  # Флаг нужно провести унификацию

            # Пока не конец базы правил
            for num, rule in self.rules.items():

                # Метод потомков, ищем правило в базе правил, выходной атом которого унфицируется с подцелью
                if check_unif:
                    if unification(self.table, rule.output, current):
                        print('Номер текущего правила: ', num)
                        print("Унификация выполнена:", rule.output, current)
                        print('Tаблица подстановок:', self.table.variables)
                        print('Таблица cвязей:', self.table.links)
                        check_unif = False
                        self.used_atoms.insert(0, current)

                if not check_unif:
                    # Смотрим входные атомы для текущего правила
                    for node in rule.input:
                        # Проверяем входят ли входные атомы в список закрытых атомов
                        if node not in self.used_atoms:
                            print('\nАтом', node)
                            end_vertex = False
                            prove_num = False

                            # Если номер текущего правила не в списке открытых, добавляем номер правила в список открытых
                            if num not in self.opened_rules:
                                self.opened_rules.insert(0, num)

                            # Пока не конец базы фактов
                            for proven in self.proven_atoms:
                                if unification(self.table, node, proven):
                                    print(f"Атом {node} унифицирует с фактом: {proven}")
                                    print('Tаблица подстановок:', self.table.variables)
                                    print('Таблица cвязей:', self.table.links)

                                    prove_num = True
                                    self.used_atoms.insert(0, node)
                                    break

                            if prove_num == False:
                                # Если атом текущего правила не в списке открытых, добавляем атом в список открытых
                                if node not in self.opened_atoms and node not in self.used_atoms:
                                    self.opened_atoms.insert(0, node)

                                # Меняем подцель, берем из головы
                                current = self.opened_atoms[0]
                                print('Атом становится новой подцелью')
                                check_unif = True
                                # Переходим к раскрытию новой подцели
                                break

                    # Если все атомы в списке фактов (закрытых) -> разметка
                    if prove_num:
                        # Распространение
                        for i in range(len(current.terms)):
                            current.terms[i] = self.table.variables[str(current.terms[i])]

                        if len(self.opened_atoms) != 0:
                            # Добавляем в список фактов (закрытых), убираем подцель из стека
                            self.proven_atoms.append(self.opened_atoms.pop(0))
                            if len(self.opened_rules) != 0:
                                self.proven_rules.append(self.opened_rules.pop(0))

                        print(f"Список доказанных атомов: ", self.proven_atoms)
                        print(f"Список доказанных правил: ", self.proven_rules)

                        # Выбираем следующий атом (подцель) из головы
                        if len(self.opened_atoms) != 0 and len(self.opened_rules) != 0:
                            current = self.opened_atoms[0]

                        # Список открытых атомов пуст
                        else:
                            # Проверяем есть ли целевой атом в списке доказанных
                            if target_atom in self.proven_atoms:
                                print('Целевой атом в спсике доказанных!')
                                self.found = True  # меняем флаг решения
                                break
                            else:
                                print("Список открытых атомов пуст!")
                                break
                        break

            # Если все атомы в правиле доказаны
            if end_vertex:
                print('Доказали все атомы в правиле, правило доказано!')

                if len(self.opened_atoms) != 0:
                    # Добавляем эту вершину в список доказанных
                    self.proven_atoms.append(self.opened_atoms.pop(0))

                    if len(self.opened_rules) != 0:
                        # Добавляем номер правила в список доказанных
                        self.proven_rules.append(self.opened_rules.pop(0))

                print('\nКонечные списки')
                print(f"Список доказанных атомов: ", self.proven_atoms)
                print(f"Список доказанных правил: ", self.proven_rules)

                if len(self.opened_atoms) != 0:
                    # Меняем подцель
                    current = self.opened_atoms[0]
                else:
                    self.found = True

        if self.found:
            print('\nРешение найдено!')
            return self.found, self.proven_atoms, self.proven_rules
        else:
            if len(self.opened_atoms) == 0:
                print('\nАтом НЕ найден! Список открытых атомов пуст!')
                return self.found


def main():
    c_N = Constant(value='N')
    c_M1 = Constant(value='M1')
    c_W = Constant(value='W')
    c_A1 = Constant(value='A1')

    v_x = Variable(name="x")
    v_y = Variable(name="y")
    v_z = Variable(name="z")
    v_x1 = Variable(name="x1")
    v_x2 = Variable(name="x2")
    v_x3 = Variable(name="x3")

    node1 = Atom(name="A", terms=[v_x])
    node2 = Atom(name="W", terms=[v_y])
    node3 = Atom(name="S", terms=[v_x, v_y, v_z])
    node4 = Atom(name="H", terms=[v_z])
    node5 = Atom(name="C", terms=[v_x])

    node6 = Atom(name="M", terms=[v_x1])
    node7 = Atom(name="O", terms=[c_N, v_x1])
    node8 = Atom(name="S", terms=[c_W, v_x1, c_N])

    node9 = Atom(name="M", terms=[v_x2])
    node10 = Atom(name="W", terms=[v_x2])

    node11 = Atom(name="E", terms=[v_x3, c_A1])
    node12 = Atom(name="H", terms=[v_x3])

    rules: dict[int, Rule] = dict()
    rules[1] = Rule(input=[node1, node3, node2, node4], output=node5)
    rules[2] = Rule(input=[node6, node7], output=node8)
    rules[3] = Rule(input=[node9], output=node10)
    rules[4] = Rule(input=[node11], output=node12)

    graph = GraphSearcher(rules)

    target = Atom(name="C", terms=[c_W])
    given = [
        Atom(name="O", terms=[c_N, c_M1]),
        Atom(name="M", terms=[c_M1]),
        Atom(name="A", terms=[c_W]),
        Atom(name="E", terms=[c_N, c_A1]),
    ]

    res, nodes, rules = graph.search_from_target(given, target)

    print("\nДоказанные атомы:", nodes)
    print("Доказанные правила:", rules)
    print("Таблица подстановок:", graph.table, sep='\n')


if __name__ == "__main__":
    main()
