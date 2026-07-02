import pygame
from settings import *

MENU_PICTURE = "assets/images/menu_wolf.png"


def _load_menu_background(screen):
    image = pygame.image.load(MENU_PICTURE).convert()
    return pygame.transform.smoothscale(image, screen.get_size())


def _draw_box(surface, rect, text, font, border_color=WHITE, text_color=WHITE):
    # Плотная контрастная подложка (темно-синий цвет, чтобы кнопка точно выделялась)
    overlay = pygame.Surface((rect.width, rect.height))
    overlay.fill((15, 25, 45))
    surface.blit(overlay, rect.topleft)

    # Жирная рамка кнопки (толщина 4)
    pygame.draw.rect(surface, border_color, rect, 4, border_radius=12)

    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)


def _button_clicked(event, rect):
    return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and rect.collidepoint(event.pos)
    )


def show_settings(screen, clock):
    font_title = pygame.font.SysFont(None, 56)
    font_button = pygame.font.SysFont(None, 40)

    # Центрируем кнопку "Назад" внизу экрана
    back_rect = pygame.Rect(SCREEN_W // 2 - 100, SCREEN_H - 120, 200, 60)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        back_hovered = back_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if _button_clicked(event, back_rect):
                return "menu"

        screen.fill((15, 25, 45))

        title_rect = pygame.Rect(SCREEN_W // 2 - 160, 80, 320, 70)
        _draw_box(screen, title_rect, "Настройки", font_title, (100, 200, 255), (100, 200, 255))

        hint_font = pygame.font.SysFont(None, 32)
        hint = hint_font.render("Скоро здесь будут настройки", True, (255, 100, 100))
        screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 280))

        border = (100, 200, 255) if back_hovered else WHITE
        text_col = (100, 200, 255) if back_hovered else WHITE
        _draw_box(screen, back_rect, "назад", font_button, border, text_col)

        pygame.display.flip()
        clock.tick(FPS)


def show_main_menu(screen, clock):
    font_title = pygame.font.SysFont(None, 64)
    font_button = pygame.font.SysFont(None, 44)
    background = _load_menu_background(screen)

    # НАСТРОЙКА КООРДИНАТ: центрируем заголовок и кнопки вертикально
    title_rect = pygame.Rect(SCREEN_W // 2 - 160, 50, 320, 80)

    # Кнопки теперь идут по центру экрана друг под другом
    play_rect = pygame.Rect(SCREEN_W // 2 - 110, SCREEN_H // 2, 220, 70)
    settings_rect = pygame.Rect(SCREEN_W // 2 - 110, SCREEN_H // 2 + 90, 220, 70)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        play_hovered = play_rect.collidepoint(mouse_pos)
        settings_hovered = settings_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if _button_clicked(event, play_rect):
                return "play"
            if _button_clicked(event, settings_rect):
                result = show_settings(screen, clock)
                if result == "quit":
                    return "quit"

        screen.blit(background, (0, 0))

        _draw_box(screen, title_rect, "PyDangeon", font_title, (100, 200, 255), (100, 200, 255))

        # При наведении кнопки будут подсвечиваться голубым цветом
        play_border = (100, 200, 255) if play_hovered else WHITE
        play_text = (100, 200, 255) if play_hovered else WHITE
        _draw_box(screen, play_rect, "играть", font_button, play_border, play_text)

        settings_border = (100, 200, 255) if settings_hovered else WHITE
        settings_text = (100, 200, 255) if settings_hovered else WHITE
        _draw_box(screen, settings_rect, "настройки", font_button, settings_border, settings_text)

        pygame.display.flip()
        clock.tick(FPS)
