import pygame
from settings import *
from tilemap import *
from player import *
from enemy import *

pygame.init()  # инициализация pygame

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))  # создаем окно
pygame.display.set_caption("PyDangeon")  # название окна

clock = pygame.time.Clock()  # контроль фпс

tilemap = TileMap()  # создание карты
player = Player(tilemap, start_x=1, start_y=1)  # создание игрока
enemy = Enemy(x=5, y=5, tilemap = tilemap)
enemy2 = Enemy(x=10, y=10, tilemap = tilemap)
enemy3 = Enemy(x=15, y=15, tilemap = tilemap)
running = True
# основной цикл игры
while running:
    clock.tick(FPS)  # ограничение фпс

    # обработка событий
    for event in pygame.event.get():

        # пользователь нажимает на крестик - цикл завершается
        if event.type == pygame.QUIT:
            running = False

        player.handle_event(event, enemy, enemy2, enemy3)

    # заливка экрана цветом
    screen.fill(DARK_GREY)

    # отрисовка карты
    enemy.update(player)
    enemy2.update(player)
    enemy3.update(player)
    tilemap.draw(screen, player)
    tilemap.draw(screen, tilemap)

    # отрисовка игрока
    player.draw(screen)
    enemy.draw(screen)
    enemy2.draw(screen)
    enemy3.draw(screen)
    # убираем мерцание
    pygame.display.flip()

pygame.quit()


