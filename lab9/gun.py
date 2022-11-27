import math
from random import *

import pygame


FPS = 30

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy -= 1
        self.vx *= 0.98
        self.x += self.vx
        self.y -= self.vy
        if self.x <= 10:
            self.x = 10
            self.vx = -self.vx * 0.5
        if self.x >= 790:
            self.x = 790
            self.vx = -self.vx * 0.5
        if self.y <= 10:
            self.y = 10
            self.vy = -self.vy * 0.5
        if self.y >= 590:
            self.y = 590
            self.vy = -self.vy * 0.5

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        gunSurf = pygame.Surface((50 * math.log10(self.f2_power), 10))
        gunSurf.fill(WHITE)
        pygame.draw.line(gunSurf, self.color, (0, 5), (50 * math.log10(self.f2_power), 5), 5)
        gunSurf = pygame.transform.rotate(gunSurf, -math.degrees(self.an))
        self.screen.blit(gunSurf, (20, 450 + min(0, 50 * math.log10(self.f2_power) * math.sin(self.an))))
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = randint(600, 780)
        y = self.y = randint(300, 550)
        r = self.r = randint(2, 50)
        vx = self.vx = randint(-10, 10)
        vy = self.vy = randint(-10, 10)
        color = self.color = RED
        self.live = 1

    def move(self):
        """Переместить цель по прошествии единицы времени.  

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy и стен по краям окна
        (размер окна 800х600).  
        
        """
        self.x += self.vx
        self.y -= self.vy
        if self.x <= 110 + self.r:
            self.x = 110 + self.r
            self.vx = -self.vx
        if self.x >= 790 - self.r:
            self.x = 790 - self.r
            self.vx = -self.vx
        if self.y <= 10 + self.r:
            self.y = 10 + self.r
            self.vy = -self.vy
        if self.y >= 550 - self.r:
            self.y = 550 - self.r
            self.vy = -self.vy

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        """ Рисует цель.  """
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

def print_text(screen, text, x, y, size):
    """Выводит текст на игровой экран.

    Args:
    screen - объект типа pygame.Surface.  
    text - текст который нужно вывести.  
    (x, y) - координаты верхнего левого угла текста.
    size - шрифт текста
    """
    font = pygame.font.Font(None, size)
    text_to_surface = font.render(text, True, BLACK)
    screen.blit(text_to_surface, (x, y))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
success_hits = []
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target(screen)
target2 = Target(screen)
finished = False
was_hit = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target1.draw()
    target2.draw()
    for b in balls:
        b.draw()
    print_text(screen,
               str(target1.points + target2.points),
               10, 10,
               36
               )
    if len(success_hits):
        if pygame.time.get_ticks() <= success_hits[0][0] + 3000:
            print_text(screen,
                       "Вы уничтожили цель за " + str(success_hits[0][1]) + " выстрелов",
                       170, 280,
                       36
                       )
        else:
            success_hits.pop(0)
        
    pygame.display.update()

    dt = clock.tick(FPS) / 150
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    target1.move()
    target2.move()

    for b in balls:
        b.move()
        if b.hittest(target1):
            target1.live = 0
            target1.hit()
            target1.new_target()
            was_hit = True
        if b.hittest(target2):
            target2.live = 0
            target2.hit()
            target2.new_target()
            was_hit = True
        b.live -= dt
        if b.live <= 0:
            balls.remove(b)
            
    if was_hit:
        success_hits.append((pygame.time.get_ticks(), bullet))
        bullet = 0
        was_hit = False
    gun.power_up()
    

pygame.quit()
