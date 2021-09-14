import pygame
from caracter import Caracter
from maps import Maps
from resources import Colors
from resources import Fonts

# Constantes
position_in_screen = {
    'player1' : (0, 200),
    'player2' : (870, 200),
    'fps' :  [10, 680],
    'life1': [0, 11],
    'life2': [780, 11],
    'header' : [0, 0],
    'result': [290, 260],
}
gameFPS = 120
distanceAttack = 230

def updateFps(clock):
    fps = '  ' + str(int(clock.get_fps())) + '  '
    fps_text = Fonts(1).render(fps, 1, Colors('white'),  Colors('black'))
    return fps_text

def HUD(SCREEN, assets_HUD, player1, player2, upFps):
    header, lifePlayer1, lifePlayer2, victory, defeat = assets_HUD

    life1, life2 = player1.getLife(), player2.getLife()
    lifePlayer1 = pygame.transform.smoothscale( lifePlayer1, [life1, 43])
    lifePlayer2 = pygame.transform.smoothscale( lifePlayer2, [life2, 43])
    
    if life2 == 0: 
        SCREEN.blit (victory, position_in_screen['result'])
    elif life1 == 0:
        SCREEN.blit (defeat, position_in_screen['result'])

    SCREEN.blit (header, position_in_screen['header'])
    SCREEN.blit (lifePlayer1, position_in_screen['life1'])
    SCREEN.blit (lifePlayer2, position_in_screen['life2'])

    SCREEN.blit(upFps, position_in_screen['fps']) # FPS

def attackColide(send_attack, receive_attack):
    colide = pygame.sprite.collide_mask(send_attack, receive_attack)
    if colide != None:
        if colide[0] <= distanceAttack and ((send_attack.flip == 'right' and receive_attack.flip == 'left' ) or (send_attack.flip == 'left' and receive_attack.flip == 'right')):
            receive_attack.hurt(send_attack.damage)

def draw(SCREEN, maps, moving_sprites, assets_HUD,  player1, player2, upFps):
    maps.draw([0,0])
    moving_sprites.draw(SCREEN)
    moving_sprites.update()
    HUD(SCREEN, assets_HUD, player1, player2, upFps)
    
def events(keys_pressed, player1, player2):
    functions_key = {
        'a' : player1.moveToLeft,
        'd' : player1.moveToRight,
        'f' : player1.attacking,
        'e' : player1.taunt,
        'j' : player2.moveToLeft,
        'l' : player2.moveToRight,
        'p' : player2.attacking,
        'o' : player2.taunt,
    }

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            for chave, valor in functions_key.items():
                if pygame.key.name(event.key) == chave:
                    keys_pressed.append(event.key)
            # Retorna menu
            if event.key == pygame.K_RETURN and (player1.getLife() == 0 or  player2.getLife() == 0):
                return False
        if event.type == pygame.KEYUP:
            if event.key in keys_pressed:
                keys_pressed.remove(event.key)
        if event.type == pygame.QUIT:
            pygame.quit()

    for player_a in [player1, player2]:
        if player_a.getLife() == 0:
            for player_b in [player1, player2]:
                if player_a != player_b: player_b.taunt()
        elif not player_a.current_sprite_load in ['Attacking', 'Dying'] :
            if len(keys_pressed) == 0:
                player_a.idle()
            else: 
                for key in keys_pressed:
                    functions_key[pygame.key.name(key)]()
        elif player_a.current_sprite > 11 and not player_a.current_sprite_load in ['Taunt', 'Dying']:
            for player_b in [player1, player2]:
                if player_a != player_b: attackColide(player_a, player_b)
    
    return True

def initalizeVariables(SCREEN, dataGame):
    player1 = Caracter(SCREEN, position_in_screen['player1'], 'Minotaur01')
    player2 = Caracter(SCREEN, position_in_screen['player2'], 'Minotaur02')
    player2.flip = 'left'

    assets_HUD = [
        pygame.image.load("assets/hud/Header.png").convert_alpha(),
        pygame.image.load("assets/hud/life.bmp").convert_alpha(),
        pygame.image.load("assets/hud/life.bmp").convert_alpha(),
        pygame.image.load("assets/hud/victory.png").convert_alpha(),
        pygame.image.load("assets/hud/defeat.png").convert_alpha()
    ]

    moving_sprites = pygame.sprite.Group()
    moving_sprites.add(player1)
    moving_sprites.add(player2)
    
    return pygame.time.Clock(), Maps(SCREEN, 'assets/backgrounds/gamebackground'+str(dataGame[0])+'/gamebackground.png'), player1, player2, moving_sprites, [], assets_HUD

def run(SCREEN, dataGame):
    clock, maps, player1, player2, moving_sprites, keys_pressed, assets_HUD = initalizeVariables(SCREEN, dataGame)

    while True:
        if not events(keys_pressed, player1, player2): return True

        draw(SCREEN, maps, moving_sprites, assets_HUD,  player1, player2, updateFps(clock))

        clock.tick(gameFPS)
        pygame.display.flip()