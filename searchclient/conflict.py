import sys


class Conflict:
    def __init__(self, agents, constraints, conflict, type_):
        self.type = type_
        self.agents = agents
        self.conflict = conflict
        self.constraints = {}
        for count, agent in enumerate(agents):
            self.constraints[agent] = constraints[count]

        self.resolveable = self.is_resolveable()

    @classmethod
    def vertex(cls, conflict):
        """(a1,a2,v,t)"""
        type_ = "VERTEX"
        constraints = []
        *agents, v, t = conflict
        for _ in agents:
            c = set()
            c.add((v, t))
            # c.add((v, t - 1))  ## extra follow conflict for speed
            constraints.append(c)
        return cls(agents, constraints, conflict, type_)

    @classmethod
    def edge(cls, conflict):
        """(a1,a2,v1,v2,t)"""
        type_ = "EDGE"
        constraints = []
        *agents, v1, v2, t = conflict
        v = [v1, v2]
        for count, _ in enumerate(agents):
            c = set()
            for vertex in v:
                c.add((vertex, t))
                # c.add((vertex, t + 1))  #### extra speed# future follow conflict
            c.add((v[count], t - 1))
            constraints.append(c)

        return cls(agents, constraints, conflict, type_)

    @classmethod
    def follow(cls, conflict):
        """(a1,a2,v,t) a1 follows a2"""
        type_ = "FOLLOW"
        constraints = []
        *agents, v, t = conflict
        times = [t, t - 1]
        # times2 = [t, t + 1]
        for count, _ in enumerate(agents):
            c = set()
            c.add((v, times[count]))
            # c.add((v, times2[count]))  ## extra speed
            c.add((v, t))
            constraints.append(c)
        return cls(agents, constraints, conflict, type_)

    def is_resolveable(self):
        resolveable = {}
        for agent in self.agents:
            resolveable[agent] = True
            for constraint in self.constraints[agent]:
                if constraint[-1] < 0:
                    if self.type == "FOLLOW":
                        resolveable[agent] = False  # Not resolveable for t < 0
        return resolveable
