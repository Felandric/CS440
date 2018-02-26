from graphics import *
import random
import time
from binary_heap import *

draw = True #set whether or not to draw the grid

UNVISITED = 0
UNBLOCKED = 1
BLOCKED = 2

INF = -1

RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

class State:
    def __init__(self, posx, posy, g):
        self.posx = posx
        self.posy = posy
        self.g = g
        self.h = 0
        if g == INF:
            self.f = INF
        else:
            self.f = g + self.h
        self.treepointer = None

    def __lt__(self, other):
        if self.f != other.f:
            return self.f < other.f
        elif self.f == other.f:
            if self.g != other.g:
                return self.g > other.g
            else:
                if random.randrange(0,2) == 0:
                    return True
                else:
                    return False    
    
    def setg(self, g):
        self.g = g
        if g == INF:
            self.f = INF
        else:
            self.f = g + self.h
            
    def seth(self, startx, starty):
        self.h = abs(self.posx - startx) + abs(self.posy - starty)
        if self.g == INF:
            self.f = INF
        else:
            self.f = self.g + self.h

results = open("rba_results.txt", 'w')
results.write("\tTime (s)\tReached Target\n")            
            
for gd in range(50):
    filename = "%d.txt"%gd
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
    for x in range(101):
        searchgrid.append(list())
        for y in range(101):
            searchgrid[x].append(None)
            
    OPEN = MinBinaryHeap()
    COST = 1
    start = State(0, 0, INF) #initialize at 0, 0, overwrite blocked if blocked, goal is 100, 100
    goal = State(100, 100, 0)

    if draw:
        pos = Rectangle(Point(goal.posx, goal.posy), Point(goal.posx + 1, goal.posy + 1))
        pos.setFill("red")
        pos.draw(win)

    def ComputePath():
        for x in range(101):
            for y in range(101):
                searchgrid[x][y] = None

        searchgrid[start.posx][start.posy] = start
        while OPEN and (start.g == INF or start.g > OPEN.peek().f):
            current = OPEN.pop()
            succs = list()
            if current.posx + 1 < 101 and (current.treepointer == None or current.treepointer.posx != current.posx + 1) and naivegrid[current.posx + 1][current.posy] != BLOCKED: #check all possible moves without backtracking, hitting walls, or going to blocked paths
                if searchgrid[current.posx + 1][current.posy] == None:
                    searchgrid[current.posx + 1][current.posy] = State(current.posx + 1, current.posy, INF)
                    searchgrid[current.posx + 1][current.posy].seth(start.posx, start.posy)
                succs.append(searchgrid[current.posx + 1][current.posy])

            if current.posx - 1 > -1 and (current.treepointer == None or current.treepointer.posx != current.posx - 1) and naivegrid[current.posx - 1][current.posy] != BLOCKED:
                if searchgrid[current.posx - 1][current.posy] == None:
                    searchgrid[current.posx - 1][current.posy] = State(current.posx - 1, current.posy, INF)
                    searchgrid[current.posx - 1][current.posy].seth(start.posx, start.posy)
                succs.append(searchgrid[current.posx - 1][current.posy])

            if current.posy + 1 < 101 and (current.treepointer == None or current.treepointer.posy != current.posy + 1) and naivegrid[current.posx][current.posy + 1] != BLOCKED:
                if searchgrid[current.posx][current.posy + 1] == None:
                    searchgrid[current.posx][current.posy + 1] = State(current.posx, current.posy + 1, INF)
                    searchgrid[current.posx][current.posy + 1].seth(start.posx, start.posy)
                succs.append(searchgrid[current.posx][current.posy + 1])

            if current.posy - 1 > -1 and (current.treepointer == None or current.treepointer.posy != current.posy - 1) and naivegrid[current.posx][current.posy - 1] != BLOCKED:
                if searchgrid[current.posx][current.posy - 1] == None:
                    searchgrid[current.posx][current.posy - 1] = State(current.posx, current.posy - 1, INF)
                    searchgrid[current.posx][current.posy - 1].seth(start.posx, start.posy)
                succs.append(searchgrid[current.posx][current.posy - 1])

            for state in succs:
                if state.g == INF or state.g > current.g + COST:
                    state.setg(current.g + COST)
                    state.treepointer = current
                    OPEN.add(state)

        return searchgrid[start.posx][start.posy]

    reached = False
    starttime = time.time()
    while not reached:
        OPEN = MinBinaryHeap()
        OPEN.add(goal)
        goal.seth(start.posx, start.posy)
        treenode = ComputePath()
        if not OPEN:
            print("The target is not reachable.")
            break
        path = list()
        path.insert(0, treenode)
        while (treenode.posx != goal.posx or treenode.posy != goal.posy):
            path.append(treenode.treepointer)
            treenode = treenode.treepointer
        for node in path:
            if grid[node.posx][node.posy] == BLOCKED:
                start = path[path.index(node) - 1]
                start = State(start.posx, start.posy, INF)
                naivegrid[node.posx][node.posy] = BLOCKED
                break
            else:
                naivegrid[node.posx][node.posy] = UNBLOCKED
                if draw:
                    pos = Rectangle(Point(node.posx, node.posy), Point(node.posx + 1, node.posy + 1))
                    pos.setFill("blue")
                    pos.draw(win)
                if node.posx == goal.posx and node.posy == goal.posy:
                    print("Target reached.")
                    reached = True
    endtime = time.time()
    if reached:
        rstring = "yes"
    else:
        rstring = "no"
    
    results.write("%d:\t%f\t%s\n"%(gd,(endtime-starttime), rstring))
    
    if draw:
        win.getMouse()
        win.close()

results.close()