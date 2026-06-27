import pygame
from settings import *
from tilemap import *
from player import *
from enemy import *
from menu import show_main_menu


def run_game(screen, clock):
    tilemap = TileMap()
    player = Player(tilemap, start_x=1, start_y=1)
    enemy = Enemy(x=5, y=5, tilemap=tilemap)
    enemy2 = Enemy(x=10, y=10, tilemap=tilemap)
    enemy3 = Enemy(x=15, y=15, tilemap=tilemap)
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.handle_event(event, enemy, enemy2, enemy3)

        screen.fill(DARK_GREY)

        enemy.update(player)
        enemy2.update(player)
        enemy3.update(player)
        tilemap.draw(screen, player)
        tilemap.draw(screen, tilemap)

        player.draw(screen)
        enemy.draw(screen)
        enemy2.draw(screen)
        enemy3.draw(screen)

        pygame.display.flip()


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("PyDangeon")
    clock = pygame.time.Clock()

    if show_main_menu(screen, clock) == "play":
        run_game(screen, clock)

    pygame.quit()


if __name__ == "__main__":
    main()
