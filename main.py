# File created by: Liam Newberry, Auden Silcock, Taran Egenolf, Alejandro Madero
# Internal imports
from settings import *
from sprites import *
# External imports
import pygame as pg

class Title:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        icon_image = pg.image.load(ICON_IMG)
        icon_image.set_colorkey(COLORKEY)
        pg.display.set_icon(icon_image)
        self.clock = pg.time.Clock()
        self.running = True
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.draw()
    def new(self):
        self.background = Background(self)
        self.background.image = pg.image.load(TITLE_IMG).convert_alpha()

        self.music = pg.mixer.music.load(TITLE_MUSIC)
        pg.mixer.music.play(-1)
    def events(self):
        for event in pg.event.get():
            event_type = event.type
            if event_type == pg.QUIT:
                pg.mixer.quit()
                pg.quit()
            elif event_type == pg.MOUSEBUTTONUP:
                self.running = False
    def draw(self):
        self.background.draw()
        self.draw_text(TITLE_TEXT,TITLE_TEXT_COORDS)
        pg.display.flip()
    def draw_text(self,text:str,coords:list):
        font = pg.font.Font(FONT,FONT_SIZE)
        text_rect = font.render(text,True,FONT_COLOR)
        self.screen.blit(text_rect,coords)

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        icon_image = pg.image.load(ICON_IMG)
        icon_image.set_colorkey(COLORKEY)
        pg.display.set_icon(icon_image)
        self.clock = pg.time.Clock()
        self.running = True
        self.attempts = 0
        self.attempt_timer = -500
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    def new(self):
        self.moved = 0

        self.dead = False 
        self.time_of_death = 0

        if pg.time.get_ticks() - self.attempt_timer > 500:
            self.attempts += 1
            self.attempt_timer = pg.time.get_ticks()
            self.attempt_delay = ATTEMPT_DELAY

        self.background = Background(self)

        self.vel = PLATFORM_VEL.copy()

        self.music = pg.mixer.music.load(GAME_MUSIC)
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(1)
        pg.mixer.music.set_pos(0)

        self.all_sprites = []
        self.platforms = []
        self.snakes = []
        self.rocks = []
        self.jump_pads = []

        self.player = Player(self)
        self.player.rect[0] = 110
        self.player.rect[1] = 649
        self.all_sprites.append(self.player)
        
        self.chunks = {0:[BigRock(self,[1000,660]),
                          Platform(self,[0,720]),
                          Platform(self,[100,720]),
                          Platform(self,[200,720]),
                          Platform(self,[300,720]),
                          Platform(self,[400,720]),
                          Platform(self,[500,720]),
                          Platform(self,[600,720]),
                          Platform(self,[700,720]),
                          Platform(self,[800,720]),
                          Platform(self,[900,720]),
                          Platform(self,[1000,720]),
                          Platform(self,[1100,720]),
                          Platform(self,[1200,720]),
                          Platform(self,[1300,720]),
                          Platform(self,[1400,720])],
                       -1500:[SmallRock(self,[2800,660]),
                              BigRock(self,[2860,660])],
                       -3000:[Snakes(self,[4000-1500,720]),
                              Snakes(self,[4060-1500,700]),
                              Snakes(self,[4160-1500,700]),
                              Snakes(self,[4260-1500,700]),
                              Snakes(self,[4360-1500,700]),
                              Snakes(self,[4460-1500,700]),
                              SmallRock(self,[3200-1500,660]),
                              BigRock(self,[3260-1500,660]),
                              Log(self,[4000-1500,660]),
                              Log(self,[4400-1500,600]),
                              Log(self,[4400-1500,660])],
                       -4500:[Snakes(self,[4560-3000,700]),
                              Snakes(self,[4660-3000,700]),
                              Snakes(self,[4760-3000,700]),
                              Snakes(self,[4860-3000,700]),
                              BigRock(self,[5320-3000,660]),
                              BigRock(self,[5380-3000,660]),
                              BigRock(self,[5440-3000,660]),
                              BigRock(self,[5500-3000,660]),
                              BigRock(self,[5560-3000,660]),
                              BigRock(self,[5620-3000,660]),
                              BigRock(self,[5680-3000,660]),
                              BigRock(self,[5740-3000,660]),
                              BigRock(self,[5800-3000,660]),
                              JumpPad(self,[5240-3000,660]),
                              Log(self,[4800-3000,540]),
                              Log(self,[4800-3000,600]),
                              Log(self,[4800-3000,660])],
                       -6000:[BigRock(self,[6340-4500,660]),
                              BigRock(self,[6400-4500,660]),
                              BigRock(self,[6460-4500,660]),
                              BigRock(self,[6520-4500,660]),
                              BigRock(self,[6720-4500,660]),
                              BigRock(self,[6780-4500,660]),
                              BigRock(self,[6840-4500,660]),
                              BigRock(self,[6900-4500,660]),
                              BigRock(self,[7100-4500,660]),
                              BigRock(self,[7160-4500,660]),
                              BigRock(self,[7220-4500,660]),
                              BigRock(self,[7280-4500,660]),
                              JumpPad(self,[7420-4500,660])],
                       -7500:[Snakes(self,[8360-6000,700]),
                              Snakes(self,[8420-6000,700]),
                              Snakes(self,[8480-6000,700]),
                              Snakes(self,[8540-6000,700]),
                              Snakes(self,[8600-6000,700]),
                              Snakes(self,[8660-6000,700]),
                              Snakes(self,[8720-6000,700]),
                              Snakes(self,[8780-6000,700]),
                              Snakes(self,[8840-6000,700]),
                              Snakes(self,[8900-6000,700]),
                              Snakes(self,[8960-6000,700]),
                              Bush(self,[8000-6000,500]),
                              Bush(self,[8060-6000,500]),
                              Bush(self,[8120-6000,500]),
                              Bush(self,[8180-6000,500]),
                              Bush(self,[8240-6000,500]),
                              Bush(self,[8300-6000,500]),
                              Bush(self,[8360-6000,500]),
                              Bush(self,[8420-6000,500]),
                              Bush(self,[8480-6000,500]),
                              Bush(self,[8540-6000,500]),
                              Bush(self,[8600-6000,500]),
                              Bush(self,[8300-6000,440]),
                              Bush(self,[8360-6000,440]),
                              Bush(self,[8240-6000,440]),
                              Bush(self,[8180-6000,440]),
                              Bush(self,[8400-6000,440]),
                              Log(self,[8300-6000,560]),
                              Log(self,[8240-6000,560]),
                              Log(self,[8360-6000,560]),
                              Log(self,[8300-6000,620]),
                              Log(self,[8300-6000,660]),
                              Bush(self,[8800-6000,440])],
                       -9000:[Snakes(self,[9020-7500,700]),
                              Snakes(self,[9080-7500,700]),
                              Snakes(self,[9140-7500,700]),
                              Snakes(self,[9200-7500,700]),
                              Snakes(self,[9260-7500,700]),
                              Snakes(self,[9320-7500,700]),
                              Snakes(self,[9380-7500,700]),
                              Snakes(self,[9420-7500,700]),
                              Snakes(self,[9480-7500,700]),
                              Snakes(self,[9540-7500,700]),
                              Snakes(self,[9600-7500,700]),
                              Snakes(self,[9660-7500,700]),
                              Snakes(self,[9720-7500,700]),
                              Snakes(self,[9780-7500,700]),
                              Snakes(self,[9840-7500,700]),
                              Snakes(self,[9900-7500,700]),
                              Snakes(self,[9960-7500,700]),
                              Snakes(self,[10020-7500,700]),
                              Bush(self,[9200-7500,440]),
                              Bush(self,[9600-7500,440]),
                              Bush(self,[10000-7500,440]),
                              Bush(self,[10400-7500,440]),
                              Bush(self,[10400-7500,380]),
                              Bush(self,[10400-7500,320]),
                              Bush(self,[10400-7500,260]),
                              Bush(self,[10400-7500,200])],
                       -10500:[JumpPad(self,[10500-9000,660]),
                               Bush(self,[11080-9000,500]),
                               Bush(self,[11140-9000,500]),
                               Bush(self,[11200-9000,500]),
                               Bush(self,[11260-9000,500]),
                               Bush(self,[11320-9000,500]),
                               Bush(self,[11380-9000,500]),
                               Bush(self,[11440-9000,500]),
                               Bush(self,[11500-9000,500]),
                               Bush(self,[11560-9000,500]),
                               Bush(self,[11620-9000,500]),
                               Bush(self,[11680-9000,500]),
                               Bush(self,[11380-9000,440]),
                               Bush(self,[11440-9000,440]),
                               Bush(self,[11320-9000,440]),
                               Bush(self,[11260-9000,440]),
                               Bush(self,[11500-9000,440]),
                               Log(self,[11380-9000,560]),
                               Log(self,[11440-9000,560]),
                               Log(self,[11320-9000,560]),
                               Log(self,[11380-9000,620]),
                               Log(self,[11380-9000,660])],
                       -12000:[SmallRock(self,[12300-10500,540]),
                               SmallRock(self,[12670-10500,480]),
                               SmallRock(self,[13120-10500,540]),
                               Log(self,[12180-10500,600]),
                               Log(self,[12180-10500,660]),
                               Log(self,[12240-10500,600]),
                               Log(self,[12240-10500,660]),
                               Log(self,[12300-10500,600]),
                               Log(self,[12300-10500,660]),
                               Log(self,[12550-10500,540]),
                               Log(self,[12610-10500,540]),
                               Log(self,[12670-10500,540]),
                               Log(self,[13000-10500,600]),
                               Log(self,[13060-10500,600]),
                               Log(self,[13120-10500,600]),
                               Log(self,[13000-10500,660]),
                               Log(self,[13060-10500,660]),
                               Log(self,[13120-10500,660])],
                       -13500:[SmallRock(self,[13720-12000,660]),
                               BigRock(self,[13780-12000,660]),
                               BigRock(self,[13840-12000,660]),
                               BigRock(self,[13900-12000,660]),
                               SmallRock(self,[13960-12000,660]),
                               SmallRock(self,[14220-12000,660]),
                               BigRock(self,[14280-12000,660]),
                               BigRock(self,[14340-12000,660]),
                               BigRock(self,[14400-12000,660]),
                               SmallRock(self,[14460-12000,660]),
                               Log(self,[14860-12000,420]),
                               Log(self,[14920-12000,420]),
                               Log(self,[14980-12000,420])],
                       -15000:[JumpPad(self,[15100-13500,660]),
                               JumpPad(self,[15580-13500,660]),
                               JumpPad(self,[15980-13500,660]),
                               Log(self,[15040-13500,420]),
                               Log(self,[15100-13500,420]),
                               Log(self,[15160-13500,420]),
                               Log(self,[15220-13500,420]),
                               Log(self,[15280-13500,420]),
                               Log(self,[15340-13500,420]),
                               Log(self,[15400-13500,420]),
                               Log(self,[15460-13500,420]),
                               Log(self,[15520-13500,420]),
                               Log(self,[15580-13500,420]),
                               Log(self,[15640-13500,420]),
                               Log(self,[15700-13500,420]),
                               Log(self,[15760-13500,420]),
                               Log(self,[16180-13500,420]),
                               Log(self,[16240-13500,420]),
                               Log(self,[16300-13500,420]),
                               Log(self,[16360-13500,420]),
                               Log(self,[16420-13500,420]),
                               Log(self,[16480-13500,420])],
                       -16500:[Snakes(self,[16560-15000,700]),
                               Snakes(self,[16460-15000,700]),
                               Snakes(self,[16360-15000,700]),
                               Snakes(self,[16260-15000,700]),
                               Snakes(self,[17060-15000,700]),
                               Snakes(self,[17120-15000,700]),
                               Snakes(self,[17180-15000,700]),
                               Snakes(self,[17240-15000,700]),
                               Snakes(self,[17300-15000,700]),
                               Snakes(self,[17360-15000,700]),
                               Snakes(self,[17420-15000,700]),
                               Snakes(self,[17480-15000,700]),
                               Snakes(self,[17540-15000,700]),
                               Snakes(self,[17600-15000,700]),
                               Snakes(self,[17660-15000,700]),
                               Snakes(self,[17720-15000,700]),
                               Snakes(self,[17780-15000,700]),
                               Snakes(self,[17840-15000,700]),
                               Snakes(self,[17900-15000,700]),
                               Snakes(self,[17960-15000,700]),
                               SmallRock(self,[17300-15000,420]),
                               BigRock(self,[17360-15000,420]),
                               BigRock(self,[17420-15000,420]),
                               BigRock(self,[17480-15000,420]),
                               SmallRock(self,[17540-15000,420]),
                               JumpPad(self,[17960-15000,420]),
                               Log(self,[16540-15000,420]),
                               Log(self,[16600-15000,420]),
                               Log(self,[16660-15000,420]),
                               Log(self,[16660-15000,480]),
                               Log(self,[16660-15000,540]),
                               Log(self,[16660-15000,600]),
                               Log(self,[16660-15000,660]),
                               Log(self,[17060-15000,480]),
                               Log(self,[17120-15000,480]),
                               Log(self,[17180-15000,480]),
                               Log(self,[17240-15000,480]),
                               Log(self,[17300-15000,480]),
                               Log(self,[17360-15000,480]),
                               Log(self,[17420-15000,480]),
                               Log(self,[17480-15000,480]),
                               Log(self,[17540-15000,480]),
                               Log(self,[17600-15000,480]),
                               Log(self,[17660-15000,480]),
                               Log(self,[17720-15000,480]),
                               Log(self,[17780-15000,480]),
                               Log(self,[17840-15000,480]),
                               Log(self,[17900-15000,480]),
                               Log(self,[17960-15000,480])],
                       -18000:[],
                       -19500:[Waterfall(self,19500-18000)]}
        self.fill_chunk(self.chunks[0])
        self.fill_chunk(self.chunks[-1500])
    def events(self):
        for event in pg.event.get():
            event_type = event.type
            if event_type == pg.QUIT:
                self.running = False
                pg.mixer.quit()
                pg.quit()
    def update(self):
        self.now = pg.time.get_ticks()
        print(len(self.all_sprites))
        self.moved += self.vel[0]
        if self.moved % 1500 == 0:
            self.fill_chunk(self.chunks[self.moved-1500])

        if self.now - self.attempt_timer > 2500:
            self.attempt_delay += self.vel[0]
        if self.dead and self.now - self.time_of_death > PLAYER_DEATH_PAUSE:
            self.new()
            self.time_of_death = 0
            self.dead = False
    def draw(self):
        self.background.draw()

        self.draw_text(f"Attempt {self.attempts}",[self.attempt_delay,250])

        i = 0
        while i < len(self.all_sprites):
            sprite = self.all_sprites[i]
            if sprite.rect[0] < -150:
                self.all_sprites.pop(i)
                sprite_type = type(sprite)
                if sprite_type in [Platform,Log,Bush]:
                    self.platforms.remove(sprite)
                elif sprite_type == Snakes:
                    self.snakes.remove(sprite)
                elif sprite_type in [BigRock,SmallRock]:
                    self.rocks.remove(sprite)
                elif sprite_type == JumpPad:
                    self.jump_pads.remove(sprite)
                continue
            sprite.update()
            sprite.draw()
            i += 1

        pg.display.flip()
    def draw_text(self,text:str,coords:list):
        font = pg.font.Font(FONT,FONT_SIZE)
        text_rect = font.render(text,True,FONT_COLOR)
        self.screen.blit(text_rect,coords)
    def fill_chunk(self,objects:list):
        for i in range(15,30):
            platform = Platform(self,[i * 100,720])
            self.all_sprites.append(platform)
            self.platforms.append(platform)
        for sprite in objects:
            sprite_type = type(sprite)
            self.all_sprites.append(sprite)
            if sprite_type in [Platform,Log,Bush]:
                self.platforms.append(sprite)
            elif sprite_type == Snakes:
                self.snakes.append(sprite)
            elif sprite_type in [BigRock,SmallRock]:
                self.rocks.append(sprite)
            elif sprite_type == JumpPad:
                self.jump_pads.append(sprite)

class End:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        icon_image = pg.image.load(ICON_IMG)
        icon_image.set_colorkey(COLORKEY)
        pg.display.set_icon(icon_image)
        self.clock = pg.time.Clock()
        self.running = True
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    def new(self):
        self.background = Background(self)
        self.background.image = pg.image.load(END_IMG).convert_alpha()

        self.sound = pg.mixer.Sound(END_SOUND)
        pg.mixer.Sound.play(self.sound)

        self.music = pg.mixer.music.load(END_MUSIC)
    def events(self):
        for event in pg.event.get():
            event_type = event.type
            if event_type == pg.QUIT:
                pg.mixer.quit()
                pg.quit()
            elif event_type == pg.MOUSEBUTTONUP:
                self.running = False
    def update(self):
        if pg.mixer.Sound.get_num_channels(self.sound) == 0 and not pg.mixer.music.get_busy():
            pg.mixer.music.play(-1)
    def draw(self):
        self.background.draw()
        pg.display.flip()

def run_game():
    pg.init()
    pg.mixer.init()

    while pg.get_init():
        t = Title()
        t.new()
        t.run()
        if pg.get_init():
            g = Game()
            g.new()
            g.run()
        if pg.get_init():
            e = End()
            e.new()
            e.run()

    if pg.get_init():
        pg.quit()
        pg.mixer.quit()