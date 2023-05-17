import memory
import time
import sys

from action import Action
from assigner import Assigner
from preprocessing import Preprocessor
globals().update(Action.__members__)

start_time = time.perf_counter()

def search(initial_state, frontier, constraints=set()):
    iterations = 0

    frontier.add(initial_state)
    explored = set()

    while True:
        iterations += 1
        if iterations % 1000 == 0:
            pass
            # print_search_status(explored, frontier)

        if memory.get_usage() > memory.max_usage:
            # print_search_status(explored, frontier)
            # print("Maximum memory usage exceeded.", file=sys.stderr, flush=True)
            return None

        if frontier.is_empty():
            return None

        state = frontier.pop()

        # print(state, file=sys.stderr)

        if state.is_goal_state(constraints):
            plan = state.extract_plan()
            # print(state.get_visited_locations(), file=sys.stderr, flush=True)
            # print(constraints, file=sys.stderr, flush=True)
            # print(f"{plan}\n{constraints}\n{state.t}\n\n", file=sys.stderr, flush=True)
            return plan

        explored.add(state)

        for child in state.get_expanded_states(constraints):
            if not frontier.contains(child) and child not in explored:
                frontier.add(child)


def print_search_status(explored, frontier):
    status_template = "#Expanded: {:8,}, #Frontier: {:8,}, #Generated: {:8,}, Time: {:3.3f} s\n[Alloc: {:4.2f} MB, MaxAlloc: {:4.2f} MB]"
    elapsed_time = time.perf_counter() - start_time
    print(
        status_template.format(
            len(explored),
            frontier.size(),
            len(explored) + frontier.size(),
            elapsed_time,
            memory.get_usage(),
            memory.max_usage,
        ),
        file=sys.stderr,
        flush=True,
    )
