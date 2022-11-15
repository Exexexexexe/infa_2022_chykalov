import pygame
from pygame.draw import *
pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GRAY = (224, 224, 224)

def draw_here():
    '''
    Рисует смайлик на экране
    
    '''
    draw_fone()
    draw_main_circle()
    draw_left_eye()
    draw_right_eye()
    draw_left_eyebrow()
    draw_right_eyebrow()
    draw_mouth()

def draw_fone():
    '''
    Закрашивает фон
    '''
    rect(screen, GRAY, (0, 0, 400, 400))
def draw_main_circle():
    '''
    Рисует главное тело смайлика
    '''
    circle(screen, YELLOW, (200, 200), 100)
def  draw_left_eye():
    '''
    Рисует левый глаз смайлика
    '''
    circle(screen, RED, (160,180), 25)
    circle(screen, BLACK, (160,180), 25, 2)
    circle(screen, BLACK, (160,180), 10)
def  draw_right_eye():
    '''
    Рисует правый глаз смайлика
    '''
    circle(screen, RED, (240,180), 15)
    circle(screen, BLACK, (240,180), 15, 2)
    circle(screen, BLACK, (240,180), 5)
def draw_left_eyebrow():
    '''
    Рисует левую бровь
    '''
    polygon(screen, BLACK, [(190, 170), (200, 160), (100, 115), (90, 125)])
def draw_right_eyebrow():
    '''
    Рисует правую бровь
    '''
    polygon(screen, BLACK, [(220, 170), (221, 160), (276, 143), (275, 152)])
def draw_mouth():
    '''
    Рисует рот смайлика
    '''
    rect(screen, BLACK, (140, 230, 120, 15))


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    draw_here()
    pygame.display.update()

pygame.quit()
