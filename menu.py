import pygame
from settings import *


def _draw_box(surface, rect, text, font, border_color=GREY, text_color=BLACK):
    pygame.draw.rect(surface, RED, rect)
    pygame.draw.rect(surface, border_color, rect, 3, border_radius=10)
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

    back_rect = pygame.Rect(SCREEN_W // 2 - 100, SCREEN_H - 120, 200, 60)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        back_hovered = back_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if _button_clicked(event, back_rect):
                return "menu"

        screen.fill(DARK_GREY)

        title_rect = pygame.Rect(SCREEN_W // 2 - 160, 80, 320, 70)
        _draw_box(screen, title_rect, "Настройки", font_title)

        hint_font = pygame.font.SysFont(None, 32)
        hint = hint_font.render("Скоро здесь будут настройки", True, RED)
        screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 280))

        border = YELLOW if back_hovered else GREY
        _draw_box(screen, back_rect, "назад", font_button, border, YELLOW if back_hovered else BLACK)

        pygame.display.flip()
        clock.tick(FPS)


def show_main_menu(screen, clock):
    font_title = pygame.font.SysFont(None, 64)
    font_button = pygame.font.SysFont(None, 44)

    title_rect = pygame.Rect(SCREEN_W // 2 - 160, 70, 320, 80)
    play_rect = pygame.Rect(80, 320, 200, 70)
    settings_rect = pygame.Rect(SCREEN_W - 280, 320, 200, 70)

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

        screen.fill(GREY)

        _draw_box(screen, title_rect, "PyDangeon", font_title, GREY, BLACK)

        play_border = YELLOW if play_hovered else GREY
        play_text = BLUE if play_hovered else BLACK
        _draw_box(screen, play_rect, "играть", font_button, play_border, play_text)

        settings_border = YELLOW if settings_hovered else GREY
        settings_text = BLUE if settings_hovered else BLACK
        _draw_box(screen, settings_rect, "настройки", font_button, settings_border, settings_text)

        pygame.display.flip()
        clock.tick(FPS)
