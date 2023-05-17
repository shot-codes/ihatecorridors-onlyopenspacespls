from state import State
import sys
import heapq

class Preprocessor:
    def __init__(self, initial_state: State) -> None:
        self.state = initial_state

    def boxes_to_walls(self):
        box_colors = set(self.state.box_colors)
        agent_colors = set(self.state.agent_colors)
        unassigned_boxes = box_colors - agent_colors
        unassigned_letters = [chr(ord('A') + i) for i in range(26) if self.state.box_colors[i] in unassigned_boxes]
        # print(unassigned_letters, file=sys.stderr, flush=True)
        for letter in unassigned_letters:
            for row in range(len(self.state.boxes)):
                for col in range(len(self.state.boxes[0])):
                    if self.state.boxes[row][col] == letter:
                        self.state.boxes[row][col] = ''
                        self.state.walls[row][col] = True

    def preprocess(self) -> State:
        self.boxes_to_walls()
        return self.state


class Dijkstra():
    def __init__(self, initial_state: 'State') -> None:
        self.state = initial_state
        self.agent_colors = self.state.agent_colors
        self.agent_row = self.state.agent_rows
        self.agent_col = self.state.agent_cols

        self.box_colors = self.state.box_colors
        self.box_locations = self.state.boxes
        self.walls = self.state.walls
        self.agent_to_box_h = 0
        self.box_to_goal_h = 0
        self.g = 0
        self.h = 0
        self.f = self.g+self.h

    def create_valid_squares_dic(self) -> dict:
        valid_squares = {(j,i): float('inf') for i,row in enumerate(self.walls) for j,col in enumerate(row) if col is False}
        return valid_squares

    def adjacency_dict(self, valid_dic: dict) -> dict:
        valid_dic = {key:{} for key in valid_dic}
        for i,j in valid_dic:
            vertex = (i,j)
            up = (i, j+1)
            down = (i, j-1)
            left = (i-1, j)
            right = (i+1, j)

            if up in valid_dic:
                if vertex in valid_dic[up]:
                    if vertex in valid_dic[up]:
                        pass
                else:
                    valid_dic[vertex][up] = 1
                    valid_dic[up][vertex] = 1
            if down in valid_dic:
                if vertex in valid_dic[down]:
                    pass
                else:
                    valid_dic[vertex][down] = 1
                    valid_dic[down][vertex] = 1
            if left in valid_dic:
                if vertex in valid_dic[left]:
                    pass
                else:
                    valid_dic[vertex][left] = 1
                    valid_dic[left][vertex] = 1
            if right in valid_dic:
                if vertex in valid_dic[right]:
                    pass
                else:
                    valid_dic[vertex][right] = 1
                    valid_dic[right][vertex] = 1
        return valid_dic


    def dijkstra(self, start: tuple[int, int], distance: dict) -> dict:
        #start is a tuple containing x,y values, i.e. col,rows.
        graph = self.adjacency_dict(distance)
        dist = distance.copy()
        dist[start] = 0
        queue = [(0, start)]

        while queue:
            current_distance, current_vertex = heapq.heappop(queue)
            if current_distance > dist[current_vertex]:
                continue

            for neighbour, cost in graph[current_vertex].items():
                new_distance = current_distance+cost

                if new_distance < dist[neighbour]:
                    dist[neighbour] = new_distance
                    heapq.heappush(queue, (new_distance, neighbour))
        delete_keys = []
        for i,j in dist.items():
            if isinstance(j, float):
                delete_keys.append(i)
        for i in delete_keys:
            del dist[i]
        return dist

    def distance_matrix(self):
        valid = self.create_valid_squares_dic()
        distance_matrix = {key:self.dijkstra(key, valid) for key in valid}
        return distance_matrix