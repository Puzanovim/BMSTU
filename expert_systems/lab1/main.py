from argparse import ArgumentParser, Namespace
from enum import Enum

from expert_systems.lab1.bfs import BFS
from expert_systems.lab1.dfs import DFS
from expert_systems.lab1.node import Node, Status
from expert_systems.lab1.plot_graph import PlotGraph
from expert_systems.lab1.trees_desctription import get_one_to_eight_graph, get_zero_to_nine_graph


class Trees(Enum):
    NotDirected = 'NotDirected'
    Directed = 'Directed'


class Searcher(Enum):
    bfs = 'bfs'
    dfs = 'dfs'


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
    V: list[Node], target: Node, plot_graph: PlotGraph, searcher: BFS | DFS
) -> None:
    result = searcher.search(target)

    print_vertices(V)
    if result:
        path, path_edges = get_path(result)
        print(f'PATH NODES: {path[::-1]}')
        print(f'PATH EDGES: {path_edges}')
        plot_graph.plot(path_edges=path_edges)
    else:
        plot_graph.plot()


def main(tree_arg: Trees, searcher_arg: Searcher):
    match tree_arg:
        case Trees.NotDirected:
            tree_description = get_one_to_eight_graph()
        case Trees.Directed:
            tree_description = get_zero_to_nine_graph()
        case _:
            raise Exception('Tree not found')

    V = tree_description.V
    E = tree_description.E
    source = tree_description.source
    target = tree_description.target
    plot_graph = PlotGraph(E, source, target, directed=tree_description.directed)
    plot_graph.plot()

    match searcher_arg:
        case Searcher.bfs:
            searcher = BFS(V, E, source, plot_graph)
        case Searcher.dfs:
            searcher = DFS(V, E, source, plot_graph)
        case _:
            raise Exception('Searcher not found')

    do_algorithm(V, target, plot_graph, searcher)


def _arg_parse() -> Namespace:
    parser = ArgumentParser(prog='GraphSearcher')
    parser.add_argument(
        '-t',
        '--tree',
        type=Trees,
        default=Trees.NotDirected,
        choices=Trees,
    )
    parser.add_argument(
        '-s',
        '--searcher',
        type=Searcher,
        default=Searcher.dfs,
        choices=Searcher,
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = _arg_parse()
    main(tree_arg=args.tree, searcher_arg=args.searcher)
