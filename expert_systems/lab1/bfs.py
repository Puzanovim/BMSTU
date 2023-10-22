from queue import Queue

from expert_systems.lab1.node import Node, Status
from expert_systems.lab1.plot_graph import PlotGraph


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
