import pygame

# Constates
life_player = 500
speed_player = 4
speed_animation = 0.3
barrier = [-60, 870]
damage = 50

class Caracter(pygame.sprite.Sprite):
    def __init__(self, SCREEN, position, skin): 
        super().__init__()
        self.SCREEN = SCREEN
        self.position = position
        self.skin = skin
        self.speed = speed_player
        self.life = life_player
        self.damage = damage
        self.loadSprites()
        self.current_sprite_load = 'Idle'
        self.current_sprite = 0
        self.flip = 'right'
        self.sprites = self.sprites_load[self.current_sprite_load]
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        
    def loadSprites(self):
        self.sprites_load = {
            'Idle': [],
            'Attacking': [],
            'Dying': [],
            'Hurt': [],
            'Taunt': [],
            'Walking': []
        }       
        type_sprites = [
            ['Idle', 12], # [Tipo, Total Imagens]
            ['Attacking', 12],
            ['Dying', 15],
            ['Hurt', 12],
            ['Taunt', 18],
            ['Walking', 18]]

        for type in type_sprites:
            for i in range(type[1]):
                img = pygame.image.load('assets/caracter/' + self.skin +'/'+ type[0] + '/' + self.skin + type[0] + str(i) + '.png').convert_alpha()
                w, h = 360, 245 
                img = pygame.transform.smoothscale( img, (w, h))
                self.sprites_load[type[0]].append(img)

    def update(self):
        if self.current_sprite_load != 'Dying' or self.current_sprite != len(self.sprites_load['Dying']):
            self.current_sprite += speed_animation

        if self.current_sprite >= len(self.sprites):
            if self.current_sprite_load in ['Attacking', 'Hurt']:
                self.idle()
            self.current_sprite = 0
            if self.current_sprite_load == 'Dying':
                self.current_sprite = 14

        self.image = pygame.transform.flip(self.sprites[int(self.current_sprite)].convert_alpha(), self.flip == 'left', False)

    def moveToLeft(self):
        if self.life == 0: return 0
        self.walking()
        if(self.rect.left >= barrier[0]):
            self.rect.left -= self.speed 
            self.flip = 'left'
    def moveToRight(self):
        if self.life == 0: return 0
        self.walking()
        if(self.rect.left <= barrier[1]):
            self.rect.left += self.speed 
            self.flip = 'right'

    def idle(self):
        if self.life == 0: return 0
        self.setCurrent_sprite_load('Idle')
    def taunt(self):
        if self.life == 0: return 0
        self.setCurrent_sprite_load('Taunt')
    def walking(self):
        if self.life == 0: return 0
        self.setCurrent_sprite_load('Walking')
    def attacking(self):
        if self.life == 0: return 0
        self.setCurrent_sprite_load('Attacking')
    def dying(self):
        self.setCurrent_sprite_load('Dying')
    def hurt(self, damage):
        self.life -= damage
        if self.life <= 0:
            self.life = 0
            self.dying()
        else:
            self.setCurrent_sprite_load('Hurt')
    def setCurrent_sprite_load(self, newCurrent_sprite_load):
        if newCurrent_sprite_load == self.current_sprite_load: 
            return 0
        self.current_sprite_load = newCurrent_sprite_load
        self.sprites = self.sprites_load[self.current_sprite_load]
        self.current_sprite = 0
    def getLife(self):
        return self.life