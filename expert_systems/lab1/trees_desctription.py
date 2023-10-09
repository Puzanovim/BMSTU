from expert_systems.lab1.node import Node


def get_one_to_eight_graph() -> tuple[list[Node], dict[Node, list[Node]], Node, Node]:
    V: list[Node] = [Node(num) for num in range(1, 9)]
    E: dict[Node, list[Node]] = {
        V[0]: [V[1], V[4]],
        V[1]: [V[0], V[5]],
        V[2]: [V[3], V[5], V[6]],
        V[3]: [V[2], V[6], V[7]],
        V[4]: [V[0]],
        V[5]: [V[1], V[2], V[6]],
        V[6]: [V[2], V[3], V[5], V[7]],
        V[7]: [V[3], V[6]],
    }
    source: Node = V[0]
    target: Node = V[7]
    return V, E, source, target


def get_zero_to_nine_graph() -> tuple[list[Node], dict[Node, list[Node]], Node, Node]:
    V: list[Node] = [Node(num) for num in range(0, 10)]
    E: dict[Node, list[Node]] = {
        V[0]: [V[1], V[2], V[3]],
        V[1]: [V[4]],
        V[2]: [V[4], V[5]],
        V[3]: [V[5], V[6]],
        V[4]: [V[8]],
        V[5]: [V[4], V[7], V[9]],
        V[6]: [V[7]],
        V[7]: [V[9]],
        V[8]: [],
        V[9]: [V[8]],
    }
    source: Node = V[0]
    target: Node = V[9]
    return V, E, source, target
