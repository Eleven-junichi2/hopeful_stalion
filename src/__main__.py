from pathlib import Path
import sys

import pygame

GAME_TITLE = "Hopeful stalion"
MAIN_PRG_DIR = Path(__file__).absolute().parent
SCRN_WIDTH = 768  # 512*1.5
SCRN_HEIGHT = 651  # 434*1.5
SCRN_SIZE = SCRN_WIDTH, SCRN_HEIGHT
BLACK = 0, 0, 0
WHITE = 255, 255, 255
KEY_REPEAT_DELAY = 125
KEY_REPEAT_INTERVAL = 125

class Game:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode(SCRN_SIZE)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()
            clock.tick(60)


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
    