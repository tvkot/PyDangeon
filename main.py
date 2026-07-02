import pygame
from settings import *
from tilemap import *
from player import *
from enemy import *
from menu import show_main_menu


def run_game(screen, clock):
    tilemap = TileMap()
    player = Player(tilemap, start_x=1, start_y=1)

    enemy = Enemy(x=5, y=5, tilemap=tilemap)
    enemy2 = Enemy(x=10, y=10, tilemap=tilemap)
    enemy3 = Enemy(x=15, y=15, tilemap=tilemap)

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            player.handle_event(event, enemy, enemy2, enemy3)

        screen.fill(DARK_GREY)

        enemy.update(player)
        enemy2.update(player)
        enemy3.update(player)

        # 1. Считаем смещение камеры, чтобы игрок ВСЕГДА был в центре экрана
        # (Вместо TILE_SIZE подставьте реальный размер клетки, например, 32 или 64, если TILE_SIZE нет в settings)
        camera_x = SCREEN_W // 2 - player.x * TILE_SIZE
        camera_y = SCREEN_H // 2 - player.y * TILE_SIZE

        # 2. Создаем временную поверхность (холст) для центрирования
        game_surface = pygame.Surface((SCREEN_W, SCREEN_H))
        game_surface.fill(DARK_GREY)

        # 3. Рисуем всё игровое окружение на этот холст
        tilemap.draw(game_surface, player)
        player.draw(game_surface)
        enemy.draw(game_surface)
        enemy2.draw(game_surface)
        enemy3.draw(game_surface)

        # 4. Выводим холст на реальный экран с правильным центрированным смещением
        screen.blit(game_surface, (camera_x, camera_y))

        pygame.display.flip()


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("PyDangeon")
    clock = pygame.time.Clock()

    menu_status = show_main_menu(screen, clock)

    if menu_status == "play":
        run_game(screen, clock)

    pygame.quit()


if __name__ == "__main__":
    main()
