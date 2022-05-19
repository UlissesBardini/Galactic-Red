import random
import pygame
from utils import apresentar, carregar_audio, carregar_sprite, criar_texto
pygame.init()

MENU_INICIAL = carregar_sprite("menu-inicial.png")
ESPACO = carregar_sprite("espaco.png")
METEORO = carregar_sprite("meteoro.png")
NAVE = carregar_sprite("nave.png")
NAVE_DESTRUIDA = carregar_sprite("nave-destruida.png")
NAVE_INIMIGA = carregar_sprite("nave2.png")
TIRO = carregar_sprite("tiro.png")
BRANCO = 255,255,255

LARGURA, ALTURA = ESPACO.get_width(), ESPACO.get_height()
WIN = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Galactic Red")

TIRO_SOM = carregar_audio("atirando.wav")
NAVE_DESTRUIDA_SOM = carregar_audio("nave-destruida.wav")
pygame.mixer.music.load('assets/sfx/soundtrack.mp3')
pygame.mixer.music.set_volume(0.5)

FPS = 60

class Cenario:
    def __init__(self):
        self.x, self.y = self.START_POS
        self.sprite = ESPACO
    
    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))
        self.move()
        if self.y > 0:
            win.blit(self.sprite, (self.x, self.y - self.sprite.get_height()))

    def move(self):
        self.y += 5
        if self.y > self.sprite.get_height():
            self.y = 0
    
    START_POS = 0, 0

class Nave:
    COOLDOWN = 30

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vida = 100
        self.tiros = []
        self.cooldown_counter = 0

    def atirar(self):
        if self.cooldown_counter == 0:
            tiro = Tiro((self.x + self.sprite.get_width()/2), self.y)
            self.tiros.append(tiro)
            self.cooldown_counter = 1

    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1

    def move_tiros(self, vel, obj):
        self.cooldown()
        for tiro in self.tiros:
            tiro.move(vel)
            if tiro.off_screen():
                self.tiros.remove(tiro)
            elif tiro.collision(obj):
                obj.vida -= 10
                self.tiros.remove(tiro)

    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))
        for tiro in self.tiros: 
            tiro.draw(WIN)

class Player(Nave):
    START_POS = 351, 440

    def __init__(self):
        super().__init__(self.START_POS[0], self.START_POS[1])
        self.vel = 10
        self.sprite = NAVE
        self.mask = pygame.mask.from_surface(self.sprite)
        self.max_vida = 100
        self.pontos = 0
    
    def move(self, left = False, right = False, up = False, down = False):
        if right:
            self.x += self.vel
        elif left:
            self.x -= self.vel

        if up:
            self.y -= self.vel
        elif down:
            self.y += self.vel

    def atirar(self):
        tiro = Tiro((self.x + self.sprite.get_width()/2), self.y)
        self.tiros.append(tiro)
        TIRO_SOM.play()
        

    def move_tiros(self, vel, objs):
        for tiro in self.tiros:
            tiro.move(vel)
            if tiro.off_screen():
                self.tiros.remove(tiro)
            else:
                for obj in objs:
                    if tiro.collision(obj):
                        self.pontos += 100
                        objs.remove(obj)
                        self.tiros.remove(tiro)

class Inimigo(Nave):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = NAVE_INIMIGA
        self.mask = pygame.mask.from_surface(self.sprite)
        self.vel = 7

    def move(self):
        self.y += self.vel
    
    def atirar(self):
        if self.cooldown_counter == 0:
            tiro = Tiro((self.x + self.sprite.get_width()/2), self.y + self.sprite.get_height())
            self.tiros.append(tiro)
            self.cooldown_counter = 1

class Tiro:
    def __init__(self, x, y):
        self.sprite = TIRO
        self.x, self.y = x, y
        self.mask = pygame.mask.from_surface(self.sprite)
    
    def move(self, vel):
        self.y -= vel

    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))

    def off_screen(self):
        return self.y < 0 or self.y > ALTURA

    def collision(self, obj):
        return collide(self, obj)

class Meteoro:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.sprite = METEORO
        self.start_pos = x, y
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))

    def move(self):
        self.y += 10
        self.x += 20 * -(abs(self.start_pos[0])/self.start_pos[0])

class MenuInicial:
    def __init__(self):
        self.x, self.y = 0, 0
        self.sprite = MENU_INICIAL

    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None

def draw_menu(win, menu, botao):
        menu.draw(win)
        texto_botao = criar_texto("Jogar","lucidasans",25,BRANCO)
        pygame.draw.rect(win, (255,0,0), botao , 0)
        pygame.draw.rect(win, BRANCO, botao , 2)
        win.blit(texto_botao, (110 - texto_botao.get_width()/2, 565 - texto_botao.get_height()/2))
        pygame.display.update()


def draw(win, cenario, player):
    cenario.draw(win)

    player.draw(win)
    for inimigo in inimigos:
        inimigo.draw(win)
    for meteoro in meteoros:
        meteoro.draw(win)

    texto_pontos = criar_texto("Pontos: " + str(player.pontos), "lucidasans",25,BRANCO)
    texto_vidas = criar_texto("Vidas: " + str(vidas), "lucidasans",25,BRANCO)
    texto_game_over = criar_texto("GAME OVER", "lucidasans",60,BRANCO)

    vida_borda = pygame.Rect(540,10, 250, 25)
    vida_rect = pygame.Rect(540,10, 250 * (player.vida/player.max_vida), 25)

    apresentar(WIN, texto_pontos, (10, 5))
    apresentar(WIN, texto_vidas, (10, 35))
    pygame.draw.rect(win, (255,0,0), vida_borda,0)
    pygame.draw.rect(win, (0,255,0), vida_rect,0)
    pygame.draw.rect(win, BRANCO, vida_borda,1)

    if perdeu:
        apresentar(WIN, texto_game_over,(LARGURA/2 - texto_game_over.get_width()/2,
            ALTURA/2 - texto_game_over.get_height()/2))
    pygame.display.update()

clock = pygame.time.Clock()
menu = MenuInicial()
cenario = Cenario()
player = Player()
run = True
game_running = True
menu_running = True
inimigos = []
meteoros = []
wave_len = 0
nivel = 0
vidas = 5
perdeu = False
perdeu_tempo = 0
replay_music = True

while run:
    if replay_music == True:
        pygame.mixer.music.play(-1)
        replay_music = False
    menu = MenuInicial()
    cenario = Cenario()
    player = Player()
    run = True
    game_running = True
    menu_running = True
    inimigos = []
    meteoros = []
    wave_len = 0
    nivel = 0
    vidas = 5
    perdeu = False
    perdeu_tempo = 0
    replay_music = False

    while menu_running:
        botao = pygame.Rect(10, 540, 200, 50)
        draw_menu(WIN, menu, botao)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                menu_running = False
                game_running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao.collidepoint(pygame.mouse.get_pos()):
                    menu_running = False
                    game_running = True

    while game_running:
        clock.tick(FPS)

        draw(WIN, cenario, player)

        if vidas <= 0 or player.vida <= 0:
            if player.vida <= 0 and perdeu_tempo == 0:
                player.sprite = NAVE_DESTRUIDA
                NAVE_DESTRUIDA_SOM.play()
            perdeu = True
            perdeu_tempo += 1

        if perdeu:
            pygame.mixer.music.stop()
            inimigos *= 0
            player.tiros *= 0
            meteoros *= 0
            if perdeu_tempo > FPS * 5:
                game_running = False
                menu_running = True
                replay_music = True
            else:
                continue

        if len(inimigos) == 0:
            nivel += 1
            wave_len += 5
            print("Nível: " + str(nivel))
            for i in range(wave_len):
                inimigo = Inimigo(random.randrange(50, LARGURA - 100), random.randrange(-5000 - 3000* nivel, -100))
                inimigos.append(inimigo)
            if nivel >= 2:
                if len(meteoros) == 0:
                    if random.randrange(0, 2) == 1:
                        meteoro = Meteoro(random.choice([-200, LARGURA]), 150)
                        meteoros.append(meteoro)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                game_running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.atirar()

        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_RIGHT]:
            if player.x + player.sprite.get_width() < WIN.get_width():
                player.move(right = True)
        elif key_pressed[pygame.K_LEFT]:
            if player.x > 0:
                player.move(left=True)
        if key_pressed[pygame.K_UP]:
            if player.y > 0:
                player.move(up=True)
        elif key_pressed[pygame.K_DOWN]:
            if player.y + player.sprite.get_height() < WIN.get_height():
                player.move(down=True)
    
        for inimigo in inimigos[:]:
            inimigo.move()
            inimigo.move_tiros(-10, player)

            if random.randrange(0,2*60) == 1:
                inimigo.atirar()

            if collide(inimigo, player):
                player.vida -= 10
                inimigos.remove(inimigo)  

            elif inimigo.y + inimigo.sprite.get_height() > ALTURA:
                vidas -= 1
                inimigos.remove(inimigo)
        
        for meteoro in meteoros[:]:
            meteoro.move()
            
            if collide(meteoro, player):
                player.vida -= 50
                meteoros.remove(meteoro)

        player.move_tiros(10, inimigos)

pygame.quit()
