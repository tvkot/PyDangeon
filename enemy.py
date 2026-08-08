import pygame
from settings import *


class Enemy:
    def __init__(self, x, y, tilemap):
        self.x = x
        self.y = y

        self.size = TILE_SIZE + 20

        self.color = RED
        self.hp = 3
        self.alive = True

        self.image = pygame.image.load("assets/images/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        for x in range(self.image.get_width()):
            for y in range(self.image.get_height()):
                r, g, b, a = self.image.get_at((x, y))
                if r > 200 and g > 200 and b > 200:
                    self.image.set_at((x, y), (0, 0, 0, 0))

        self.last_move_time = pygame.time.get_ticks()
        self.move_delay = 250

        self.tilemap = tilemap

    def update(self, player):
        if not self.alive:
            return

        now = pygame.time.get_ticks()

        if now - self.last_move_time < self.move_delay:
            return

        self.last_move_time = now

        # Если враг уже рядом с игроком — атакует
        distance = abs(player.x - self.x) + abs(player.y - self.y)

        if distance == 1:
            player.take_damage(2)
            return

        dx = 0
        dy = 0

        if player.x > self.x:
            dx = 1
        elif player.x < self.x:
            dx = -1

        if player.y > self.y:
            dy = 1
        elif player.y < self.y:
            dy = -1

        new_x = self.x + dx
        new_y = self.y + dy

        if dx != 0 and not self.tilemap.is_wall(new_x, self.y):
            self.x = new_x
        elif dy != 0 and not self.tilemap.is_wall(self.x, new_y):
            self.y = new_y

    def draw(self, screen):
        if not self.alive:
            return

        offset = (TILE_SIZE - self.size) // 2
        px = self.x * TILE_SIZE + offset
        py = self.y * TILE_SIZE + offset

        screen.blit(self.image, (px, py))

    def take_damage(self, damage):
        self.hp -= damage

        if self.hp <= 0:
            self.alive = False
            print("Враг убит")
