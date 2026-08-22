import pygame
import os
import settings as game_settings
from settings import *
from tilemap import TileMap
from player import *
from enemy import *
from menu import show_main_menu, _draw_box, _button_clicked

scream_picture = pygame.image.load("assets/images/scream_picture.jpg")
game_over_sound = None


def create_screen():
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    w, h = game_settings.SCREEN_SIZES[game_settings.screen_size]

    return pygame.display.set_mode(
        (w, h),
        pygame.RESIZABLE
    )


def run_game(screen, clock, character):
    tilemap = TileMap()

    # 1. Получаем случайные безопасные клетки (индексы) для игрока
    p_cell_x, p_cell_y = tilemap.get_safe_cell_position()

    # 2. Создаем игрока ОДИН раз по безопасным координатам
    player = Player(
        tilemap,
        start_x=p_cell_x,
        start_y=p_cell_y,
        character=character,
    )

    # 3. Получаем случайные безопасные клетки отдельно для каждого врага
    e1_x, e1_y = tilemap.get_safe_cell_position()
    e2_x, e2_y = tilemap.get_safe_cell_position()
    e3_x, e3_y = tilemap.get_safe_cell_position()

    # 4. Передаем координаты клеток в конструкторы врагов
    enemy = Enemy(x=e1_x, y=e1_y, tilemap=tilemap)
    enemy2 = Enemy(x=e2_x, y=e2_y, tilemap=tilemap)
    enemy3 = Enemy(x=e3_x, y=e3_y, tilemap=tilemap)

    font_button = pygame.font.SysFont(None, 36)

    if game_settings.sound_enabled:
        try:
            pygame.mixer.music.load("assets/sounds/low_sound.mp3")
            pygame.mixer.music.play(-1)

        except pygame.error:
            pass

    while True:
        clock.tick(FPS)

        map_w = MAP_WIDTH * TILE_SIZE
        map_h = MAP_HEIGHT * TILE_SIZE
        sw, sh = screen.get_size()
        offset_x = (sw - map_w) // 2
        offset_y = (sh - map_h) // 2

        exit_rect = pygame.Rect(offset_x + map_w - 130, offset_y + 10, 120, 50)

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

        if not player.alive:
            pygame.mixer.music.stop()
            game_over_sound.play()

            font = pygame.font.SysFont(None, 72)
            text = font.render("GAME OVER", True, RED)

            bg = pygame.transform.smoothscale(
                scream_picture,
                screen.get_size()
            )

            screen.blit(bg, (0, 0))

            screen.blit(
                text,
                (
                    screen.get_width() // 2 - text.get_width() // 2,
                    screen.get_height() // 2 - text.get_height() // 2,
                ),
            )

            pygame.display.flip()
            pygame.time.wait(3000)

            return "menu"

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
        text = (100, 200, 255) if exit_hovered else WHITE

        _draw_box(screen, exit_rect, "выход", font_button, border, text)

        pygame.display.flip()


def main():
    pygame.init()
    pygame.mixer.init()

    global game_over_sound
    game_over_sound = pygame.mixer.Sound("assets/sounds/s_s.mp3")

    screen = create_screen()
    pygame.display.set_caption("PyDangeon")
    clock = pygame.time.Clock()

    while True:

        menu_result = show_main_menu(screen, clock)

        if isinstance(menu_result, tuple):
            menu_status, character = menu_result
        else:
            menu_status = menu_result
            character = None

        if menu_status == "quit":
            break

        if menu_status == "resize":
            screen = create_screen()
            continue

        if menu_status == "play":
            game_status = run_game(screen, clock, character)

            if game_status == "quit":
                break

    pygame.quit()


if __name__ == "__main__":
    main()
