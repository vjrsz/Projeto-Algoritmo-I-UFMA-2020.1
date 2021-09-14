import pygame

class Maps():
    def __init__(self, SCREEN, src):
        self.SCREEN = SCREEN
        self.map = pygame.image.load(src).convert_alpha()
        self.map = pygame.transform.smoothscale( self.map, SCREEN.get_size())
        
    def draw(self, position):
        self.SCREEN.blit(self.map, position)
    