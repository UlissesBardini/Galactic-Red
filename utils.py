import pygame

def carregar_sprite(img):
    return pygame.image.load("assets/sprites/" + img)

def criar_texto(texto, fonte, tamanho, cor):
    return pygame.font.SysFont(fonte, tamanho).render(texto, True, cor)

def apresentar(win, texto, pos):
    win.blit(texto, pos)

def carregar_audio(audio):
    return pygame.mixer.Sound("assets/sfx/" + audio)