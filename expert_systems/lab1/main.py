from expert_systems.lab1.bfs import BFS
from expert_systems.lab1.node import Node, Status
from expert_systems.lab1.plot_graph import PlotGraph


def get_path(result: Node) -> tuple[list[int], list[tuple[int, int]]]:
    node = result
    path = [node.number]
    while node.previous:
        node = node.previous
        path.append(node.number)
    path_edges = [(i, j) for i, j in zip(path, path[1:])]
    return path, path_edges


def print_vertices(V: list[Node]) -> None:
    closed_v = []
    open_v = []
    for v in V:
        match v.status:
            case Status.WHITE:
                open_v.append(v.number)
            case Status.BLACK:
                closed_v.append(v.number)

    print(f'OPENED: {open_v}')
    print(f'CLOSED: {closed_v}')


def do_algorithm(
    V: list[Node], E: dict[Node, list[Node]], source: Node, target: Node, plot_graph: PlotGraph,
) -> None:
    searcher = BFS(V, E, source, plot_graph)

    result = searcher.search(target)

    print_vertices(V)
    if result:
        path, path_edges = get_path(result)
        print(f'PATH NODES: {path[::-1]}')
        print(f'PATH EDGES: {path_edges}')
        plot_graph.plot(path_edges=path_edges)
    else:
        plot_graph.plot()


def main():
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

    plot_graph = PlotGraph(E, source, target)
    plot_graph.plot()
    do_algorithm(V, E, source, target, plot_graph)


if __name__ == '__main__':
    main()
