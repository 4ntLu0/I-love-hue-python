import sys
import random
import pygame

# Window size
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

### initialisation
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gradient Rect")


def gradientRect(window, topleft_colour, topright_colour, bottomright_colour, bottomleft_colour, target_rect):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface((2, 2))  # tiny! 2x2 bitmap
    pygame.draw.line(colour_rect, bottomleft_colour, (0, 0), (0, 0))  # left colour line
    pygame.draw.line(colour_rect, topright_colour, (1, 1), (1, 1))
    pygame.draw.line(colour_rect, bottomright_colour, (1, 0), (1, 0))
    pygame.draw.line(colour_rect, topleft_colour, (0, 1), (0, 1))
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))  # stretch!
    window.blit(colour_rect, target_rect)  # paint it


def getColours():
    x = 0
    list = []
    for j in range(0, 399, 50):
        for i in range(0, 399, 50):
            list.insert(x, pygame.Surface.get_at(window, (j, i)))
            x = x + 1
    return list


def shuffle(list):
    random.shuffle(list)
    shuffled = list
    return list


def draw(xd):
    x = 0
    for j in range(0, 399, 50):
        for i in range(0, 399, 50):
            pygame.draw.rect(window, xd[x], (j, i, 50, 50))
            x = x + 1

# Update the window
# window.fill((0,0,0))
gradientRect(window, (33, 11, 84), (201, 205, 242), (201, 255, 249), (6, 39, 69), pygame.Rect(0, 0, 400, 400))
# pygame.display.flip() #this is what displays the colours

boop = getColours()
for x in range(0, 1):
    shuffled = shuffle(getColours())
    # draw(shuffled)
    draw(boop)
pygame.display.update()


### Main Loop
game_over = False
while not game_over:

    # Handle user-input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    '''
    boop = getColours()
    random.shuffle(boop)
    shuffled = boop
    draw(shuffled)
    pygame.display.flip()
    '''
