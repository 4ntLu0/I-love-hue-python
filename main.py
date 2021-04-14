import pygame
import msvcrt
import sys
import random
import time

# TODO: change to billinear smoothed generation
# TODO: change to array[x][y] instead of array[y][x] (for simplicity)
# TODO: draw each rectangle as an individual rectangle. (maybe an array?)


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

    time.sleep(1)

    for i in range(0, y_step):
        for j in range(0, x_step):
            # we are now going through each step left to right for each row.
            x = x_block * j
            y = y_block * i
            pygame.draw.rect(myscreen, newGrid[i][j], (x, y, x_block, y_block), 0)
            pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit();


def shuffleBoardyx(grid, x_step, y_step, constants):
    """
    shuffles a board using a board which is y-x bound.
    """
    templist = []
    print(constants)
    for y in range(0, y_step):
        for x in range(0, x_step):
            # we will ignore i/j if they are in our constants.
            if (x,y) in constants:
                continue
            else:
                templist.append(grid[y][x])

    random.shuffle(templist)

    newGrid = []
    count = 0
    for y in range(0, y_step):
        shuffleList = []
        for x in range(0, x_step):
            if (x,y) in constants:
                shuffleList.append(grid[y][x])
            else:
                shuffleList.append(templist[count])
                count += 1
        newGrid.append(shuffleList)

    return newGrid

def generateSmoothBoard(window, colours, colours_size=(2,2), targetRect=pygame.Rect(0,0,400,400)):
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

    colour_rect = pygame.Surface(colours_size) # x by y bitmap
    for i in colours:
        pygame.draw.line(colour_rect, i[0], i[1], i[1])
    colour_rect = pygame.transform.smoothscale(colour_rect, (targetRect.width, targetRect.height))
    window.blit(colour_rect, targetRect)
    pygame.display.update()


if __name__ == "__main__":
    pygame.init()

    windowSize = (400, 400)

    # common sizes for 1200x900
    # 300x300:  x=4     y=3
    # 150x150:  x=8     y=6
    # 100x100:  x=12    y=9
    # 75x75:    x=16    y=12
    # 60x60:    x=20    y=15
    # 50x50:    x=24    y=18

    # for 900x900, 9, 6, 3
    x_step = 8
    y_step = 8

    # use 4 random colours for now
    c1, c2, c3, c4 = ((33, 11, 84), (201, 205, 242), (201, 255, 249), (6, 39, 69))
    # c1 = (255, 0, 0)
    # c2 = (0, 255, 0)
    # c3 = (0, 0, 255)
    # c4 = (150, 150, 150)

    # constants are blocks that won't move.
    constants = []

    # general block
    constants.append((0,0))
    constants.append((x_step-1,y_step-1))
    constants.append((0,y_step-1))
    constants.append((x_step-1,0))

    # center block
    constants.append((((x_step-1)/2),((y_step-1)/2)))

    # 7x7 block
    # constants.append((0, 0))
    # constants.append((6, 6))
    # constants.append((0, 6))
    # constants.append((6, 0))
    # constants.append((3, 3))

    # createColourGridyx(windowSize, c1, c2, c3, c4, x_step, y_step, constants)

    testWindow = pygame.display.set_mode(windowSize)
    pygame.display.set_caption("test_window")
    colours = []
    colours.append([(33,11,84),(0,0)])
    colours.append([(201,205,242), (0,1)])
    colours.append([(201,255,240), (1,1)])
    colours.append([(6,39,69),(1,0)])

    colours_size = (2,2)

    generateSmoothBoard(testWindow, colours, colours_size, pygame.Rect(0,0,400,400))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit();