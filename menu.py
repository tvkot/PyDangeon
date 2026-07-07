import pygame
from settings import *
import settings as game_settings

MENU_PICTURE = "assets/images/menu_wolf.png"
# Путь к аудиофайлу с цикадами (поддерживаются форматы .mp3, .ogg, .wav)
MENU_SOUND = "assets/sounds/cicadas-and-crickets.mp3"


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

    title_w, title_h = 320, 70
    button_w, button_h = 220, 70
    gap = 40

    while True:
        sw, sh = screen.get_size()

        total_h = title_h + gap + 40 + gap + button_h
        start_y = sh // 2 - total_h // 2
        title_rect = pygame.Rect(sw // 2 - title_w // 2, start_y, title_w, title_h)
        sound_rect = pygame.Rect(sw // 2 - 110, start_y + title_h + gap, 220, 60)
        size_rect = pygame.Rect(sw // 2 - 110, start_y + title_h + gap + 80, 220, 60)

        back_rect = pygame.Rect(
            sw // 2 - button_w // 2,
            start_y + title_h + gap + 150 + gap,
            button_w,
            button_h,
        )

        mouse_pos = pygame.mouse.get_pos()
        back_hovered = back_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
            if _button_clicked(event, back_rect):
                return "menu"
            if _button_clicked(event, sound_rect):
                game_settings.sound_enabled = not game_settings.sound_enabled
                # Мгновенно включаем или выключаем звук прямо в меню настроек
                if game_settings.sound_enabled:
                    try:
                        pygame.mixer.music.play(-1)  # -1 означает бесконечный повтор
                    except pygame.error:
                        pass
                else:
                    pygame.mixer.music.stop()

            if _button_clicked(event, size_rect):
                if game_settings.screen_size == "big":
                    game_settings.screen_size = "small"
                else:
                    game_settings.screen_size = "big"
                return "resize"

        screen.fill((15, 25, 45))

        _draw_box(screen, title_rect, "Настройки", font_title, (100, 200, 255), (255, 0, 0))
        if game_settings.sound_enabled:
            sound_text = "Звук: вкл."
        else:
            sound_text = "Звук: выкл."

        if game_settings.screen_size == "big":
            size_text = "Размер: большой"
        else:
            size_text = "Размер: маленький"

        _draw_box(screen, sound_rect, sound_text, font_button, WHITE, WHITE)
        _draw_box(screen, size_rect, size_text, font_button, WHITE, WHITE)

        border = (100, 200, 255) if back_hovered else WHITE
        text_col = (255, 0, 0) if back_hovered else WHITE
        _draw_box(screen, back_rect, "назад", font_button, border, text_col)

        pygame.display.flip()
        clock.tick(FPS)


def show_main_menu(screen, clock):
    font_title = pygame.font.SysFont(None, 64)
    font_button = pygame.font.SysFont(None, 44)
    background = _load_menu_background(screen)

    # Загружаем и запускаем эмбиент цикад при входе в главное меню
    try:
        pygame.mixer.music.load(MENU_SOUND)
        if game_settings.sound_enabled:
            pygame.mixer.music.play(-1)  # Зацикливание звука
    except pygame.error:
        print(f"Предупреждение: Не удалось загрузить аудиофайл {MENU_SOUND}")

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
                pygame.mixer.music.stop()  # Глушим звук при выходе из игры
                return "quit"
            if _button_clicked(event, play_rect):
                pygame.mixer.music.stop()  # Глушим цикад перед переходом в саму игру
                return "play"
            if _button_clicked(event, settings_rect):
                result = show_settings(screen, clock)
                if result in ("quit", "resize"):
                    pygame.mixer.music.stop()
                    return result

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
