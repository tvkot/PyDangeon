import pygame
import random
from settings import *

TILE_WALL = 0
TILE_DOOR = 1
TILE_FLOOR = 3


class MapGenerator:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def generate(self):

        # Вся карта изначально состоит из стен
        map_data = [
            [TILE_WALL for _ in range(self.width)]
            for _ in range(self.height)
        ]

        rooms = []

        # ==============================
        # НАСТРОЙКИ КОМНАТ
        # ==============================

        max_rooms = 10

        min_room_width = 4
        max_room_width = 8

        min_room_height = 5
        max_room_height = 9

        attempts = 100

        # ==============================
        # СОЗДАНИЕ КОМНАТ
        # ==============================

        for _ in range(attempts):

            room_width = random.randint(
                min_room_width,
                max_room_width
            )

            room_height = random.randint(
                min_room_height,
                max_room_height
            )

            # Защита от слишком маленькой карты
            if self.width <= room_width + 2:
                continue

            if self.height <= room_height + 2:
                continue

            x = random.randint(
                1,
                self.width - room_width - 2
            )

            y = random.randint(
                1,
                self.height - room_height - 2
            )

            new_room = (
                x,
                y,
                room_width,
                room_height
            )

            # ==============================
            # ПРОВЕРКА ПЕРЕСЕЧЕНИЯ
            # ==============================

            overlaps = False

            for other_room in rooms:

                ox, oy, ow, oh = other_room

                if (
                        x < ox + ow + 1
                        and x + room_width + 1 > ox
                        and y < oy + oh + 1
                        and y + room_height + 1 > oy
                ):
                    overlaps = True
                    break

            if overlaps:
                continue

            # ==============================
            # РИСУЕМ КОМНАТУ
            # ==============================

            for room_y in range(
                    y,
                    y + room_height
            ):

                for room_x in range(
                        x,
                        x + room_width
                ):
                    map_data[room_y][room_x] = TILE_FLOOR

            rooms.append(new_room)

            if len(rooms) >= max_rooms:
                break

        # ==============================
        # СОЕДИНЯЕМ КОМНАТЫ
        # КОРИДОР ШИРИНОЙ 2 КЛЕТКИ
        # ==============================

        for i in range(1, len(rooms)):

            previous_room = rooms[i - 1]
            current_room = rooms[i]

            previous_x = (
                    previous_room[0]
                    + previous_room[2] // 2
            )

            previous_y = (
                    previous_room[1]
                    + previous_room[3] // 2
            )

            current_x = (
                    current_room[0]
                    + current_room[2] // 2
            )

            current_y = (
                    current_room[1]
                    + current_room[3] // 2
            )

            # ==============================
            # СНАЧАЛА X
            # ==============================

            if random.choice([True, False]):

                for x in range(
                        min(previous_x, current_x),
                        max(previous_x, current_x) + 1
                ):

                    for offset in (0, 1):

                        yy = previous_y + offset

                        if (
                                0 <= yy < self.height
                                and 0 <= x < self.width
                        ):
                            map_data[yy][x] = TILE_FLOOR

                for y in range(
                        min(previous_y, current_y),
                        max(previous_y, current_y) + 1
                ):

                    for offset in (0, 1):

                        xx = current_x + offset

                        if (
                                0 <= y < self.height
                                and 0 <= xx < self.width
                        ):
                            map_data[y][xx] = TILE_FLOOR

            # ==============================
            # СНАЧАЛА Y
            # ==============================

            else:

                for y in range(
                        min(previous_y, current_y),
                        max(previous_y, current_y) + 1
                ):

                    for offset in (0, 1):

                        xx = previous_x + offset

                        if (
                                0 <= y < self.height
                                and 0 <= xx < self.width
                        ):
                            map_data[y][xx] = TILE_FLOOR

                for x in range(
                        min(previous_x, current_x),
                        max(previous_x, current_x) + 1
                ):

                    for offset in (0, 1):

                        yy = current_y + offset

                        if (
                                0 <= yy < self.height
                                and 0 <= x < self.width
                        ):
                            map_data[yy][x] = TILE_FLOOR

        return map_data, rooms


# ==========================================================
# TILE MAP
# ==========================================================

class TileMap:

    def __init__(self):

        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT

        # Генерируем карту
        generator = MapGenerator(
            self.width,
            self.height
        )

        self.map_data, self.rooms = generator.generate()

        # ==============================
        # ЗАГРУЖАЕМ ТЕКСТУРЫ
        # ==============================

        self.floor_image = pygame.image.load(
            "assets/images/wood_floor.png"
        ).convert()

        self.wall_image = pygame.image.load(
            "assets/images/picture_stone.png"
        ).convert()

        # Масштабируем под размер клетки
        self.floor_image = pygame.transform.scale(
            self.floor_image,
            (TILE_SIZE, TILE_SIZE)
        )

        self.wall_image = pygame.transform.scale(
            self.wall_image,
            (TILE_SIZE, TILE_SIZE)
        )

    # ======================================================
    # ТЕПЕРЬ МЕТОД НА СВОЕМ МЕСТЕ (Вне __init__)
    # ======================================================
    def get_safe_cell_position(self):
        """
        Ищет случайную клетку на карте. Если это пол,
        возвращает её координаты в виде (x, y) без перевода в пиксели.
        """
        while True:
            # Выбираем случайную клетку в пределах карты
            spawn_x = random.randint(0, self.width - 1)
            spawn_y = random.randint(0, self.height - 1)

            # Если по ней можно ходить — возвращаем индексы клеток
            if self.is_walkable(spawn_x, spawn_y):
                return spawn_x, spawn_y

    # ======================================================
    # ПРОВЕРКА ПРОХОДИМОСТИ
    # ======================================================

    def is_walkable(self, x, y):

        if x < 0 or x >= self.width:
            return False

        if y < 0 or y >= self.height:
            return False

        return self.map_data[y][x] in (
            TILE_FLOOR,
            TILE_DOOR
        )

    def is_wall(self, x, y):

        if x < 0 or x >= self.width:
            return True

        if y < 0 or y >= self.height:
            return True

        return self.map_data[y][x] == TILE_WALL

    # ======================================================
    # ОТРИСОВКА КАРТЫ
    # ======================================================

    def draw(self, surface, player=None):

        for y in range(self.height):

            for x in range(self.width):

                tile = self.map_data[y][x]

                position = (
                    x * TILE_SIZE,
                    y * TILE_SIZE
                )

                # ==========================
                # ПОЛ
                # ==========================

                if tile == TILE_FLOOR:

                    surface.blit(
                        self.floor_image,
                        position
                    )

                # ==========================
                # СТЕНА
                # ==========================

                else:

                    surface.blit(
                        self.wall_image,
                        position
                    )
