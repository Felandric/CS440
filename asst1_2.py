from graphics import *
import random

draw = True #set whether or not to draw the grid

#initialize RNG
random.seed(12345)

UNVISITED = 0
UNBLOCKED = 1
BLOCKED = 2

RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

class State:
    def __init__(self, posx, posy, g):
        self.posx = posx
        self.posy = posy
        self.g = g
        self.h = (100 - posx) + (100 - posy)
        if g == INF:
            self.f = INF
        else:
            self.f = g + self.h
        self.treepointer = None

    def setg(self, g):
        self.g = g
        if g == INF:
            self.f = INF
        else:
            self.f = g + self.h

for g in range(50):
    filename = "%d.txt"%g
    file = open(filename, 'r')
    print(filename)
    #initialize grid
    if draw:
        win = GraphWin('Grid', 510, 510)
        win.setCoords(0.0, 0.0, 101.0, 101.0)
        win.setBackground("white")
    grid = list()
    for x in range(101):
        grid.append(list())
        for y in range(101):
            grid[x].append(int(file.read(1)))
            if draw and grid[x][y] == BLOCKED:
                pos = Rectangle(Point(x, y), Point(x + 1, y + 1))
                pos.setFill("black")
                pos.draw(win)
        file.read(1)
    file.close()

    naivegrid = list()
    for x in range(101):
        naivegrid.append(list())
        for y in range(101):
            naivegrid[x].append(UNVISITED)

    searchgrid = list()
    OPEN = list()
    INF = -1
    COST = 1
    start = State(0, 0, 0) #initialize at 0, 0, overwrite blocked if blocked, goal is 100, 100
    goal = State(100, 100, INF)

    pos = Rectangle(Point(goal.posx, goal.posy), Point(goal.posx + 1, goal.posy + 1))
    pos.setFill("red")
    pos.draw(win)

    def ComputePath():
        searchgrid = list()
        for x in range(101):
            searchgrid.append(list())
            for y in range(101):
                searchgrid[x].append(None)

        prev = None
        searchgrid[goal.posx][goal.posy] = goal
        while OPEN and (searchgrid[goal.posx][goal.posy].g == INF or searchgrid[goal.posx][goal.posy].g > OPEN[0].f):
            current = OPEN.pop(0)
            succs = list()
            searchgrid[current.posx][current.posy] = current
            if current.posx + 1 < 101 and prev != LEFT and naivegrid[current.posx + 1][current.posy] != BLOCKED:
                if searchgrid[current.posx + 1][current.posy] == None:
                    searchgrid[current.posx + 1][current.posy] = State(current.posx + 1, current.posy, INF)
                succs.append(searchgrid[current.posx + 1][current.posy])

            if current.posx - 1 > -1 and prev != RIGHT and naivegrid[current.posx - 1][current.posy] != BLOCKED:
                if searchgrid[current.posx - 1][current.posy] == None:
                    searchgrid[current.posx - 1][current.posy] = State(current.posx - 1, current.posy, INF)
                succs.append(searchgrid[current.posx - 1][current.posy])

            if current.posy + 1 < 101 and prev != DOWN and naivegrid[current.posx][current.posy + 1] != BLOCKED:
                if searchgrid[current.posx][current.posy + 1] == None:
                    searchgrid[current.posx][current.posy + 1] = State(current.posx, current.posy + 1, INF)
                succs.append(searchgrid[current.posx][current.posy + 1])

            if current.posy - 1 > -1 and prev != UP and naivegrid[current.posx][current.posy - 1] != BLOCKED:
                if searchgrid[current.posx][current.posy - 1] == None:
                    searchgrid[current.posx][current.posy - 1] = State(current.posx, current.posy - 1, INF)
                succs.append(searchgrid[current.posx][current.posy - 1])

            for state in succs:
                if state.g == INF or state.g > current.g + COST:
                    state.setg(current.g + COST)
                    state.treepointer = current
                    if state in OPEN:
                        OPEN.remove(state)
                    if not OPEN:
                        OPEN.insert(0, state)
                    else:
                        endoflist = True
                        for s in OPEN:
                            if state.f < s.f:
                                OPEN.insert(OPEN.index(s), state)
                                endoflist = False
                                break
                        if endoflist:
                            OPEN.append(state)
                         #   elif:
                                #break ties
        return searchgrid[goal.posx][goal.posy]

    reached = False
    while not reached:
        OPEN = list()
        OPEN.append(start)
        goal.setg(INF)
        treenode = ComputePath()
        if not OPEN:
            print("The target is not reachable.")
            break
        path = list()
        counter = 0
        path.insert(0, treenode)
        while (treenode.posx != start.posx or treenode.posy != start.posy):
            path.insert(0, treenode.treepointer)
            treenode = treenode.treepointer
        for node in path:
            if grid[node.posx][node.posy] == BLOCKED:
                start = path[path.index(node) - 1]
                start = State(start.posx, start.posy, 0)
                naivegrid[node.posx][node.posy] = BLOCKED
                break
            else:
                naivegrid[node.posx][node.posy] = UNBLOCKED
                pos = Rectangle(Point(node.posx, node.posy), Point(node.posx + 1, node.posy + 1))
                pos.setFill("blue")
                pos.draw(win)
                if node.posx == goal.posx and node.posy == goal.posy:
                    print("Target reached.")
                    reached = True

    win.getMouse()
    win.close()
