from enum import Enum, unique

@unique
class ActionType(Enum):
    NoOp = 0
    Move = 1
    Push = 2
    Pull = 3

@unique
class Action(Enum):
    NoOp = ("NoOp", ActionType.NoOp, 0, 0, 0, 0)

    MoveN = ("Move(N)", ActionType.Move, -1, 0, 0, 0)
    MoveS = ("Move(S)", ActionType.Move, 1, 0, 0, 0)
    MoveE = ("Move(E)", ActionType.Move, 0, 1, 0, 0)
    MoveW = ("Move(W)", ActionType.Move, 0, -1, 0, 0)

    PushNS = ("Push(N,S)", ActionType.Push, -1, 0, 1, 0)
    PushNN = ("Push(N,N)", ActionType.Push, -1, 0, -1, 0)
    PushNE = ("Push(N,E)", ActionType.Push, -1, 0, 0, 1)
    PushNW = ("Push(N,W)", ActionType.Push, -1, 0, 0, -1)
    PushSS = ("Push(S,S)", ActionType.Push, 1, 0, 1, 0)
    PushSN = ("Push(S,N)", ActionType.Push, 1, 0, -1, 0)
    PushSE = ("Push(S,E)", ActionType.Push, 1, 0, 0, 1)
    PushSW = ("Push(S,W)", ActionType.Push, 1, 0, 0, -1)
    PushES = ("Push(E,S)", ActionType.Push, 0, 1, 1, 0)
    PushEN = ("Push(E,N)", ActionType.Push, 0, 1, -1, 0)
    PushEE = ("Push(E,E)", ActionType.Push, 0, 1, 0, 1)
    PushEW = ("Push(E,W)", ActionType.Push, 0, 1, 0, -1)
    PushWS = ("Push(W,S)", ActionType.Push, 0, -1, 1, 0)
    PushWN = ("Push(W,N)", ActionType.Push, 0, -1, -1, 0)
    PushWE = ("Push(W,E)", ActionType.Push, 0, -1, 0, 1)
    PushWW = ("Push(W,W)", ActionType.Push, 0, -1, 0, -1)

    PullNS = ("Pull(N,S)", ActionType.Pull, -1, 0, 1, 0)
    PullNN = ("Pull(N,N)", ActionType.Pull, -1, 0, -1, 0)
    PullNE = ("Pull(N,E)", ActionType.Pull, -1, 0, 0, 1)
    PullNW = ("Pull(N,W)", ActionType.Pull, -1, 0, 0, -1)
    PullSS = ("Pull(S,S)", ActionType.Pull, 1, 0, 1, 0)
    PullSN = ("Pull(S,N)", ActionType.Pull, 1, 0, -1, 0)
    PullSE = ("Pull(S,E)", ActionType.Pull, 1, 0, 0, 1)
    PullSW = ("Pull(S,W)", ActionType.Pull, 1, 0, 0, -1)
    PullES = ("Pull(E,S)", ActionType.Pull, 0, 1, 1, 0)
    PullEN = ("Pull(E,N)", ActionType.Pull, 0, 1, -1, 0)
    PullEE = ("Pull(E,E)", ActionType.Pull, 0, 1, 0, 1)
    PullEW = ("Pull(E,W)", ActionType.Pull, 0, 1, 0, -1)
    PullWS = ("Pull(W,S)", ActionType.Pull, 0, -1, 1, 0)
    PullWN = ("Pull(W,N)", ActionType.Pull, 0, -1, -1, 0)
    PullWE = ("Pull(W,E)", ActionType.Pull, 0, -1, 0, 1)
    PullWW = ("Pull(W,W)", ActionType.Pull, 0, -1, 0, -1)

    def __init__(self, name, type, ard, acd, brd, bcd):
        self.name_ = name
        self.type = type
        self.agent_row_delta = ard # horisontal displacement agent
        self.agent_col_delta = acd # vertical displacement agent
        self.box_row_delta = brd # horisontal displacement box
        self.box_col_delta = bcd # vertical displacement box

    def __repr__(self):
        return self.name
