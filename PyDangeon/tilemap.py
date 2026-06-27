import pygame
from settings import *

# Эти числа — "тип" каждой клетки на карте
# Мы используем числа, потому что компьютеру легче сравнивать числа чем текст
TILE_WALL = 0  # стена
TILE_DOOR = 1  # дверь
TILE_FLOOR = 3  # пол

# Карта нашего подземелья — список строк
# '#' = стена, '.' = пол
# Это удобно читать глазами — сразу видно как выглядит уровень!
MAP_DATA = [
    "####################",
    "#..................#",
    "#..................#",
    "#.....##...........#",
    "#..................#",
    "#..................#",
    "#..######..........#",
    "#.........##.......#",
    "#..................#",
    "D...................",
    "#...........######.#",
    "#..................#",
    "#..................#",
    "#....#######.......#",
    "#...................",
    "#..................#",
    "#.......####.......#",
    "#..................#",
    "#..................#",
    "####################",
]
MAP_DATA2 = [
    "####################",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "....................",
    "#..................#",
    "#..................#",
    "#..................#",
    "#....#######.......#",
    "#...................",
    "#..................#",
    "#.......####.......#",
    "#..................#",
    "#..................#",
    "####################",
]


def parse_map(map_data):
    tiles = []
    for row in map_data:
        tile_row = []
        for char in row:
            if char == "#":
                tile_row.append(TILE_WALL)
            elif char == "D":
                tile_row.append(TILE_DOOR)
            else:
                tile_row.append(TILE_FLOOR)
        tiles.append(tile_row)
    return tiles


class TileMap:
    def __init__(self):
        # Превращаем строки с '#' и '.' в числа (0 и 3)
        # Так потом проще проверять — стена это или пол
        self.maps = [parse_map(MAP_DATA), parse_map(MAP_DATA2)]
        self.current_map = 0

        self.image = pygame.transform.scale(
            pygame.image.load("assets/images/picture_stone.png").convert_alpha(),
            (TILE_SIZE, TILE_SIZE),
        )
        self.image2 = pygame.transform.scale(
            pygame.image.load("assets/images/wood_floor.png").convert_alpha(),
            (TILE_SIZE, TILE_SIZE),
        )
        self.image3 = pygame.transform.scale(
            pygame.image.load("assets/images/picture_door.png").convert_alpha(),
            (TILE_SIZE, TILE_SIZE),
        )

    def is_wall(self, x, y):
        tiles = self.maps[self.current_map]
        return tiles[y][x] == TILE_WALL

    def draw(self, screen, player):
        tiles = self.maps[self.current_map]
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                tile = tiles[y][x]

                px = x * TILE_SIZE
                py = y * TILE_SIZE

                if tile == TILE_WALL:
                    screen.blit(self.image, (px, py))
                elif tile == TILE_DOOR:
                    screen.blit(self.image3, (px, py))
                else:
                    screen.blit(self.image2, (px, py))

