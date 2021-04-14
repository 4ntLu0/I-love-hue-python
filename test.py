import pygame
import sys

pygame.init()
window = pygame.display.set_mode((800,600))

rect = pygame.Rect(100,100, 50, 50)

pygame.draw.rect(window, (255,255,255), rect)

running = True
moving = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                moving = True

        elif event.type == pygame.MOUSEBUTTONUP:
            moving = False

        elif event.type == pygame.MOUSEMOTION and moving:
            rect.move_ip(event.rel)

    window.fill((0,0,0))
    pygame.draw.rect(window, (255,255,255), rect)
    pygame.display.update()

pygame.quit()