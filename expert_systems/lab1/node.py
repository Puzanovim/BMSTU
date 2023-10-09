from enum import Enum


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
