import pygame as pg
import pandas as pd
import numpy as np
from random import randint

best_players = pd.read_csv("Best_players.csv")
Nickname = input("Введите имя игрока: ")
if Nickname in best_players.columns:
    Nickname = input("Имя занято, введите другое: ")

pg.init()

FPS = 30
width = 1000
height = 750
screen = pg.display.set_mode((width, height))

#Возможные цвета шариков в формате, подходящем для pygame.Color.
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
green = (0, 255, 0)
magenta = (255, 0, 255)
cyan = (0, 255, 255)
colors = [red, blue, yellow, green, magenta, cyan]

result = 0    # Количество очков
balls = []    # Массив содержащий параметры шаров, нахлдящихся на экране

def first_ball(surface, x_range, y_range, vx_range,
               vy_range, r_range, colors):
    '''Создаёт шар только при первой итерации.
    surface - объект pygame.Surface.  
    x_range - диапазон возможных координат x центра шара.   
    y_range - диапазон возможных координат y центра шара.  
    vx_range - диапазон возможных скоростей шара по оси x.  
    vy_range - диапазон возможных скоростей шара по оси y.  
    r_range - диапазон возможных радиусов шара.  
    colors - массив возможных цветов в формате,
    подходящем для pygame.Color.

    '''
    global first_cicle
    if first_cicle:
        new_ball(
            surface, x_range, y_range, vx_range,
            vy_range, r_range, colors)
        first_cicle = False

def new_ball(surface, x_range, y_range, vx_range,
             vy_range, r_range, colors):
    '''Рисует новый шарик.  
    surface - объект pygame.Surface.  
    x_range - диапазон возможных координат x центра шара.  
    y_range - диапазон возможных координат y центра шара.
    vx_range - диапазон возможных скоростей шара по оси x.  
    vy_range - диапазон возможных скоростей шара по оси y.  
    r_range - диапазон возможных радиусов шара.  
    colors - массив возможных цветов в формате,
    подходящем для pygame.Color.
    
    '''
    global balls
    parametrs = random_parametrs(x_range, y_range, vx_range,
                                 vy_range, r_range)
    color = random_color(colors)
    draw_ball(surface, parametrs, color)
    # Сохраняем параметры шара в виде словаря и добавляем в массив шаров.
    ball = {
        "x": parametrs[0][0],
        "y": parametrs[0][1],
        "vx": parametrs[1][0],
        "vy": parametrs[1][1],
        "r": parametrs[2],
        "color": color
        }
    balls.append(ball)

def random_parametrs(x_range, y_range, vx_range, vy_range,  r_range):
    '''Возвращает случайные параметры в виде массива:
    (x, y) - кортеж из координат центра круга,
    (vx, vy) - кортеж из компонент скоростей шарика,
    r - радиус круга.  
    x_range - диапазон возможных координат x центра шара.  
    y_range - диапазон возможных координат y центра шара.  
    vx_range - диапазон возможных скоростей шара по оси x.  
    vy_range - диапазон возможных скоростей шара по оси y.  
    r_range - диапазон возможных радиусов шара.
    
    '''
    x = randint(x_range[0], x_range[1])
    y = randint(y_range[0], y_range[1])
    r = randint(r_range[0], r_range[1])
    vx = randint(vx_range[0], vx_range[1])
    vy = randint(vy_range[0], vy_range[1])
    return [(x, y), (vx, vy), r]

def random_color(colors):
    '''Возвращает случайный цвет в формате,
    подходящем для pyygame.Color.
    
    '''
    return colors[randint(0, len(colors) - 1)]

def draw_ball(surface, parametrs, color):
    '''Рисует шарик.  
    surface - объект pygame.Surface.
    parametrs - параметры в виде массива:
    (x, y) - кортеж из координат центра круга,
    (vx, vy) - кортеж из компонент скоростей шарика,
    r - радиус круга.  
    color - цвет шара в формате,
    подходящем для pyygame.Color.
    
    '''
    pg.draw.circle(surface, color, parametrs[0], parametrs[2])

def click_at_least_one_ball(event, balls):
    '''Проверяет попадание хотя бы в один шар,
    в противном случае увеличивает счётчик непопадний.  
    event - объект pygame.Event.  
    balls - Массив содержащий параметры шаров, нахлдящихся на экране.
    
    '''
    for i in range(len(balls)):
        click(event, balls[i])
        if success:
            balls.pop(i)    # Обновляет массив шаров, находящихся на экране
            break

def click(event, ball):
    '''Проверяет попадание мыши по шару и засчитывает очки.
    event - объект pygame.Event.
    ball - словарь с параметрами шара.
    
    '''
    global result, success
    if (event.pos[0]-ball["x"])**2 + \
       (event.pos[1]-ball["y"])**2 <= ball["r"]**2:
        result += 1    # Засчитывает очко за попадание
        success = True
    else:
        success = False


def move_balls(balls, width_of_screen, height_of_screen,
               vx_range, vy_range):
    '''Двигает шары в ходе игры.  
    balls - Массив содержащий параметры шаров, находящихся на экране.
    width_of_scree - ширина игрового экрана.
    height_of_scree - высота игрового экрана.  
    vx_range - диапазон возможных скоростей шара по оси x.  
    vy_range - диапазон возможных скоростей шара по оси y.
    
    '''
    for ball in balls:
        reflection_from_wall(ball, width_of_screen, height_of_screen,
                             vx_range, vy_range)
        ball["x"] += ball["vx"] * dt
        ball["x"] = int(ball["x"])
        ball["y"] += ball["vy"] * dt
        ball["y"] = int(ball["y"])
        pg.draw.circle(screen, ball["color"],
                      (ball["x"], ball["y"]), ball["r"])

def reflection_from_wall(ball, width_of_screen, height_of_screen,
                         vx_range, vy_range):
    '''Сменяет, если необходимо, скорость шара при отражении,
    на случайный вектор, направленный так, чтобы шар летел от стены.  
    ball - словарь с параметрами шара.
    width_of_scree - ширина игрового экрана.
    height_of_scree - высота игрового экрана.  
    vx_range - диапазон возможных скоростей шара по оси x.  
    vy_range - диапазон возможных скоростей шара по оси y.  

    '''
    if ball["x"] <= ball["r"]:
        ball["vx"] = randint(1, vx_range[1])
    elif ball["x"] >= width_of_screen - ball["r"]:
        ball["vx"] = randint(vx_range[0], -1)
    if ball["y"] <= ball["r"]:
        ball["vy"] = randint(1, vx_range[1])
    elif ball["y"] >= height_of_screen - ball["r"]:
        ball["vy"] = randint(vy_range[0], -1)

pg.display.update()
clock = pg.time.Clock()
finished = False
first_cicle = True

while not finished:
    dt = clock.tick(FPS) / 1000.0
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            click_at_least_one_ball(event, balls)
            # Добавляем  новый шар в случае промаха
            # или отсутствия шаров на экране
            if (len(balls) == 0) or not success:    
                new_ball(screen, (75, 925), (75, 625), (-100, 100),
                        (-100, 100), (20, 45), colors)
    move_balls(balls, width, height, (-100, 100), (-100, 100))
    first_ball(screen, (75, 925), (75, 625), (-50, 50),
              (-50, 50), (20, 45), colors)
    pg.display.update()
    screen.fill((0, 0, 0))    # Заполняет экран чёрным цветом

pg.quit()

print("Количество очков: ", result)

def add_score_to_table():
    '''Добавляет результат в таблицу 5 лучших,
    если он является таким.

    '''
    game_result = pd.DataFrame({"Nickname": [Nickname], "Score": [result]})
    best_players_cur = pd.concat([best_players, game_result],
                                 ignore_index = True)
    best_players_cur.sort_values(by="Score", ascending = False,
                                 inplace = True)
    new_best_players = best_players_cur.loc[0:4]
    new_best_players.to_csv("Best_players.csv", index = False)
add_score_to_table()
