# File created by: Liam Newberry, Auden Silcock, Taran Egenolf, Alejandro Madero
# Internal imports
from settings import *
# External imports
import pygame as pg

class Background:
    def __init__(self,game):
        self.game = game
        self.image = pg.image.load(BACKGROUND_IMG).convert_alpha()
        self.rect = self.image.get_rect()
    def draw(self):
        self.game.screen.blit(self.image,self.rect)

class Player:
    def __init__(self,game):
        self.game = game
        self.image = pg.image.load(PLAYER_IMG).convert()
        self.image.set_colorkey(COLORKEY)
        self.sound = pg.mixer.Sound(PLAYER_SOUND)
        self.rect = PLAYER_RECT
        self.vel = [0,0]
        self.on_platform = False
    def update(self):
        self.vel[1] = round(self.vel[1],4)
        self.rect[1] = round(self.rect[1],4)

        self.on_platform = self.check_platforms_vert()
        self.check_platforms_hori()
        self.check_snakes()
        self.check_rocks()
        self.check_jump_pads()

        if self.on_platform:
            self.get_input()
        else:
            self.vel[1] += GRAVITY

        if self.vel[1] > PLAYER_MAX_YVEL:
            self.vel[1] = PLAYER_MAX_YVEL

        self.rect[0] += self.vel[0]
        self.rect[1] += self.vel[1]
    def draw(self):
        self.game.screen.blit(self.image,self.rect)
    def check_platforms_vert(self):
        for platform in self.game.platforms:
            if x_collides(self.rect,platform.rect):
                if (self.rect[1] + self.rect[3] <= platform.rect[1] and
                    round(self.rect[1] + self.rect[3] + self.vel[1]) >= platform.rect[1]):
                    self.rect[1] = platform.rect[1] - self.rect[3]
                    self.vel[1] = 0
                    return True
                elif (self.rect[1] >= platform.rect[1] + platform.rect[3] and
                      self.rect[1] + self.vel[1] <= platform.rect[1] + platform.rect[3]):
                    self.die()
                    return False
        return False
    def check_platforms_hori(self):
        for platform in self.game.platforms:
            if y_collides(self.rect,platform.rect):
                if (self.rect[0] + self.rect[2] <= platform.rect[0] and
                    round(self.rect[0] + self.rect[2] - self.game.vel[0]) >= platform.rect[0]):
                    self.die()
    def check_snakes(self):
        for snakes in self.game.snakes:
            if collides(self.rect,snakes.rect):
                self.die()
    def check_rocks(self):
        for rock in self.game.rocks:
            if collides(self.rect,rock.hitbox):
                self.die()
    def check_jump_pads(self):
        for pad in self.game.jump_pads:
            if collides(self.rect,pad.hitbox):
                self.vel[1] = 2 * PLAYER_JUMP_VEL
                pg.mixer.Sound.play(pad.sound)
    def get_input(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_UP] or keystate[pg.K_SPACE]:
            self.vel[1] += PLAYER_JUMP_VEL
    def die(self):
        pg.mixer.Sound.play(self.sound)
        pg.mixer.music.set_volume(0)
        self.rect[1] = 1000
        self.game.vel[0] = 0
        self.game.tod = self.game.now
        self.game.dead = True

class Platform:
    def __init__(self,game,coords:list):
        self.game = game
        self.image = pg.image.load(PLATFORM_IMG).convert_alpha()
        self.rect = coords + PLATFORM_SIZE
    def update(self):
        self.rect[0] += self.game.vel[0]
        self.rect[1] += self.game.vel[1]
    def draw(self):
        self.game.screen.blit(self.image,self.rect)

class Block(Platform):
    def __init__(self, game,coords:list):
        super().__init__(game,coords)
        self.rect[2] = BLOCK_SIZE[0]
        self.rect[3] = BLOCK_SIZE[1]

class Log(Block):
    def __init__(self,game,coords:list):
        super().__init__(game,coords)
        self.image = pg.image.load(LOG_IMG).convert_alpha()

class Bush(Block):
    def __init__(self,game,coords:list):
        super().__init__(game,coords)
        self.image = pg.image.load(BUSH_IMG).convert_alpha()

class Snakes(Platform):
    def __init__(self,game,coords:list):
        super().__init__(game,coords)
        self.image = pg.image.load(LAVA_IMG).convert_alpha()

class Rock:
    def __init__(self,game,coords:list):
        self.game = game
        self.rect = [coords[0],coords[1],0,0]
    def update(self):
        self.rect[0] += self.game.vel[0]
        self.rect[1] += self.game.vel[1]
    def draw(self):
        self.game.screen.blit(self.image,self.rect)
    
class BigRock(Rock):
    def __init__(self,game,coords):
        super().__init__(game,coords)
        self.rect[2] = BROCK_SIZE[0]
        self.rect[3] = BROCK_SIZE[1]
        self.image = pg.image.load(BROCK_IMG).convert_alpha()
        self.image.set_colorkey(COLORKEY)
        self.hitbox = [self.rect[0]+21,self.rect[1]+7,14,30]
    def update(self):
        super().update()
        self.hitbox[0] = self.rect[0] + 21
        self.hitbox[1] = self.rect[1] + 7
    def draw(self):
        super().draw()
        # pg.draw.rect(self.game.screen,RED,self.hitbox)

class SmallRock(Rock):
    def __init__(self,game,coords):
        super().__init__(game,coords)
        self.rect[2] = SROCK_SIZE[0]
        self.rect[3] = SROCK_SIZE[1]
        self.image = pg.image.load(SROCK_IMG).convert_alpha()
        self.image.set_colorkey(COLORKEY)
        self.hitbox = [self.rect[0]+14,self.rect[1]+37,36,8]
    def update(self):
        super().update()
        self.hitbox[0] = self.rect[0] + 14
        self.hitbox[1] = self.rect[1] + 37
    def draw(self):
        super().draw()
        # pg.draw.rect(self.game.screen,RED,self.hitbox)

class JumpPad:
    def __init__(self,game,coords:list):
        self.game = game
        self.image = pg.image.load(JUMP_PAD_IMG).convert_alpha()
        self.image.set_colorkey(COLORKEY)
        self.sound = pg.mixer.Sound(JUMP_PAD_SOUND)
        self.rect = coords + JUMP_PAD_SIZE
        self.hitbox = coords + JUMP_PAD_HITBOX
    def update(self):
        self.rect[0] += self.game.vel[0]
        self.rect[1] += self.game.vel[1]
        self.hitbox[0] = self.rect[0]
        self.hitbox[1] = self.rect[1] + 40
    def draw(self):
        self.game.screen.blit(self.image,self.rect)


class Waterfall:
    def __init__(self,game,x:int):
        self.game = game
        self.rect = [x,0,100,HEIGHT]

        self.images = []
        for image in WATERFALL_IMGS:
            img = pg.image.load(image).convert_alpha()
            img.set_colorkey(COLORKEY)
            self.images.append(img)

        self.image_index = 0
        self.index_interval = 1.0 / 7
        self.stop = False
    def update(self):
        if not self.stop:
            self.check_stop()
        self.check_finish()

        self.image = self.images[int(round(self.image_index,5))]
        self.image_index += self.index_interval
        self.image_index %= 7

        self.rect[0] += self.game.vel[0]
        self.rect[1] += self.game.vel[1]
    def draw(self):
        self.game.screen.blit(self.image,self.rect)
    def check_stop(self):
        if self.rect[0] <= WIDTH - self.rect[2]:
            self.rect[0] = WIDTH - self.rect[2]
            self.stop = True
            self.game.vel[0] = 0
            self.game.player.vel[0] = 10
    def check_finish(self):
        i = self.rect[0] - self.game.player.rect[0]
        if i <= 300:
            self.index_interval = 1.0 / (((300 - i) / 50) + 8)
            self.game.player.vel[0] = (i/80) + 0.5
            self.game.player.rect[1] -= (i/40)
            self.game.player.vel[1] = 0
            if self.game.player.rect[0] + PLAYER_RECT[2] >= self.rect[0]:
                self.game.running = False

def x_collides(rect1:list,rect2:list):
    if rect1[0] <= rect2[0] <= rect1[0] + rect1[2]:
        return True
    elif rect2[0] <= rect1[0] <= rect2[0] + rect2[2]:
        return True
    return False

def y_collides(rect1:list,rect2:list):
    return (rect2[1] <  rect1[1] + rect1[3] <= rect2[1] + rect2[3] or
        rect2[1] <= rect1[1] < rect2[1] +  rect2[3] or 
        rect1[1] <  rect2[1] + rect2[3] <= rect1[1] + rect1[3] or
        rect1[1] <= rect2[1] < rect1[1] +  rect1[3])

def collides(rect1:list,rect2:list):
    return x_collides(rect1,rect2) and y_collides(rect1,rect2)