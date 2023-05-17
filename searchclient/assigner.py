import collections
from sys import stderr

from state import State

class PathUtils:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.reachability_map = [[False] * len(grid[0]) for _ in range(len(grid))]

    def dfs(self, x, y) -> None:
        if x < 0 or y < 0 or x >= len(self.grid) or y >= len(self.grid[0]):
            return
        if self.grid[x][y]:
            return
        if self.reachability_map[x][y]:
            return
        self.reachability_map[x][y] = True
        self.dfs(x + 1, y)
        self.dfs(x - 1, y)
        self.dfs(x, y + 1)
        self.dfs(x, y - 1)

    def bfs(self, start, target) -> list:
        queue = collections.deque([[start]])
        seen = set([start])

        while queue:
            path = queue.popleft()
            y, x = path[-1]

            if (y, x) == target:
                return path

            for y2, x2 in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= x2 < len(self.grid[0]) and 0 <= y2 < len(self.grid) and not self.grid[y2][x2] and (y2, x2) not in seen:
                    queue.append(path + [(y2, x2)])
                    seen.add((y2, x2))

        return None

    def get_reachability_map(self, position) -> list:
        self.reachability_map = [[False] * len(self.grid[0]) for _ in range(len(self.grid))]
        x, y = position
        self.dfs(x, y)
        return self.reachability_map


class Goal:
    def __init__(self, position, letter) -> None:
        self.position = position
        self.letter = letter

    def __repr__(self) -> str:
        return f"Goal({self.position}, {self.letter})"


class GoalsGraph:
    def __init__(self, tasks, agent_position) -> None:
        path_utils = PathUtils(State.walls)
        self.nodes = dict()
        start = Goal("start", None)
        finish = Goal("finish", None)
        self.nodes[start] = set()
        self.nodes[finish] = set()
        for letter in tasks:
            for position in tasks[letter]:
                goal = Goal(position, letter)
                self.nodes[goal] = {finish}
                self.nodes[start].add(goal)

        for node, neighbours in self.nodes.items():
            if node == start or node == finish or not ord("A") <= ord(node.letter) <= ord("Z"):
                continue
            path = path_utils.bfs(agent_position, node.position)
            for other_node in self.nodes:
                if other_node == start or other_node == finish:
                    continue
                if not ord('A') <= ord(other_node.letter) <= ord('Z') or other_node != node and other_node.position in path:
                    self.nodes[node].add(other_node)

    def get_order(self) -> list:
        visited = {node: False for node in self.nodes}
        stack = []

        def topologicalSortUtil(node):
            visited[node] = True
            for neighbour in self.nodes[node]:
                if not visited[neighbour]:
                    topologicalSortUtil(neighbour)
            stack.insert(0, node)

        for node in self.nodes:
            if not visited[node]:
                topologicalSortUtil(node)

        return stack

    def __repr__(self) -> str:
        return f"GoalsGraph({self.nodes})"


class Assigner:
    def __init__(self, initial_state: State) -> None:
        self.state = initial_state

    def assign_tasks_to_agent(self, agent) -> tuple:
        n_rows, n_cols = len(self.state._goals), len(self.state._goals[0])
        agent_color = State.agent_colors[agent]
        letters = [chr(ord('A') + i) for i in range(26) if self.state.box_colors[i] == agent_color]
        floodfill = PathUtils(State.walls)
        reachability_map = floodfill.get_reachability_map((self.state.agent_rows[agent], self.state.agent_cols[agent]))
        boxes = {}
        for letter in letters:
            boxes[letter] = [(row, col) for row in range(n_rows) for col in range(n_cols) if self.state.boxes[row][col] == letter and reachability_map[row][col]]
        goals = {}
        for letter in letters + [chr(ord('0') + agent)]:
            goals[letter] = [(row, col) for row in range(n_rows) for col in range(n_cols) if self.state._goals[row][col] == letter and reachability_map[row][col]]

        # print(f"Agent {agent} boxes: {boxes}", file=stderr, flush=True)
        # print(f"Agent {agent} goals: {goals}", file=stderr, flush=True)
        return boxes, goals

    def get_graph(self, agent) -> GoalsGraph:
        tasks = self.assign_tasks_to_agent(agent)[1]
        agent_position = (self.state.agent_rows[agent], self.state.agent_cols[agent])
        graph = GoalsGraph(tasks, agent_position)
        # print(graph.nodes, file=stderr, flush=True)
        return graph

    def assign_plans(self) -> list:
        return [self.get_graph(agent).get_order() for agent in range(len(self.state.agent_rows))]
