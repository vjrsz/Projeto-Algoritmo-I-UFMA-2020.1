import pygame

def Colors(cor):
    colors = {
        'white': [255, 255, 255],
        'red': [255, 10, 10],
        'redS': [190, 50, 50],
        'green': [0, 255, 0],
        'black': [0, 0, 0],
        'gray' : [225, 225, 225],
    }
    return colors[cor]
        
def Fonts(num):
    font = [
        pygame.font.Font('assets/font/pixelart.ttf', 72),
        pygame.font.Font('assets/font/pixelart.ttf', 32)
    ]
    return font[num]