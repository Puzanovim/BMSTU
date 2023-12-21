import copy
from pydantic import BaseModel


class Atom(BaseModel):
    name: str
    negative: bool = False

    def __str__(self):
        if self.negative:
            return f'!{self.name}'
        else:
            return self.name

    def __repr__(self):
        return self.__str__()


class Disjunct(BaseModel):
    atoms: list[Atom]

    def __str__(self):
        return '(' + ', '.join([str(atom) for atom in self.atoms]) + ')'

    def __repr__(self):
        return self.__str__()

    def tuple(self):
        return tuple([str(atom) for atom in self.atoms])


def disjunction(first_disjunct, second_disjunct):
    excluded = []
    result_atoms = []
    solution_flag = False

    for first_atom in first_disjunct.atoms:
        for second_atom in second_disjunct.atoms:
            if first_atom.name == second_atom.name:
                if first_atom.negative != second_atom.negative:
                    excluded.append(first_atom.name)
                    solution_flag = True

    if solution_flag:
        for atom in first_disjunct.atoms + second_disjunct.atoms:
            if atom.name not in excluded:
                result_atoms.append(atom)
                excluded.append(atom.name)

        return Disjunct(atoms=result_atoms)
    else:
        return None


def print_disjuncts(disjuncts: list[Disjunct], title: str) -> None:
    print('-------------------')
    print(title)
    for disjunct in disjuncts:
        print(disjunct)
    print('-------------------')


def resolution(disjuncts: list[Disjunct], target: Disjunct):
    print(f"Даны дизъюнкты (A): {disjuncts} и цель (F): {target}")
    solution_flag = False

    for atom in target.atoms:
        atom.negative = not atom.negative
        disjuncts.append(Disjunct(atoms=[atom]))

    print_disjuncts(disjuncts, 'После добавления цели к дизъюнктам')

    size = len(disjuncts)
    i = 0
    while i < size - 1:
        j = i + 1
        while j < size:
            new_disjunct = disjunction(disjuncts[i], disjuncts[j])
            if new_disjunct is not None:
                if len(new_disjunct.atoms):
                    if new_disjunct not in disjuncts:
                        disjuncts.append(new_disjunct)
                        size += 1
                        print(f"Найден новый дизъюнкт: {new_disjunct} из {disjuncts[i]} {disjuncts[j]}")
                        print_disjuncts(disjuncts, "Текущие дизъюнкты:")
                else:
                    print(f"Найден пустой дизъюнкт из {disjuncts[i]} {disjuncts[j]}")
                    disjuncts.append(new_disjunct)
                    print_disjuncts(disjuncts, "Текущие дизъюнкты:")
                    solution_flag = True
                    return solution_flag
            j += 1
        i += 1

    print('Пустой дизъюнкт не найден, F не является логическим выводом A')
    return solution_flag


def main():
    a = Atom(name='a')
    b = Atom(name='b')
    c = Atom(name='c')
    d = Atom(name='d')
    neg_a = Atom(name='a', negative=True)
    neg_b = Atom(name='b', negative=True)
    neg_c = Atom(name='c', negative=True)
    neg_d = Atom(name='d', negative=True)

    # abcd = Disjunct(atoms=[copy.deepcopy(a), copy.deepcopy(b), copy.deepcopy(c), copy.deepcopy(d)])
    # anbc = Disjunct(atoms=[copy.deepcopy(a), copy.deepcopy(neg_b), copy.deepcopy(c)])
    #
    # print(resolution([abcd, anbc], Disjunct(atoms=[a, d])))

    dis_1 = Disjunct(atoms=[copy.deepcopy(a), copy.deepcopy(b), copy.deepcopy(c), copy.deepcopy(d)])
    dis_2 = Disjunct(atoms=[copy.deepcopy(a), copy.deepcopy(neg_b), copy.deepcopy(neg_c)])

    print(resolution([dis_1, dis_2], Disjunct(atoms=[a, d])))


if __name__ == "__main__":
    main()
