import random
import pygame
from caracter import Caracter
from maps import Maps

def draw(SCREEN,  moving_sprites, bg_menu, text_menu, option_selected):
    # Animação de background fundo
    for bg in bg_menu:
        bg[0].draw(bg[1])

    #Animação do player de fundo
    moving_sprites.draw(SCREEN)
    moving_sprites.update()

    # Menu principal
    SCREEN.blit(text_menu[0], [390, 110])
    SCREEN.blit(text_menu[option_selected], [390, 110])

def menuImage(menu_actual):
    if(menu_actual == 0): #menu inicial
        return[
            pygame.image.load("assets/menu/menu0.png").convert_alpha(),
            pygame.image.load("assets/menu/start.png").convert_alpha(),
            pygame.image.load("assets/menu/comojogar.png").convert_alpha(),
            pygame.image.load("assets/menu/exit.png").convert_alpha(), 
        ], 4
    if(menu_actual == 1): #menu de mapa
        return [
            pygame.image.load("assets/menu/menu1.png").convert_alpha(),
            pygame.image.load("assets/menu/map1.png").convert_alpha(),
            pygame.image.load("assets/menu/map2.png").convert_alpha(),
            pygame.image.load("assets/menu/map3.png").convert_alpha(),
            pygame.image.load("assets/menu/map4.png").convert_alpha(), 
        ], 5
def initializeVariables(SCREEN):
    # Imagens de fundo do menu
    numBg = random.randrange(1, 8)
    if (numBg > 4): numBg -= 4
    numBg = str(numBg)

    bg_menu = [
        [Maps(SCREEN, "assets/backgrounds/gamebackground"+numBg+"/backland.png"),[0,0], 2],
        [Maps(SCREEN, "assets/backgrounds/gamebackground"+numBg+"/backland.png"),[1280,0], 2],
        [Maps(SCREEN, "assets/backgrounds/gamebackground"+numBg+"/menuBg.png"),[0,0], 5],
        [Maps(SCREEN, "assets/backgrounds/gamebackground"+numBg+"/menuBg.png"),[1280,0], 5],
    ]

    text_menu, limit_options= menuImage(0)

    #animação do player de fundo
    anim_player = Caracter(SCREEN, (0, 200), 'Minotaur01')
    anim_player.walking()
    anim_player.speed_animation = 0.5
    moving_sprites = pygame.sprite.Group()
    moving_sprites.add(anim_player)

    return moving_sprites, bg_menu, text_menu, 1, 0, limit_options, []
    
def menu(SCREEN):
    moving_sprites, bg_menu, text_menu, option_selected, menu_actual, limit_options, data_game = initializeVariables(SCREEN) 
    
    while True: 
        #atualiza Animação background
        for bg in bg_menu:
            if bg[1][0]  <= -1280:
                bg[1][0] = 1280
            else:
                bg[1][0] -= bg[2]

        draw(SCREEN, moving_sprites, bg_menu, text_menu, option_selected)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN :
                    if option_selected == limit_options-1:
                        option_selected = 0
                    option_selected += 1
                if event.key == pygame.K_UP :
                    if option_selected == 1:
                        option_selected = limit_options
                    option_selected -= 1
                if event.key == pygame.K_RETURN :
                    if menu_actual == 0: #menu inicial
                        if option_selected == 1:
                            menu_actual = 1
                            text_menu, limit_options = menuImage(menu_actual)
                        if option_selected == 2:
                            option_selected = 1
                        if option_selected == 3:
                            pygame.quit()
                            option_selected = 1
                    elif menu_actual == 1: #menu de mapa
                        data_game.append(option_selected)
                        option_selected = 1
                        return data_game
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.flip()