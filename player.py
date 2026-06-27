import pygame
from settings import *


def _load_sound(*paths):
    for path in paths:
        try:
            return pygame.mixer.Sound(path)
        except pygame.error:
            continue
    return None


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
        self.size = TILE_SIZE - -20

        # Цвет игрока — синий
        self.color = BLUE

        self.image = pygame.image.load("assets/images/picture_player.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.attack_sound = _load_sound("assets/sounds/sound_hit.mp3")
        self.step_sound = _load_sound(
            "assets/sounds/sound_walking.mp3",
            "assets/sounds/sound_fast_walking.mp3",
        )

    def is_adjacent(self, other_x, other_y):
        dx = abs(self.x - other_x)
        dy = abs(self.y - other_y)
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    def attack(self, enemy, enemy2, enemy3):
        for target in (enemy, enemy2, enemy3):
            if target.alive and self.is_adjacent(target.x, target.y):
                if self.attack_sound:
                    self.attack_sound.play()
                target.take_damage(1.5)
                break

    def move(self, dx, dy, enemy, enemy2, enemy3):
        # dx — шаг по горизонтали (-1 влево, +1 вправо, 0 стоим)
        # dy — шаг по вертикали   (-1 вверх,  +1 вниз,   0 стоим)

        # Считаем куда ХОТИМ пойти
        new_x = self.x + dx
        new_y = self.y + dy

        if enemy.alive and new_x == enemy.x and new_y == enemy.y:
            enemy.take_damage(1)
            return

        # Проверяем: там не стена? Тогда идём!
        # Если там стена — просто ничего не делаем
        if not self.tilemap.is_wall(new_x, new_y):
            self.x = new_x
            self.y = new_y
            if self.step_sound:
                self.step_sound.play()

    def handle_event(self, event, enemy, enemy2, enemy3):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move(-1, 0, enemy, enemy2, enemy3)
            if event.key == pygame.K_RIGHT:
                self.move(1, 0, enemy, enemy2, enemy3)
            if event.key == pygame.K_UP:
                self.move(0, -1, enemy, enemy2, enemy3)
            if event.key == pygame.K_DOWN:
                self.move(0, 1, enemy, enemy2, enemy3)
            if event.key == pygame.K_SPACE:
                self.attack(enemy, enemy2, enemy3)

    def draw(self, screen):
        offset = (TILE_SIZE - self.size) // 2
        px = self.x * TILE_SIZE + offset
        py = self.y * TILE_SIZE + offset

        screen.blit(self.image, (px, py))