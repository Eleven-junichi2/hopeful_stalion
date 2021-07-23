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
TARGET_FPS = 60
WHITE = (255, 255, 255)
asset_dir = MAIN_PRG_DIR / "assets"
font_dir = asset_dir / "font"
image_dir = asset_dir / "image"
sound_dir = asset_dir / "sound"
music_dir = sound_dir / "music"
sound_effect_dir = sound_dir / "se"


class Game:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode(SCRN_SIZE)
        self.clock = pygame.time.Clock()
        self.gametext = {}  # TODO: make masterdata of text and translation

    def run(self) -> None:
        pygame.mixer.init(frequency=44100)
        pygame.mixer.music.load(str(music_dir / "hopeful_stalion_theme.ogg"))

        font_title = pygame.font.Font(str(font_dir / "misaki_gothic.ttf"), 48)

        text_title = "ホープフルスタリオン"
        text_surface_title = font_title.render(
            text_title, False, WHITE)
        text_title_pos = [SCRN_WIDTH / 2 - font_title.size(
            text_title)[0] / 2, SCRN_HEIGHT / 2 - font_title.size(text_title)[1]]
        title_was_being_showed = False
        title_showing_delta_frame = 0
        title_showing_interval = 2

        font_titlemenu = pygame.font.Font(
            str(font_dir / "misaki_gothic.ttf"), 24)
        text_titlemenu = {"start_game": {"text": "スタート", "pos": None},
                          "game_config": {"text": "設定", "pos": None},
                          "exit": {"text": "終了", "pos": None}}
        text_titlemenu["start_game"]["pos"] = [
            SCRN_WIDTH / 2.1 - font_titlemenu.size(
                text_titlemenu["start_game"]["text"])[0] / 2,
            SCRN_HEIGHT / 3 + font_titlemenu.size(text_titlemenu["start_game"]["text"])[1]]
        text_titlemenu["game_config"]["pos"] = [
            text_titlemenu["start_game"]["pos"][0],
            text_titlemenu["start_game"]["pos"][1] + 16 + font_titlemenu.size(text_titlemenu["game_config"]["text"][1])[1]]
        text_titlemenu["exit"]["pos"] = [
            text_titlemenu["start_game"]["pos"][0],
            text_titlemenu["game_config"]["pos"][1] + 16 + font_titlemenu.size(text_titlemenu["exit"]["text"][1])[1]]
        text_surface_start_game = font_titlemenu.render(
            text_titlemenu["start_game"]["text"], False, WHITE)
        text_surface_game_config = font_titlemenu.render(
            text_titlemenu["game_config"]["text"], False, WHITE)
        text_surface_exit = font_titlemenu.render(
            text_titlemenu["exit"]["text"], False, WHITE)

        titlemenu_keys = list(text_titlemenu.keys())
        titlemenu_list_max_index = len(titlemenu_keys) - 1

        font_menu_cursor = pygame.font.Font(
            str(font_dir / "misaki_gothic.ttf"), 24)
        text_menu_cursor = "->"
        current_menu_choice: int = 0
        text_surface_menu_cursor = font_titlemenu.render(
            text_menu_cursor, False, WHITE)
        def text_menu_cursor_pos():
            return [text_titlemenu["start_game"]["pos"][0] - font_menu_cursor.size(
                        text_menu_cursor)[0], text_titlemenu[titlemenu_keys[current_menu_choice]]["pos"][1]]
        # TODO: make scene transition
        while True:
            self.screen.fill((0, 0, 0))
            dt = self.clock.tick(60) * 0.001 * TARGET_FPS  # delta time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and current_menu_choice > 0:
                        current_menu_choice -= 1
                    elif event.key == pygame.K_DOWN and current_menu_choice < titlemenu_list_max_index:
                        current_menu_choice += 1
                    elif event.key == pygame.K_z:
                        if titlemenu_keys[current_menu_choice] == "exit":
                            sys.exit()
            if not title_was_being_showed:
                title_showing_delta_frame += 1
                if title_showing_delta_frame % title_showing_interval == 0:
                    text_title_pos[1] -= 5 * dt
                if text_title_pos[1] <= SCRN_HEIGHT / 5:
                    pygame.mixer.music.play(-1, fade_ms=7800)
                    title_was_being_showed = True
            if title_was_being_showed:
                self.screen.blit(text_surface_start_game,
                                 text_titlemenu["start_game"]["pos"])
                self.screen.blit(text_surface_game_config,
                                 text_titlemenu["game_config"]["pos"])
                self.screen.blit(text_surface_exit,
                                 text_titlemenu["exit"]["pos"])
                self.screen.blit(text_surface_menu_cursor,
                                 text_menu_cursor_pos())
            self.screen.blit(text_surface_title, text_title_pos)
            pygame.display.update()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
