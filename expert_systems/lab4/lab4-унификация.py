from pydantic import BaseModel


class Term(BaseModel):
    variable: bool
    constant: bool


class Constant(Term, BaseModel):
    value: str | int
    variable: bool = False
    constant: bool = True

    def __str__(self):
        return self.value


class Variable(Term, BaseModel):
    name: str
    variable: bool = True
    constant: bool = False

    def __str__(self):
        return self.name


class Atom(BaseModel):
    name: str
    terms: list[Term]

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


def unification(p1: Atom, p2: Atom, prints=True) -> tuple[bool, Table]:
    if prints:
        print(f'Получены атомы:\n1) {p1}\n2) {p2}\n')

    table = Table()
    unification_flag: bool = True

    # Проверяем, равны ли имена p1,p2, если нет, то унификация не выполняется
    if p1.name != p2.name:
        if prints:
            print('Имена не совпадают')
        unification_flag = False
        return unification_flag, table

    # Проверяем, равна ли длина массивов термов атомов p1 и p2, если нет, то унификация не выполняется
    if len(p1.terms) != len(p2.terms):
        if prints:
            print('Длины массивов термов не совпадают')
        unification_flag = False
        return unification_flag, table

    t1: Term
    t2: Term
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
                table.links[t2.name].append(t1.name)

            # t1 есть в таблице, t2 нет в таблице подстановок
            elif t1_in_table and not t2_in_table:
                # связываем t2 c t1
                table.variables[t2.name] = table.variables[t1.name]
                table.links[t1.name].append(t2.name)
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
                return unification_flag, table

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
                for variable in table.links[t1.name]:
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
                return unification_flag, table

        # t1 константа, t2 переменная
        elif t1.constant and t2.variable:
            t1: Constant
            t2: Variable
            if prints:
                print(f't1 ({t1}) - константа, t2 ({t2}) - переменная')

            # Если переменной t2 нет в таблице подстановок или ее значение не определено
            if t2.name not in table.variables or table.variables[t2.name] is None:
                table.variables[t2.name] = t1.value  # присваиваем переменной t2 значение константы t1
                # обновляем связанные переменные
                for variable in table.links[t2.name]:
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
                return unification_flag, table

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
                return unification_flag, table

    if prints:
        print('\n-------- Функция унификации закончена -------\n')
    return unification_flag, table


def print_results(unification_flag, table):
    print()
    if unification_flag:
        print('Унификация выполнена')
    else:
        print('Унификация невозможна')

    print(table)
    print()


def unification_tests():
    v1 = Variable(name="x1")
    v2 = Variable(name="x2")
    c1 = Constant(value="A")
    c2 = Constant(value="B")

    variations = [
        # корректные
        (Atom(name="A", terms=[v1, c1, v1]), Atom(name="A", terms=[v2, v2, c1]), True),
        (Atom(name="A", terms=[c1, c2]), Atom(name="A", terms=[c1, c2]), True),
        # тест на название
        (Atom(name="A", terms=[c1, c2]), Atom(name="B", terms=[c1, c2]), False),
        # тесты на длину
        (Atom(name="A", terms=[c1, c2, v1]), Atom(name="A", terms=[c1, c2]), False),
        (Atom(name="A", terms=[c1, c2]), Atom(name="A", terms=[c1, c2, v1]), False),
        # тест на несовпадающие константы
        (Atom(name="A", terms=[c2, c1]), Atom(name="A", terms=[c1, c2]), False),
        (Atom(name="A", terms=[c2, c1]), Atom(name="A", terms=[c1, c2]), False),
    ]
    for i, (a1, a2, true_result) in enumerate(variations):
        result, _ = unification(a1, a2, prints=False)
        if result == true_result:
            print(f'Тест {i} пройден')
        else:
            print(f'Тест {i} провален')


def main(tests=False):
    if tests:
        unification_tests()
    else:
        v1 = Variable(name="x1")
        v2 = Variable(name="x2")
        c1 = Constant(value="A")
        c2 = Constant(value="B")

        a1 = Atom(name="A", terms=[v1, c1, v1])
        a2 = Atom(name="A", terms=[v2, v2, c1])

        res, table = unification(a1, a2)
        print_results(res, table)

        # a1 = Atom(name="A", terms=[v1, c1, v1])
        # a2 = Atom(name="A", terms=[v2, v2, c2])
        #
        # res, table = unification(a1, a2)
        # print_results(res, table)


if __name__ == "__main__":
    main()
