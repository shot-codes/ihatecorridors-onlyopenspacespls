from abc import ABCMeta, abstractmethod
import sys
import math
import heapq

class Heuristic(metaclass=ABCMeta):
    def __init__(self, initial_state: 'State'):
        # Here's a chance to pre-process the static parts of the level.
        #self.x_goal
        #self.y_goal
        #self.num_agents = len(initial_state.agent_rows)
        #for row in initial_state._g:
        #    for col in row:
        #        for
        pass

    def h(self, state) -> 'int':
        # row = state.agent_rows
        # col = state.agent_cols
        # agent_colors = state.agent_colors
        # box_loc = state.boxes
        # box_colors = state.box_colors
        # goals = state._goals
        #
        # agent_to_box_h = 0
        # box_to_goal_h = 0
        # box_pos_col = {}
        # #agent to box distances
        # for i, rows in enumerate(box_loc):
        #     for j, cols in enumerate(rows):
        #         if cols != '':
        #             box_color = box_colors[ord(cols)-65]
        #             box_pos = (j,i)
        #             box_pos_col[cols] = (j,i)
        #             agent = [i.value for i in agent_colors if i == box_color]
        #             agent_pos = (col[agent[0]],row[agent[0]])
        #             agent_to_box_h+=self.map[agent_pos][box_pos]
        #
        #
        # #box to goal distances - includes initial agent location to agent goal if needed
        # for i, rows in enumerate(goals):
        #     for j, cols in enumerate(rows):
        #         if cols != '' and cols in box_pos_col:
        #             goal_pos = (j,i)
        #             box_pos = box_pos_col[cols]
        #             box_to_goal_h+=self.map[goal_pos][box_pos]
        #         elif cols != '':
        #             goal_pos = (j,i)
        #             agent_pos = (col[int(cols)],row[int(cols)])
        #             box_to_goal_h+=self.map[goal_pos][agent_pos]
        # # print(agent_to_box_h+box_to_goal_h,file=sys.stderr)
        # return agent_to_box_h+box_to_goal_h
        return 0

    @abstractmethod
    def f(self, state: 'State') -> 'int':
        pass

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError


class HeuristicDijkstra:
    assigned_boxes = []
    assigned_goals = []
    pre_processed_map = None
    def __init__(self):
        pass
    
    def h(self, state) -> 'int':

        agent_row = state.agent_rows
        # print(agent_row,file=sys.stderr)
        agent_col = state.agent_cols
        agent_to_box_h = 0
        box_to_goal_h = 0
        find_agent = None
        find_boxes = {}
        # print("goals",state._goals,file=sys.stderr)
        # print("GOALS HERE GET YOUR GOALS HERE",state._goals,file=sys.stderr)
        #if multiple boxes with one goal
        goal_amount = 0
        find_goals = {}
        single_goal = None
        for row, rows in enumerate(state._goals):
            for col, cols in enumerate(rows):
                if cols != '':
                    if cols not in find_goals:
                        find_goals[cols] = (col,row)
                        single_goal = cols
                        goal_pos = (col,row)
                        goal_amount+=1
        # print(goal_amount,file=sys.stderr)
        if goal_amount == 1:
            return self.single_goal(state,find_goals,single_goal)
        elif goal_amount > 1:
            # print("goal_amount",goal_amount,file=sys.stderr)
            # return self.mult_goals(state,find_goals)
            pass
        hej = "CHECK IF MULTIPLE GOALS FUCKS THE DICT"
              

        #If multiple boxes and multiple goals
        #agent to boxes h if only checking one agent at a time
        if len(agent_row) == 1:
            for row_pos, row in enumerate(state.boxes):
                # print("this is before 2nd loop", find_boxes,file=sys.stderr)
                for col_pos, col in enumerate(row):
                    if col != '':
                        find_boxes[col] = (col_pos, row_pos)
                        box_pos = (col_pos, row_pos)
                        agent_pos = (agent_col[0],agent_row[0])
                        if box_pos in self.pre_processed_map[agent_pos]:
                            agent_to_box_h+=self.pre_processed_map[agent_pos][box_pos]
                        else:
                            continue

            
        elif len(agent_row) > 1:
            for agent, agent_dic in enumerate(self.assigned_boxes):
                for letter in agent_dic[0]:
                    if len(agent_dic[0][letter]) > 0:
                        find_boxes[col] = (col_pos, row_pos)
                        box_pos = (agent_dic[0][letter][0][1],agent_dic[0][letter][0][0])
                        agent_pos = (col[agent],row[agent])
                        agent_to_box_h+=self.pre_processed_map[agent_pos][box_pos]
        #box to goal len == 1
        last_box = None           
        for row, rows in enumerate(state._goals):
            for col, cols in enumerate(rows):
                if cols != '' and "A" <= cols <= "Z":
                    box_pos = find_boxes[cols]
                    last_box = find_boxes[cols]
                    goal_pos = (col,row)
                    if box_pos in self.pre_processed_map[goal_pos]:
                        box_to_goal_h+=self.pre_processed_map[goal_pos][box_pos]
                    else:
                        continue
                    
                    
        #agent to goal len == 1
        for row, rows in enumerate(state._goals):
            for col, cols in enumerate(rows):
                if cols != '' and "0" <= cols <= "9":
                    if len(find_boxes) > 0:
                        goal_pos = (col,row)
                        agent_pos = find_boxes[list(find_boxes.keys())[-1]]
                        box_to_goal_h+=self.pre_processed_map[goal_pos][box_pos]
                    else:
                        goal_pos = (col,row)
                        agent_pos = last_box
                        box_to_goal_h+=self.pre_processed_map[goal_pos][agent_pos]
        return box_to_goal_h+agent_to_box_h
    

    def f(self, state: 'State') -> 'int':
        return state.g+self.h(state)

    def __repr__(self):
        pass

    def mult_goals(self, state, goals):
        agent_row = state.agent_rows
        # print(agent_row,file=sys.stderr)
        agent_col = state.agent_cols
        agent_to_box_h = 0
        box_to_goal_h = 0
        find_agent = None
        find_boxes = {}
        #If multiple boxes and multiple goals
        #agent to boxes h if only checking one agent at a time
        for row_pos, row in enumerate(state.boxes):
            # print("this is before 2nd loop", find_boxes,file=sys.stderr)
            for col_pos, col in enumerate(row):
                if col in goals:
                    goal_pos = goals[col]
                    box_pos = (col_pos, row_pos)
                    agent_pos = (agent_col[0],agent_row[0])
                    if box_pos in self.pre_processed_map[agent_pos]:
                        agent_to_box_h+=self.pre_processed_map[agent_pos][box_pos]
                    if box_pos in self.pre_processed_map[goal_pos]:
                        box_to_goal_h+=self.pre_processed_map[box_pos][goal_pos]
                    else:
                        continue
        return agent_to_box_h+box_to_goal_h
    
    def single_goal(self,state,goal,goal_letter):
        agent_row = state.agent_rows[0]
        agent_col = state.agent_cols[0]
        agent_to_box_h = 0
        box_to_agent_h = 0
        #If single box and single goal
        #agent to box
        for row_pos, row in enumerate(state.boxes):
            # print("this is before 2nd loop", find_boxes,file=sys.stderr)
            for col_pos, col in enumerate(row):
                if col == goal_letter:
                    box_pos = (col_pos, row_pos)
                    goal_pos = goal[col]
                    agent_pos = (agent_col,agent_row)
                    if box_pos in self.pre_processed_map[goal_pos]:
                        agent_to_box_h+=self.pre_processed_map[goal_pos][box_pos]
                    if box_pos in self.pre_processed_map[agent_pos]:
                        agent_to_box_h+=self.pre_processed_map[agent_pos][box_pos]
                    else:
                        continue
        return agent_to_box_h+box_to_agent_h


class HeuristicAStar(Heuristic):
    def __init__(self, initial_state: 'State'):
        super().__init__(initial_state)

    def f(self, state: 'State') -> 'int':
        return state.g + self.h(state)

    def __repr__(self):
        return 'A* evaluation'

class HeuristicWeightedAStar(Heuristic):
    def __init__(self, initial_state: 'State', w: 'int'):
        super().__init__(initial_state)
        self.w = w

    def f(self, state: 'State') -> 'int':
        return state.g + self.w * self.h(state)

    def __repr__(self):
        return 'WA*({}) evaluation'.format(self.w)

class HeuristicGreedy(Heuristic):
    def __init__(self, initial_state: 'State'):
        super().__init__(initial_state)

    def f(self, state: 'State') -> 'int':
        return self.h(state)

    def __repr__(self):
        return 'greedy evaluation'
