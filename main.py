import pygame
from play import run
from menus import menu

ScreenWidth = 1280
ScreenHeight = 720 

pygame.init()
SCREEN = pygame.display.set_mode([ScreenWidth, ScreenHeight])
pygame.display.set_caption('Momoca')

while True:
    dataGame = menu(SCREEN)
    run(SCREEN, dataGame)


