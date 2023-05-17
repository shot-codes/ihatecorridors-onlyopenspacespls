import copy
import sys
import traceback

from graphsearch import search
from frontier import FrontierBestFirst, CBSQueue
from heuristic import HeuristicDijkstra
from state import State
from action import Action
from conflict import Conflict
from preprocessing import Preprocessor, Dijkstra
from assigner import Assigner, PathUtils


class Root:
    initial_state = None

    def __init__(self, num_agents, count=0):
        self.count = count
        self.solution = []
        self.cost = 0
        self.constraints = [set() for _ in range(num_agents)]

    def get_conflict(self) -> "Conflict":
        longest_plan = len(max(self.solution, key=len))
        state = copy.deepcopy(self.initial_state)
        for step in range(longest_plan):
            joint_action = []
            for agent, _ in enumerate(self.solution):
                try:
                    action = self.solution[agent][step]
                except IndexError:
                    action = [Action.NoOp]
                joint_action = joint_action + action
            conflicts = state.is_conflict(joint_action, state.t)
            if conflicts:
                return conflicts
            state = state.apply_action(joint_action)
        return None

    def extract_plan(self):
        solution = []
        longest_plan = len(max(self.solution, key=len))
        for step in range(longest_plan):
            joint_action = []
            for agent, _ in enumerate(self.solution):
                try:
                    action = self.solution[agent][step]
                except IndexError:
                    action = [Action.NoOp]
                joint_action = joint_action + action
            solution.append(joint_action)
        return solution


def catch_items(state, agent, reachability_maps):
    def get_goal_char(letter, letters):
        if letter in letters:
            if ord('0') <= ord(letter) <= ord('9'):
                return "0"
            else:
                return letter
        else:
            return ""

    reachability_map = reachability_maps[agent]
    agent_color = state.agent_colors[agent]
    letters = [chr(ord("0") + agent)] + [chr(ord('A') + i) for i in range(26) if state.box_colors[i] == agent_color]
    boxes = [[state.boxes[row][col] if state.boxes[row][col] in letters and reachability_map[row][col] else "" for col in range(len(state.boxes[0]))] for row in range(len(state.boxes))]
    goal = [[get_goal_char(state._goals[row][col], letters) if reachability_map[row][col] else "" for col in range(len(state.boxes[0]))] for row in range(len(state.boxes))]
    # print(f"boxes: {boxes} goals: {goal} agent: {agent}", file=sys.stderr)
    return boxes, goal


def replace_colors(state: State, agent: int) -> State:
    updated_state = copy.deepcopy(state)
    agent_color = copy.deepcopy(state.agent_colors[agent])
    first_box_color = state.box_colors[0]
    for i in range(len(state.box_colors)):
        if state.box_colors[i] is not agent_color:
            updated_state.box_colors[i] = None
        else:
            updated_state.box_colors[i] = first_box_color
    return updated_state


def cbs_search(initial_state, frontier, reachability_maps):
    root = Root(len(initial_state.agent_rows))
    Root.initial_state = copy.deepcopy(initial_state)
    goals = []
    boxes = []
    for agent, _ in enumerate(initial_state.agent_rows):
        state = copy.deepcopy(initial_state)
        sa_frontier = FrontierBestFirst(HeuristicDijkstra())
        agent_row, agent_col = [state.agent_rows[agent]], [state.agent_cols[agent]]
        box, goal = catch_items(state, agent, reachability_maps)
        sa_state = replace_colors(State(agent_row, agent_col, box, goal, initial_state.box_colors), agent)
        # print("Boxes:", agent, sa_state.boxes, file=sys.stderr)
        # print("Goals:", agent, sa_state._goals, file=sys.stderr)
        goals.append(goal); boxes.append(box)
        # print(f"Initial search for agent {agent} of color {state.agent_colors[agent]} with boxes {state.box_colors}", file=sys.stderr)
        plan = search(sa_state, sa_frontier)
        # print(f"Initial plan for agent {agent}: {plan}", file=sys.stderr)
        root.solution.append(plan)
    frontier.add(root)
    count = 0
    while not frontier.is_empty():
        print("Count:", count, file=sys.stderr)
        node = frontier.pop()
        for i, solution in enumerate(node.solution):
            print("Popped:", i, solution, file=sys.stderr)
            pass
        conflict = node.get_conflict()
        if conflict is None:
            plan = node.extract_plan()
            return plan
        for agent in conflict.agents:
            constraints = conflict.constraints[agent]
            print("New:", agent, conflict.type, constraints, file=sys.stderr)
            sa_frontier = FrontierBestFirst(HeuristicDijkstra())
            m = copy.deepcopy(node)
            m.count = count
            m.constraints[agent].update(constraints)
            print("Total:", agent, m.constraints[agent], file=sys.stderr)
            if not conflict.resolveable[agent]:
                plan = None
            else:
                plan = resolve_conflict(
                    agent, m.constraints[agent], initial_state, boxes[agent], goals[agent], state.box_colors
                )
                m.solution[agent] = plan
                if plan:
                    print("Fixed:", agent, plan, file=sys.stderr)
                    frontier.add(m)
        count += 1
        # print("____________________________________", file=sys.stderr)


def resolve_conflict(agent, constraints, initial_state, box, goal, box_colors):
    sa_frontier = FrontierBestFirst(HeuristicDijkstra())
    agent_row, agent_col = [initial_state.agent_rows[agent]], [
        initial_state.agent_cols[agent]
    ]
    sa_state = State(agent_row, agent_col, box, goal, box_colors)
    # print(f"Conflict resolution search for agent {agent}", file=sys.stderr)
    plan = search(sa_state, sa_frontier, constraints=constraints)
    return plan


def get_final_state(initial_state, plan):
    state = copy.deepcopy(initial_state)
    for joint_action in plan:
        state = state.apply_action(joint_action)
    return state


def sequential_cbs(initial_state):
    state = Preprocessor(initial_state).preprocess()
    pre_map = Dijkstra(state).distance_matrix()
    HeuristicDijkstra.pre_processed_map = pre_map
    floodfill = PathUtils(State.walls)
    reachability_maps = [floodfill.get_reachability_map((state.agent_rows[agent], state.agent_cols[agent])) for agent in range(len(initial_state.agent_rows))]
    assigner = Assigner(state)
    agent_tasks = [task[1:-1] for task in assigner.assign_plans()]
    #print(agent_tasks, file=sys.stderr)
    initial_state_goals = copy.deepcopy(initial_state._goals)
    boxes = copy.deepcopy(initial_state.boxes)
    plan = []
    max_task_length = max([len(task) for task in agent_tasks])
    for i in range(max_task_length):
        goals = [["" for col in range(len(initial_state.boxes[0]))] for row in range(len(initial_state.boxes))]
        for j, agent_task in enumerate(agent_tasks):
            try:
                task = agent_task[i]
                goals = [[task.letter if task.position == (row, col) else goals[row][col] for col in range(len(initial_state.walls[0]))] for row in range(len(initial_state.walls))]
            except IndexError as e:
                pass
        state._goals = goals
        print(state, file=sys.stderr)
        step_plan = cbs_search(state, CBSQueue(), reachability_maps)
        print(step_plan, file=sys.stderr)
        plan += step_plan
        # print(plan, file=sys.stderr)
        state = get_final_state(state, step_plan)
        print(state, file=sys.stderr)
        boxes = state.boxes
        for row in range(len(boxes)):
            for col in range(len(boxes[0])):
                if boxes[row][col] == initial_state_goals[row][col]:
                    boxes[row][col] = ""
        state.boxes = boxes
        # print(boxes, file=sys.stderr)
    # print(plan, file=sys.stderr)
    # print(get_final_state(initial_state, plan), file=sys.stderr)
    return plan
