import pygame
import settings as game_settings
from settings import *


def _load_sound(*paths):
    for path in paths:
        try:
            return pygame.mixer.Sound(path)
        except pygame.error:
            continue
    return None


class Player:
    def __init__(self, tilemap, start_x, start_y, character):
        self.tilemap = tilemap

        self.x = start_x
        self.y = start_y

        self.alive = True

        self.hp = 10
        self.last_hit_time = 0
        self.hit_cooldown = 1000

        self.size = TILE_SIZE + 20

        if character == "knight":
            image_path = "assets/images/picture_player.png"
        elif character == "thief":
            image_path = "assets/images/pictue_thief.png"
        else:
            image_path = "assets/images/picture_player.png"

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.attack_sound = _load_sound("assets/sounds/sound_hit.mp3")
        self.step_sound = _load_sound(
            "assets/sounds/sound_walking.mp3",
            "assets/sounds/sound_fast_walking.mp3",
        )
        self.door_sound = _load_sound("assets/sounds/sound_door.mp3")

    def is_adjacent(self, other_x, other_y):
        dx = abs(self.x - other_x)
        dy = abs(self.y - other_y)
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    def attack(self, enemy, enemy2, enemy3):
        for target in (enemy, enemy2, enemy3):
            if target.alive and self.is_adjacent(target.x, target.y):
                if game_settings.sound_enabled and self.attack_sound:
                    self.attack_sound.play()
                target.take_damage(0.5)
                break

    def move(self, dx, dy, enemy, enemy2, enemy3):
        # dx — шаг по горизонтали (-1 влево, +1 вправо, 0 стоим)
        # dy — шаг по вертикали   (-1 вверх,  +1 вниз,   0 стоим)

        # Считаем куда ХОТИМ пойти
        new_x = self.x + dx
        new_y = self.y + dy

        if enemy.alive and new_x == enemy.x and new_y == enemy.y:
            return

        if enemy2.alive and new_x == enemy2.x and new_y == enemy2.y:
            return

        if enemy3.alive and new_x == enemy3.x and new_y == enemy3.y:
            return

        # Проверяем: там не стена? Тогда идём!
        # Если там стена — просто ничего не делаем
        if not self.tilemap.is_wall(new_x, new_y):
            self.x = new_x
            self.y = new_y
            if self.tilemap.is_door(self.x, self.y):
                if game_settings.sound_enabled and self.door_sound:
                    self.door_sound.play()
                if self.tilemap.current_map == 0:
                    self.tilemap.switch_map(1, self)
                else:
                    self.tilemap.switch_map(0, self)
            if game_settings.sound_enabled and self.step_sound:
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

    def take_damage(self, damage):
        now = pygame.time.get_ticks()

        if now - self.last_hit_time < self.hit_cooldown:
            return

        self.last_hit_time = now
        self.hp -= damage

        print(f"HP: {self.hp}")

        if self.hp <= 0:
            self.alive = False
