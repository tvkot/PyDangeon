import pygame
import settings as game_settings
from settings import *

MENU_PICTURE = "assets/images/menu_wolf.png"
MENU_SOUND = "assets/sounds/cicadas-and-crickets.mp3"
scream_picture2 = pygame.image.load("assets/images/picture_bg.jpg")
MENU_PLAYER_SOUND = "assets/images/wind.mp3"
def _load_menu_background(screen):
    sw, sh = screen.get_size()
    image = pygame.image.load(MENU_PICTURE).convert()
    img_w, img_h = image.get_size()

    scale = max(sw / img_w, sh / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    scaled = pygame.transform.smoothscale(image, (new_w, new_h))

    background = pygame.Surface((sw, sh))
    background.fill((15, 25, 45))
    background.blit(scaled, ((sw - new_w) // 2, (sh - new_h) // 2))
    return background


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
    button_w, button_h = 220, 60
    gap = 24

    while True:
        mouse = pygame.mouse.get_pos()
        sw, sh = screen.get_size()

        total_h = title_h + gap + button_h + gap + button_h + gap + button_h
        start_y = sh // 2 - total_h // 2

        title_rect = pygame.Rect(sw // 2 - title_w // 2, start_y, title_w, title_h)
        sound_rect = pygame.Rect(sw // 2 - button_w // 2, start_y + title_h + gap, button_w, button_h)
        size_rect = pygame.Rect(
            sw // 2 - button_w // 2,
            start_y + title_h + gap + button_h + gap,
            button_w,
            button_h,
        )
        back_rect = pygame.Rect(
            sw // 2 - button_w // 2,
            start_y + title_h + gap + button_h + gap + button_h + gap,
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

                if game_settings.sound_enabled:
                    try:
                        pygame.mixer.music.play(-1)
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

        _draw_box(screen, title_rect, "Настройки", font_title, (100, 200, 255), (100, 200, 255))

        sound_text = "звук: вкл" if game_settings.sound_enabled else "звук: выкл"
        size_text = "экран: большой" if game_settings.screen_size == "big" else "экран: маленький"

        _draw_box(screen, sound_rect, sound_text, font_button, WHITE, WHITE)
        _draw_box(screen, size_rect, size_text, font_button, WHITE, WHITE)

        border = (100, 200, 255) if back_hovered else WHITE
        text_col = (100, 200, 255) if back_hovered else WHITE
        _draw_box(screen, back_rect, "назад", font_button, border, text_col)

        pygame.display.flip()
        clock.tick(FPS)


def show_main_menu(screen, clock):
    font_title = pygame.font.SysFont(None, 64)
    font_button = pygame.font.SysFont(None, 44)

    try:
        pygame.mixer.music.load(MENU_SOUND)
        if game_settings.sound_enabled:
            pygame.mixer.music.play(-1)
    except pygame.error:
        print(f"Предупреждение: не удалось загрузить {MENU_SOUND}")

    title_w, title_h = 320, 80
    button_w, button_h = 220, 70
    gap = 24

    while True:
        sw, sh = screen.get_size()
        background = _load_menu_background(screen)

        total_h = title_h + gap + button_h + gap + button_h + gap + button_h
        start_y = sh // 2 - total_h // 2

        title_rect = pygame.Rect(sw // 2 - title_w // 2, start_y, title_w, title_h)
        play_rect = pygame.Rect(sw // 2 - button_w // 2, start_y + title_h + gap, button_w, button_h)
        settings_rect = pygame.Rect(
            sw // 2 - button_w // 2,
            start_y + title_h + gap + button_h + gap,
            button_w,
            button_h,
        )
        exit_rect = pygame.Rect(sw // 2 - title_w // 2, start_y + 295, title_w, title_h)

        mouse_pos = pygame.mouse.get_pos()
        play_hovered = play_rect.collidepoint(mouse_pos)
        settings_hovered = settings_rect.collidepoint(mouse_pos)
        exit_hovered = exit_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "quit"

            if _button_clicked(event, play_rect):
                result, character = show_character_selection(screen, clock)

                if result == "quit":
                    return "quit"

                if result == "menu":
                    break

                if result == "play":
                    return "play", character

            if _button_clicked(event, exit_rect):
                pygame.mixer.music.stop()
                return "quit"

            if _button_clicked(event, settings_rect):
                result = show_settings(screen, clock)

                if game_settings.sound_enabled:
                    try:
                        pygame.mixer.music.load("assets/sounds/dungeon_ambient.mp3")
                        pygame.mixer.music.play(-1)
                    except pygame.error:
                        pass

                if result == "quit":
                    pygame.mixer.music.stop()
                    return "quit"

                if result == "resize":
                    pygame.mixer.music.stop()
                    return "resize"

                if game_settings.sound_enabled:
                    try:
                        pygame.mixer.music.play(-1)
                    except pygame.error:
                        pass

        screen.fill((15, 25, 45))
        screen.blit(background, (0, 0))

        _draw_box(screen, title_rect, "PyDangeon", font_title, (100, 200, 255), (100, 200, 255))

        play_border = (100, 200, 255) if play_hovered else WHITE
        play_text = (100, 200, 255) if play_hovered else WHITE
        exit_border = (100, 200, 255) if exit_hovered else WHITE
        exit_text_col = (100, 200, 255) if exit_hovered else WHITE

        _draw_box(screen, play_rect, "играть", font_button, play_border, play_text)
        _draw_box(screen, settings_rect, "настройки", font_button,
                  (100, 200, 255) if settings_hovered else WHITE,
                  (100, 200, 255) if settings_hovered else WHITE)
        _draw_box(screen, exit_rect, "выход", font_button, exit_border, exit_text_col)

        pygame.display.flip()
        clock.tick(FPS)


def show_character_selection(screen, clock):
    font_title = pygame.font.SysFont(None, 56)
    font_button = pygame.font.SysFont(None, 40)
    if game_settings.sound_enabled:
        try:
            pygame.mixer.music.load("assets/sounds/wind.mp3")
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    title_w, title_h = 400, 70
    button_w, button_h = 260, 60
    gap = 20

    while True:
        mouse = pygame.mouse.get_pos()
        sw, sh = screen.get_size()

        total_h = title_h + gap + button_h * 3 + gap * 2
        start_y = sh // 2 - total_h // 2

        title_rect = pygame.Rect(
            sw // 2 - title_w // 2,
            start_y,
            title_w,
            title_h,
        )

        knight_rect = pygame.Rect(
            sw // 2 - button_w // 2,
            start_y + title_h + gap,
            button_w,
            button_h,
        )

        thief_rect = pygame.Rect(
            sw // 2 - button_w // 2,
            knight_rect.bottom + gap,
            button_w,
            button_h,
        )

        back_rect = pygame.Rect(
            sw // 2 - button_w // 2,
            thief_rect.bottom + gap,
            button_w,
            button_h,
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "quit", None

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu", None

            if _button_clicked(event, knight_rect):
                pygame.mixer.music.stop()
                return "play", "knight"

            if _button_clicked(event, thief_rect):
                pygame.mixer.music.stop()
                return "play", "thief"

            if _button_clicked(event, back_rect):
                return "menu", None

        bg = pygame.transform.smoothscale(
            scream_picture2,
            screen.get_size()
        )

        screen.blit(bg, (0, 0))

        _draw_box(
            screen,
            title_rect,
            "Выберите персонажа",
            font_title,
            (100, 200, 255),
            (100, 200, 255),
        )

        _draw_box(
            screen,
            knight_rect,
            "Рыцарь",
            font_button,
            (100, 200, 255) if knight_rect.collidepoint(mouse) else WHITE,
            (100, 200, 255) if knight_rect.collidepoint(mouse) else WHITE,
        )

        _draw_box(
            screen,
            thief_rect,
            "Вор",
            font_button,
            (100, 200, 255) if thief_rect.collidepoint(mouse) else WHITE,
            (100, 200, 255) if thief_rect.collidepoint(mouse) else WHITE,
        )

        _draw_box(
            screen,
            back_rect,
            "Назад",
            font_button,
            (100, 200, 255) if back_rect.collidepoint(mouse) else WHITE,
            (100, 200, 255) if back_rect.collidepoint(mouse) else WHITE,
        )

        pygame.display.flip()
        clock.tick(FPS)
