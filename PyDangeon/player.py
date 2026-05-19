import pygame
from settings import *

class Player:
    def __init__(self, tilemap, start_x, start_y):
        # tilemap — это наша карта, передаём её сюда
        # чтобы игрок мог проверять — стена впереди или нет
        self.tilemap = tilemap

        # Позиция игрока в КЛЕТКАХ (не в пикселях!)
        # Например x=1, y=1 — это вторая клетка по горизонтали и вертикали
        # (счёт начинается с 0)
        self.x = start_x
        self.y = start_y

        # Размер игрока чуть меньше клетки чтобы красиво выглядело
        self.size = TILE_SIZE - 4

        # Цвет игрока — синий
        self.color = BLUE

    def move(self, dx, dy):
        # dx — шаг по горизонтали (-1 влево, +1 вправо, 0 стоим)
        # dy — шаг по вертикали   (-1 вверх,  +1 вниз,   0 стоим)

        # Считаем куда ХОТИМ пойти
        new_x = self.x + dx
        new_y = self.y + dy

        # Проверяем: там не стена? Тогда идём!
        # Если там стена — просто ничего не делаем
        if not self.tilemap.is_wall(new_x, new_y):
            self.x = new_x
            self.y = new_y

    def handle_event(self, event):
        # Обрабатываем нажатие клавиш
        # KEYDOWN — это событие "клавиша нажата"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move(-1, 0)   # влево
            if event.key == pygame.K_RIGHT:
                self.move(1, 0)    # вправо
            if event.key == pygame.K_UP:
                self.move(0, -1)   # вверх
            if event.key == pygame.K_DOWN:
                self.move(0, 1)    # вниз

    def draw(self, screen):
        # Переводим позицию из КЛЕТОК в ПИКСЕЛИ для отрисовки
        # +2 — небольшой отступ чтобы игрок был по центру клетки
        px = self.x * TILE_SIZE + 2
        py = self.y * TILE_SIZE + 2

        pygame.draw.rect(screen, self.color, (px, py, self.size, self.size))
