from graphics import *
import random

draw = False #set whether or not to draw the grid

#initialize RNG
random.seed(12346)

UNVISITED = 0
UNBLOCKED = 1
BLOCKED = 2

RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

#create array of values and draw grid
            
for g in range(50):
    filename = "%d.txt"%g
    file = open(filename, 'w')
    print(filename)
    #initialize grid
    if draw:
        win = GraphWin('Grid', 510, 510)
        win.setCoords(0.0, 0.0, 101.0, 101.0)
        win.setBackground("gray")
    grid = list()
    for x in range(101):
        grid.append(list())
        for y in range(101):
            grid[x].append(UNVISITED)

    unvisited = list()
    for x in range(101):
        for y in range(101):
            if grid[x][y] == UNVISITED:
                unvisited.append((x,y))
                
    while unvisited:
        posx, posy = random.choice(unvisited) #initialize at random point
        grid[posx][posy] = UNBLOCKED #mark point as unblocked
        unblocked = list()
        unblocked.append((posx,posy))
            
        prev = None #keep track of last move in order not to check that direction
        while unblocked:
            grid[posx][posy] = UNBLOCKED
            
            if draw:
                pos = Rectangle(Point(posx, posy), Point(posx + 1, posy + 1))
                pos.setFill("white")
                pos.draw(win)
            
            dirs = list() #possible directions to move 0=right, 1=left, 2=up, 3=down

            if (posx + 1 < 101) and prev != LEFT and (grid[posx + 1][posy] == UNVISITED): #check for walls and avoid backtracking
                dirs.append(RIGHT)

            if (posx - 1 > -1) and prev != RIGHT and (grid[posx - 1][posy] == UNVISITED):
                dirs.append(LEFT)
                       
            if (posy + 1 < 101) and prev != DOWN and (grid[posx][posy + 1] == UNVISITED):
                dirs.append(UP)
       
            if (posy - 1 > -1) and prev != UP and (grid[posx][posy - 1] == UNVISITED):
                dirs.append(DOWN)
            
            if not dirs: #check if directions are available
                posx, posy = unblocked.pop()
                prev = None 
            else: 
                pos = None
                blocked = None
                if random.randrange(0,10) < 3:
                    blocked = True
                else:
                    blocked = False 
                    unblocked.append((posx, posy))
                    prev = dir
                    
                dir = random.choice(dirs) #0=right, 1=left, 2=up, 3=down
                if dir == RIGHT:
                    if blocked:
                        grid[posx + 1][posy] = BLOCKED
                        if draw:
                            pos = Rectangle(Point(posx + 1, posy), Point(posx + 2, posy + 1))
                    else:                 
                        posx += 1
                        
                elif dir == LEFT:
                    if blocked:
                        grid[posx - 1][posy] = BLOCKED
                        if draw:
                            pos = Rectangle(Point(posx - 1, posy), Point(posx, posy + 1))
                    else:
                        posx -= 1
                        
                elif dir == UP:
                    if blocked:
                        grid[posx][posy + 1] = BLOCKED
                        if draw:
                            pos = Rectangle(Point(posx, posy + 1), Point(posx + 1, posy + 2))
                    else:
                        posy += 1
                
                else:
                    if blocked:
                        grid[posx][posy - 1] = BLOCKED
                        if draw:
                            pos = Rectangle(Point(posx, posy - 1), Point(posx + 1, posy))
                    else:
                        posy -= 1
                if blocked and draw: 
                    pos.setFill("black")
                    pos.draw(win)

            
        del unvisited
        unvisited = list()
        for x in range(101):
            for y in range(101):
                if grid[x][y] == UNVISITED:
                    unvisited.append((x,y))
    
    grid[0][0] = UNBLOCKED #set goal and start to be unblocked
    grid[100][100] = UNBLOCKED
    
    for row in grid:
        for val in row:
            file.write("%d" % val)
        file.write("\n")    
    file.close()   
   
    if draw:
        pos = Rectangle(Point(100, 100), Point(101, 101))
        pos.setFill("red")
        pos.draw(win)
        win.getMouse()
        win.close()
    
     

