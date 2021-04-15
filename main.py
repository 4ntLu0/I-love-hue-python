import pygame
import msvcrt
import sys
import random
import time


# TODO: add circles for constant rectangles
# TODO: add swapping functions.

# DONE: change to billinear smoothed generation
# DONE: change to array[x][y] instead of array[y][x] (for simplicity)
# DONE: draw each rectangle as an individual rectangle. (maybe an array?)

class MyRect:
    rect = ""
    colour = 0, 0, 0
    moving = False
    moving_colour = 0, 0, 0
    originals = 0, 0, 0, 0
    location = 0, 0, 0, 0
    has_moved = False

    def __init__(self, rect, colour, moving=False):
        self.rect = rect
        self.colour = colour
        self.moving = False
        self.originals = rect.left, rect.top, rect.width, rect.height
        self.location = self.rect.left, self.rect.top, self.rect.width, self.rect.height

    def set_moving(self):
        self.moving = True

    def stop_moving(self):
        self.moving = False

    def get_rect(self):
        return self.rect

    def get_col(self, bypass=False):
        if bypass:
            return self.colour
        elif self.moving:
            return self.moving_colour
        else:
            return self.colour

    def set_rect(self, rect):
        self.rect = rect

    def set_col(self, colour):
        self.colour = colour

    def selfblit(self, win_size, window):
        surface = pygame.Surface(win_size)
        pygame.draw.rect(surface, self.colour, self.rect)
        pygame.Surface.blit(surface, window, self.rect)

    def reset_originals(self):
        self.rect = pygame.Rect(self.originals)

    def set_location(self, locations):
        self.location = locations
        self.rect = pygame.Rect(self.location)

    def get_location(self):
        return self.location

class Grid:
    """
    This class should contain the entire grid. It will contain rgb values and positions of rects.
    """

    # recall that grids are [x][y] arrays of RGB TRIOS only.
    # rectgrids are paired as rectangles of colour and location.
    def __init__(self, grid):
        self.original_grid = grid
        self.shuffle_grid = grid
        self.rect_grid = None

    def setShuffleGrid(self, shuffleGrid):
        self.shuffle_grid = shuffleGrid

    def checkGrids(self):
        if self.original_grid==self.shuffle_grid:
            return True
        else:
            return False

    def setRectGrid(self, rectGrid):
        self.rect_grid = rectGrid

def generateSteps(c1, c2, numSteps):
    """
    creates a list of colours that fade from c1 to c2.
    should be a linear map
    :param c1: rgb tuple (#,#,#) of first colour
    :param c2: rgb tuple (#,#,#) of second colour
    :param numSteps: int of steps between
    :return:
    """
    # starting from c1
    strip = [c1]  # the strip of colour

    # rgb values of difference
    colourDiff = [c1[0] - c2[0], c1[1] - c2[1], c1[2] - c2[2]]

    # defines steps for red/green/blue
    rStep = (colourDiff[0] / (numSteps - 1))
    gStep = (colourDiff[1] / (numSteps - 1))
    bStep = (colourDiff[2] / (numSteps - 1))

    for i in range(1, numSteps):
        strip.append((c1[0] - rStep * i, c1[1] - gStep * i, c1[2] - bStep * i))

    # ending on c2
    strip.append(c2)

    return strip


def createColourGridyx(windowSize, c1, c2, c3, c4, x_step, y_step, constants):
    """
    creates a Y-X bound colour grid using custom interpolation.
    """
    myscreen = pygame.display.set_mode(windowSize)

    # determines the sizes of each block.
    # TODO: for our game, we want to maintain these as S Q U A R E S
    x_block = windowSize[0] / x_step
    y_block = windowSize[1] / y_step

    colourGrid = []
    # recall draw_rect uses x,y sizes and top_left corner.

    # TODO: we want to be able to use bilinear extrapolation an N number of points on an ixj grid using pygame.transform.smoothscale
    # NOTE: see test.py

    # generate linear mappings along two vertical columns
    leftColumn = generateSteps(c1, c4, y_step)
    rightColumn = generateSteps(c2, c3, y_step)

    # TODO: remake grid with [x][y] (full rehaul recode).
    # iterating
    for i in range(0, y_step):
        # this now generates across
        # this should append an entire list, so you get [[],[],[]] on each y level 0->y_step and 0->x_step
        colourGrid.append(generateSteps(leftColumn[i], rightColumn[i], x_step))

    oriGrid = colourGrid  # this is extraneous but we're doing it just to be sure

    # colourArray should now be filled with rgb values.
    # colourArray should have the same number of x_steps and y_steps.

    # newGrid = shuffleBoard(oriGrid, x_step, y_step, constants)
    newGrid = oriGrid

    for i in range(0, y_step):
        for j in range(0, x_step):
            # we are now going through each step left to right for each row.
            x = x_block * j
            y = y_block * i
            pygame.draw.rect(myscreen, colourGrid[i][j], (x, y, x_block, y_block), 0)
            pygame.display.update()

    for i in range(0, y_step):
        for j in range(0, x_step):
            # we are now going through each step left to right for each row.
            x = x_block * j
            y = y_block * i
            pygame.draw.rect(myscreen, newGrid[i][j], (x, y, x_block, y_block), 0)
            pygame.display.update()


def shuffleBoardyx(grid, x_step, y_step, constants):
    """
    shuffles a board using a board which is y-x bound.
    """
    templist = []
    print(constants)
    for y in range(0, y_step):
        for x in range(0, x_step):
            # we will ignore i/j if they are in our constants.
            if (x, y) in constants:
                continue
            else:
                templist.append(grid[y][x])

    random.shuffle(templist)

    newGrid = []
    count = 0
    for y in range(0, y_step):
        shuffleList = []
        for x in range(0, x_step):
            if (x, y) in constants:
                shuffleList.append(grid[y][x])
            else:
                shuffleList.append(templist[count])
                count += 1
        newGrid.append(shuffleList)

    return newGrid


def shuffleBoardxy(grid, steps, constants, bypass=False):
    # if you want to bypass grid shuffling
    if bypass:
        return grid

    x_step, y_step = steps
    templist = []
    for x in range(0, x_step):
        for y in range(0, y_step):
            if (x, y) in constants:
                continue
            else:
                templist.append(grid[x][y])

    random.shuffle(templist)

    shuffle_grid = []
    count = 0
    for x in range(0, x_step):
        shuffleList = []
        for y in range(0, y_step):
            if (x, y) in constants:
                shuffleList.append(grid[x][y])
            else:
                shuffleList.append(templist[count])
                count += 1
        shuffle_grid.append(shuffleList)

    return shuffle_grid


def generateSmoothBoard(window, colours, colours_size=(2, 2), targetRect=pygame.Rect(0, 0, 400, 400)):
    """
    colours is going to be a LIST of lists defined in this way:
        [[colour, location], [colour, location]]
        [[(rr,gg,bb), (x_step, y_step)], [(rr,gg,bb), (x_step, y_step)]]
        where rrggbb are rgb values and x_step and y_step or the location given a typical 0,0 start
          0 1 2 3 4 5 6 7 8 9
        0 . . . . . . . . . .
        1 . . . . . . . . . .
        2 . . . . . . . . . .
        3 . . . . . . . . . .
        4 . . . . . . . . . .
        5 . . . . . . . . . .
        6 . . . . . . . . . .
        7 . . . . . . . . . .
        8 . . . . . . . . . .
        9 . . . . . . . . . .
    x_size, y_size denote the x/y sizes of the board. Default is 2x2
        THESE MUST MATCH WITH THE COLOUR SIZING
    targetRect is a rect of same size as window.
    """
    # TODO: allow dynamic assignment of target rect

    colour_rect = pygame.Surface(colours_size)  # x by y bitmap
    for i in colours:
        pygame.draw.line(colour_rect, i[0], i[1], i[1])
    colour_rect = pygame.transform.smoothscale(colour_rect, (targetRect.width, targetRect.height))
    window.blit(colour_rect, targetRect)
    pygame.display.update()


def getColours(window, win_size, steps):
    grid = []
    x_size, y_size = win_size
    x_step, y_step = steps

    x_loc_scalar = x_size / x_step
    y_loc_scalar = y_size / y_step

    for x in range(0, x_step):
        templist = []
        for y in range(0, y_step):
            templist.append(pygame.Surface.get_at(window, (int(x * x_loc_scalar), int(y * y_loc_scalar))))
        grid.append(templist)
    return grid


def gridToRects(win_size, steps, grid):
    # note: do we need window?
    rects = []
    x_size, y_size = win_size
    x_step, y_step = steps

    x_loc_scalar = x_size / x_step
    y_loc_scalar = y_size / y_step

    # rects contains RECTANGLE and then COLOUR
    for x in range(0, x_step):
        for y in range(0, y_step):
            rect = pygame.Rect(x * x_loc_scalar, y * y_loc_scalar, x_loc_scalar, y_loc_scalar)
            rects.append(MyRect(rect, grid[x][y]))

    return rects


def drawGridLoose(window, win_size, steps, grid):
    x_size, y_size = win_size
    x_step, y_step = steps

    x_loc_scalar = x_size / x_step
    y_loc_scalar = y_size / y_step

    for x in range(0, x_step):
        for y in range(0, y_step):
            pygame.draw.rect(window, grid[x][y], (x * x_loc_scalar, y * y_loc_scalar, x_loc_scalar, y_loc_scalar))
    pygame.display.update()


def drawFromRects(window, rects):
    for i in rects:
        pygame.draw.rect(window, i.get_col(), i.rect)


def drawRect(window, i):
    pygame.draw.rect(window, i.get_col(True), i.rect)


def drawBlank(window, locs):
    rect = pygame.Rect(locs)
    pygame.draw.rect(window, (0, 0, 0), rect)


def checkWin(grid, window, win_size, steps):
    curr_grid = getColours(window, win_size, steps)
    if curr_grid == grid:
        return True
    else:
        return False

def ilovehue():
    debug = False
    window_size = (400, 400)

    # common sizes for 1200x900
    # 300x300:  x=4     y=3
    # 150x150:  x=8     y=6
    # 100x100:  x=12    y=9
    # 75x75:    x=16    y=12
    # 60x60:    x=20    y=15
    # 50x50:    x=24    y=18

    # for 900x900, 9, 6, 3
    steps = 4, 4
    x_step, y_step = steps

    # use 4 random colours for now
    c1, c2, c3, c4 = ((33, 11, 84), (201, 205, 242), (201, 255, 249), (6, 39, 69))
    # c1 = (255, 0, 0)
    # c2 = (0, 255, 0)
    # c3 = (0, 0, 255)
    # c4 = (150, 150, 150)

    # constants are blocks that won't move.
    constants = []

    # general block
    constants.append((0, 0))
    constants.append((x_step - 1, y_step - 1))
    constants.append((0, y_step - 1))
    constants.append((x_step - 1, 0))

    # center block
    constants.append((((x_step - 1) / 2), ((y_step - 1) / 2)))

    # 7x7 block
    # constants.append((0, 0))
    # constants.append((6, 6))
    # constants.append((0, 6))
    # constants.append((6, 0))
    # constants.append((3, 3))

    # createColourGridyx(windowSize, c1, c2, c3, c4, x_step, y_step, constants)

    testWindow = pygame.display.set_mode(window_size)
    pygame.display.set_caption("test_window")
    colours = []
    # set 1
    colours.append([(255, 153, 51),(1,1)])
    colours.append([(153, 51, 255),(0,1)])
    colours.append([(51, 153, 255),(0,0)])
    colours.append([(51, 255, 153),(1,0)])

    # set 2
    # colours.append([(33, 11, 84), (0, 0)])
    # colours.append([(201, 205, 242), (0, 1)])
    # colours.append([(201, 255, 240), (1, 1)])
    # colours.append([(6, 39, 69), (1, 0)])


    # colours.append([(240,230,140),(1,0)])
    # colours.append([(129,0,0), (1,1)])

    colours_size = (2, 2)

    generateSmoothBoard(testWindow, colours, colours_size, pygame.Rect(0, 0, 400, 400))
    grid = getColours(testWindow, window_size, steps)

    game_grid = Grid(grid) # extra but we will keep for now

    drawGridLoose(testWindow, window_size, steps, grid)
    time.sleep(1)
    shufflegrid = shuffleBoardxy(grid=grid, steps=steps, constants=constants)

    game_grid.setShuffleGrid(shufflegrid)

    rects = gridToRects(window_size, steps, game_grid.shuffle_grid)

    game_grid.setRectGrid(rects)

    drawFromRects(testWindow, rects)
    pygame.display.update()
    # drawGridLoose(shuffleWindow, window_size, steps, shufflegrid)

    tempcol = 0, 0, 0, 0
    moving = False
    locations = 0, 0, 0, 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit();

            if event.type == pygame.MOUSEBUTTONDOWN:
                # there needs to be a class here to activate each rectangles movement
                for i in rects:
                    if i.rect.collidepoint(event.pos):
                        i.moving = True
                        i.has_moved = True
                        tempcol = i.colour

            if event.type == pygame.MOUSEBUTTONUP:
                if debug: print("mouseup")
                for i in rects:
                    i.moving = False
                    i.reset_originals()
                    if i.rect.collidepoint(event.pos):
                        # swap currentRect and i.
                        swapcol = i.colour
                        # print(swapcol)
                        if debug: print(tempcol)
                        i.set_col(tempcol)

                        for j in rects:
                            if j.has_moved:
                                j.colour = swapcol
                                j.has_moved = False

                drawFromRects(testWindow, rects)

            if event.type == pygame.MOUSEMOTION:
                for i in rects:
                    if i.moving:
                        i.rect.move_ip(event.rel)

                        drawFromRects(testWindow, rects)

                        # until i figure out a better solution, we have to draw two rects.
                        # TODO: add a way to add a blank
                        drawRect(testWindow, i)

            if checkWin(grid, testWindow, window_size, steps):
                print("you have won")
                drawGridLoose(testWindow, window_size, steps, grid)
                pygame.display.update()
                running = False
        pygame.display.update()


if __name__ == "__main__":
    pygame.init()

    ilovehue()
