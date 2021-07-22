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
asset_dir = MAIN_PRG_DIR / "assets"
font_dir = asset_dir / "font"
image_dir = asset_dir / "image"


class Game:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode(SCRN_SIZE)

    def run(self) -> None:
        clock = pygame.time.Clock()

        font = pygame.font.Font(str(font_dir / "misaki_gothic.ttf"), 48)
        text_title = "ホープフルスタリオン"
        text_surface_title = font.render(text_title, False, (255, 255, 255))
        text_title_pos = [SCRN_WIDTH / 2 - font.size(
            text_title)[0] / 2, SCRN_HEIGHT / 2 - font.size(text_title)[1]]
        title_was_being_showed = False
        title_showing_delta_time = 0
        title_showing_interval = 2

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if not title_was_being_showed:
                title_showing_delta_time += 1
                if title_showing_delta_time % title_showing_interval == 0:
                    text_title_pos[1] -= 5
                if text_title_pos[1] <= SCRN_HEIGHT / 5:
                    title_was_being_showed = True

            self.screen.fill((0, 0, 0))
            self.screen.blit(text_surface_title, text_title_pos)
            pygame.display.update()
            clock.tick(60)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
