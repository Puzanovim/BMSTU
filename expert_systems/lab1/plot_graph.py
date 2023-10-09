import time

import matplotlib.pyplot as plt
import networkx as nx

from expert_systems.lab1.node import Node, Status


class PlotGraph:
    def __init__(self, E: dict[Node, list[Node]], source: Node, target: Node, point_node_color: str = 'pink'):
        self._graph = nx.Graph()
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
