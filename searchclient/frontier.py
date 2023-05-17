from abc import ABCMeta, abstractmethod
from collections import deque
from queue import PriorityQueue
from itertools import count


class Frontier(metaclass=ABCMeta):
    @abstractmethod
    def add(self, state: "State"):
        raise NotImplementedError

    @abstractmethod
    def pop(self) -> "State":
        raise NotImplementedError

    @abstractmethod
    def is_empty(self) -> "bool":
        raise NotImplementedError

    @abstractmethod
    def size(self) -> "int":
        raise NotImplementedError

    @abstractmethod
    def contains(self, state: "State") -> "bool":
        raise NotImplementedError

    @abstractmethod
    def get_name(self):
        raise NotImplementedError


class FrontierBFS(Frontier):
    def __init__(self):
        super().__init__()
        self.queue = deque()
        self.set = set()

    def add(self, state: "State"):
        self.queue.append(state)
        self.set.add(state)

    def pop(self) -> "State":
        state = self.queue.popleft()
        self.set.remove(state)
        return state

    def is_empty(self) -> "bool":
        return len(self.queue) == 0

    def size(self) -> "int":
        return len(self.queue)

    def contains(self, state: "State") -> "bool":
        return state in self.set

    def get_name(self):
        return "breadth-first search"


class FrontierDFS(Frontier):
    def __init__(self):
        super().__init__()
        raise NotImplementedError

    def add(self, state: "State"):
        raise NotImplementedError

    def pop(self) -> "State":
        raise NotImplementedError

    def is_empty(self) -> "bool":
        raise NotImplementedError

    def size(self) -> "int":
        raise NotImplementedError

    def contains(self, state: "State") -> "bool":
        raise NotImplementedError

    def get_name(self):
        return "depth-first search"


class FrontierBestFirst(Frontier):
    def __init__(self, heuristic: "Heuristic"):
        super().__init__()
        self.heuristic = heuristic
        self.queue = PriorityQueue()
        self.set = set()
        self._counter = count()

    def add(self, state: "State"):
        f = self.heuristic.f(state)
        self.queue.put((f, next(self._counter), state))
        self.set.add(state)

    def pop(self) -> "State":
        return self.queue.get()[2]

    def is_empty(self) -> "bool":
        return self.queue.empty()

    def size(self) -> "int":
        return self.queue.qsize()

    def contains(self, state: "State") -> "bool":
        return state in self.set

    def get_name(self):
        return "best-first search using {}".format(self.heuristic)


class CBSQueue:
    def __init__(self):
        self.queue = PriorityQueue()
        self.set = set()
        self._counter = count()

    def _cost(self, node):
        solution = node.solution
        cost = 0.0
        for agent_solution in solution:
            if agent_solution is None:
                return float("inf")
            cost += len(agent_solution)
        return cost

    def add(self, node):
        cost = self._cost(node)
        node.cost = cost
        if cost < float("inf"):
            self.queue.put((cost, next(self._counter), node))
            self.set.add(node)

    def pop(self) -> "State":
        return self.queue.get()[2]

    def is_empty(self) -> "bool":
        return self.queue.empty()

    def size(self) -> "int":
        return self.queue.qsize()

    def contains(self, state: "State") -> "bool":
        return state in self.set

    def get_name(self):
        return "CBS"
