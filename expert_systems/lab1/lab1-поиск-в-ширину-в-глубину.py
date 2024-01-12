import time
from collections import deque
from queue import Queue

import matplotlib.pyplot as plt
import networkx as nx

from argparse import ArgumentParser, Namespace
from enum import Enum

from pydantic import BaseModel


class Status(Enum):
    WHITE = 'WHITE'
    GREY = 'GREY'
    BLACK = 'BLACK'


class Node:
    def __init__(self, number: int) -> None:
        self.number = number
        self.previous: Node | None = None
        self.status: Status = Status.WHITE

    def __repr__(self):
        return f'({self.number}' + (f': {self.previous})' if self.previous else ')')


class PlotGraph:
    def __init__(
            self,
            E: dict[Node, list[Node]],
            source: Node,
            target: Node,
            directed: bool,
            point_node_color: str = 'pink',
    ):
        self._graph = nx.DiGraph() if directed else nx.Graph()
        self._E = E
        self._source = source
        self._target = target
        self._point_node_color = point_node_color
        self._node_colors_map: dict[Node, str] = {}
        self._edge_colors_map: dict[tuple[int, int], str]

        graph_nodes: list[int] = []
        graph_edges: list[tuple[int, int]] = []

        for node, vertices in E.items():
            graph_nodes.append(node.number)
            self._node_colors_map[node] = 'blue'
            graph_edges.extend([(node.number, v.number) for v in vertices])

        self._node_colors_map[self._source] = 'green'
        self._node_colors_map[self._target] = 'red'

        self._graph.add_nodes_from(graph_nodes)
        self._graph.add_edges_from(graph_edges)

        self._edge_colors_map = {edge: 'black' for edge in self._graph.edges}

    def _match_source_target_node(self, node: Node, color: str) -> None:
        match node:
            case self._source:
                self._node_colors_map[node] = 'green'
            case self._target:
                self._node_colors_map[node] = 'red'
            case _:
                self._node_colors_map[node] = color

    def plot(self, path_edges: list[tuple[int, int]] | None = None):

        for node, vertices in self._E.items():
            match node.status:
                case Status.WHITE:
                    self._match_source_target_node(node, 'blue')
                case Status.GREY:
                    self._node_colors_map[node] = 'pink'
                case Status.BLACK:
                    self._match_source_target_node(node, 'grey')

        if path_edges:
            for pair in path_edges:
                if self._edge_colors_map.get(pair):
                    self._edge_colors_map[pair] = 'red'
                if self._edge_colors_map.get(pair[::-1]):
                    self._edge_colors_map[pair[::-1]] = 'red'

        nx.draw(
            self._graph,
            node_color=self._node_colors_map.values(),
            edge_color=self._edge_colors_map.values(),
            pos=nx.planar_layout(self._graph, center=[1, 10]),
            node_size=1000,
            font_size=15,
            width=2,
            with_labels=True,
        )
        plt.show()
        time.sleep(1)

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


class Trees(Enum):
    NotDirected = 'NotDirected'
    Directed = 'Directed'


class Searcher(Enum):
    bfs = 'bfs'
    dfs = 'dfs'


class BFS:
    def __init__(
        self, V: list[Node], E: dict[Node, list[Node]], source: Node, plot_graph: PlotGraph
    ) -> None:
        self.V = V
        self.E = E
        self._plot_graph = plot_graph
        self._opened = Queue()
        self._closed: set[Node] = set()

        self._opened.put(source)

        print('Init BFS by Open Close')

    def _open_node(self) -> Node:
        node = self._opened.get()
        node.status = Status.GREY
        return node

    def _close_node(self, node: Node) -> None:
        self._closed.add(node)
        node.status = Status.BLACK

    def search(self, target: Node) -> Node | None:
        print(f'Start search {target}')

        while not self._opened.empty():
            n = self._open_node()
            self._plot_graph.plot()
            self._close_node(n)

            for v in self.E.get(n):
                if v.status == Status.WHITE:
                    self._opened.put(v)
                    v.previous = n
                    if v == target:
                        print(f'Target found')
                        return v
        else:
            print(f'Target not found')


class DFS:
    def __init__(
        self, V: list[Node], E: dict[Node, list[Node]], source: Node, plot_graph: PlotGraph,
    ) -> None:
        self.V = V
        self.E = E
        self._plot_graph = plot_graph
        self._opened = deque()
        self._closed: set[Node] = set()

        self._opened.append(source)

        print('Init DFS by Open Close')

    def _open_node(self) -> Node:
        node = self._opened.pop()
        node.status = Status.GREY
        return node

    def _close_node(self, node: Node) -> None:
        self._closed.add(node)
        node.status = Status.BLACK

    def search(self, target: Node) -> Node | None:
        print(f'Start search {target}')

        while len(self._opened) > 0:
            n = self._open_node()
            self._plot_graph.plot()
            self._close_node(n)

            for v in self.E.get(n):
                if v.status == Status.WHITE:
                    self._opened.append(v)
                    v.previous = n
                    if v == target:
                        print(f'Target found')
                        return v
        else:
            print(f'Target not found')



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
