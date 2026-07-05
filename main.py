import pygame
from settings import *
from tilemap import *
from player import *
from enemy import *
from menu import show_main_menu, _draw_box, _button_clicked


def run_game(screen, clock):
    tilemap = TileMap()
    player = Player(tilemap, start_x=1, start_y=1)

    enemy = Enemy(x=5, y=5, tilemap=tilemap)
    enemy2 = Enemy(x=10, y=10, tilemap=tilemap)
    enemy3 = Enemy(x=15, y=15, tilemap=tilemap)

    font_button = pygame.font.SysFont(None, 36)

    running = True

    while running:
        clock.tick(FPS)

        map_w = MAP_WIDTH * TILE_SIZE
        map_h = MAP_HEIGHT * TILE_SIZE
        sw, sh = screen.get_size()
        offset_x = (sw - map_w) // 2
        offset_y = (sh - map_h) // 2
        exit_rect = pygame.Rect(offset_x + map_w - 900, offset_y + 10, 120, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
            if _button_clicked(event, exit_rect):
                return "menu"
            player.handle_event(event, enemy, enemy2, enemy3)

        screen.fill(DARK_GREY)

        enemy.update(player)
        enemy2.update(player)
        enemy3.update(player)

        game_surface = pygame.Surface((map_w, map_h))
        game_surface.fill(DARK_GREY)

        tilemap.draw(game_surface, player)
        player.draw(game_surface)
        enemy.draw(game_surface)
        enemy2.draw(game_surface)
        enemy3.draw(game_surface)

        screen.blit(game_surface, (offset_x, offset_y))

        exit_hovered = exit_rect.collidepoint(pygame.mouse.get_pos())
        border = (100, 200, 255) if exit_hovered else WHITE
        text_col = (100, 200, 255) if exit_hovered else WHITE
        _draw_box(screen, exit_rect, "выход", font_button, border, text_col)

        pygame.display.flip()


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("PyDangeon")
    clock = pygame.time.Clock()

    while True:
        menu_status = show_main_menu(screen, clock)
        if menu_status == "quit":
            break
        if menu_status == "play":
            game_status = run_game(screen, clock)
            if game_status == "quit":
                break

    pygame.quit()


if __name__ == "__main__":
    main()
