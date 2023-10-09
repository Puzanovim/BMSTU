from pydantic import BaseModel

from expert_systems.lab1.node import Node


class TreeDescription(BaseModel):
    V: list[Node]
    E: dict[Node, list[Node]]
    source: Node
    target: Node
    directed: bool

    class Config:
        arbitrary_types_allowed = True


def get_one_to_eight_graph() -> TreeDescription:
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
    return TreeDescription(
        V=V,
        E=E,
        source=V[0],
        target=V[7],
        directed=False,
    )


def get_zero_to_nine_graph() -> TreeDescription:
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
    return TreeDescription(
        V=V,
        E=E,
        source=V[0],
        target=V[9],
        directed=True,
    )
