from pathlib import Path
import sys
import json

import pygame

from gamesystem import scene_trans

GAME_TITLE = "Hopeful stalion"
MAIN_PRG_DIR = Path(__file__).absolute().parent
TRANSLATION_DIR = Path(__file__).parent / "translation"
CONFIG_PATH = MAIN_PRG_DIR / "config.json"
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


class GameConfig:
    def __init__(self):
        self.config = {}
        self.reload()

    def reload(self) -> dict:
        with open(str(CONFIG_PATH),
                  encoding="utf-8_sig") as f:
            self.config = json.load(f)


class GameLocalizedText:
    def __init__(self, language="jp"):
        self.language = language
        self.texts = {}
        with open(str(TRANSLATION_DIR / "jp.json"), "r",
                  encoding="utf-8_sig") as f:
            self.texts["jp"] = json.load(f)
        with open(str(TRANSLATION_DIR / "en.json"), "r",
                  encoding="utf-8_sig") as f:
            self.texts["en"] = json.load(f)

    def get_text(self, text_key) -> str:
        return self.texts[self.language][text_key]


class GameSceneManager(scene_trans.SceneManager):
    def __init__(self, screen: pygame.Surface, game):
        super().__init__()
        self.game = game

# TODO: make config scene
# TODO: make GameMenu class to refactoring code

class GameMenu:
    """This class makes it easier to code menu UI behavior."""


class ConfigScene(scene_trans.Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.font_menu_cursor = pygame.font.Font(
            str(font_dir / "misaki_gothic.ttf"), 24)
        self.text_menu_cursor = "->"
        self.current_menu_choice: int = 0
        self.text_surface_menu_cursor = self.font_menu_cursor.render(
            self.text_menu_cursor, False, WHITE)

        self.font_menu = pygame.font.Font(
            str(font_dir / "misaki_gothic.ttf"), 24)

        self.text_config_menu = {"cancel_config": {"text": self.sm.game.gametext.get_text("cancel_config"), "pos": None},
                                 "confirm_config": {"text": self.sm.game.gametext.get_text("confirm_config"), "pos": None},
                                 "lang": {"text": f"{self.sm.game.gametext.get_text('config_head_lang')}: {self.text_from_language_config()}", "pos": None}, }

        self.text_config_menu["cancel_config"]["pos"] = [SCRN_WIDTH / 2.5 - self.font_menu.size(self.text_config_menu["cancel_config"]["text"])[
            0] / 2, SCRN_HEIGHT / 4 - self.font_menu.size(self.text_config_menu["cancel_config"]["text"])[1] / 2]
        self.text_surface_cancel_config = self.font_menu.render(
            self.text_config_menu["cancel_config"]["text"], False, WHITE)

        self.text_config_menu["confirm_config"]["pos"] = [self.text_config_menu["cancel_config"]["pos"][0],
                                                          self.text_config_menu["cancel_config"]["pos"][1] + 8 + self.font_menu.size(self.text_config_menu["confirm_config"]["text"])[1]]
        self.text_surface_confirm_config = self.font_menu.render(
            self.text_config_menu["confirm_config"]["text"], False, WHITE)

        self.text_config_menu["lang"]["pos"] = [self.text_config_menu["cancel_config"]["pos"][0],
                                                self.text_config_menu["confirm_config"]["pos"][1] + 8 + self.font_menu.size(self.text_config_menu["lang"]["text"])[1]]
        self.text_surface_lang = self.font_menu.render(
            self.text_config_menu["lang"]["text"], False, WHITE)

        self.config_menu_keys = list(self.text_config_menu.keys())
        self.config_menu_list_max_index = len(self.config_menu_keys) - 1

    def text_from_language_config(self):
        language = self.sm.game.gameconfig.config["language"]
        if language == "jp":
            result = "日本語"
        elif language == "en":
            result = "English"
        return result

    def calc_menu_cursor_pos(self):
        return [self.text_config_menu["cancel_config"]["pos"][0] - self.font_menu_cursor.size(
            self.text_menu_cursor)[0], self.text_config_menu[self.config_menu_keys[self.current_menu_choice]]["pos"][1]]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.current_menu_choice > 0:
                self.current_menu_choice -= 1
            elif event.key == pygame.K_DOWN and self.current_menu_choice < self.config_menu_list_max_index:
                self.current_menu_choice += 1
            elif event.key == pygame.K_z:
                if self.config_menu_keys[self.current_menu_choice] == "cancel_config":
                    self.sm.set_current_scene("title")
                if self.config_menu_keys[self.current_menu_choice] == "confirm_config":
                    self.sm.set_current_scene("title")
                if self.config_menu_keys[self.current_menu_choice] == "lang":
                    pass

    def run(self, dt):
        self.sm.game.screen.fill((0, 0, 0))
        self.sm.game.screen.blit(
            self.text_surface_cancel_config, self.text_config_menu["cancel_config"]["pos"])
        self.sm.game.screen.blit(
            self.text_surface_confirm_config, self.text_config_menu["confirm_config"]["pos"])
        self.sm.game.screen.blit(
            self.text_surface_lang, self.text_config_menu["lang"]["pos"])
        # self.sm.game.screen.blit(
            # self.text_surface_lang, self.text_config_menu["volume"]["pos"])
        self.sm.game.screen.blit(self.text_surface_menu_cursor,
                                 self.calc_menu_cursor_pos())


class TitleScene(scene_trans.Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pygame.mixer.music.load(str(music_dir / "hopeful_stalion_theme.ogg"))

        self.font_title = pygame.font.Font(
            str(font_dir / "misaki_gothic.ttf"), 48)

        self.text_title = self.sm.game.gametext.get_text("title")
        self.text_surface_title = self.font_title.render(
            self.text_title, False, WHITE)
        self.text_title_pos = [SCRN_WIDTH / 2 - self.font_title.size(
            self.text_title)[0] / 2, SCRN_HEIGHT / 2 - self.font_title.size(self.text_title)[1]]
        self.title_was_being_showed = False
        self.title_showing_delta_frame = 0
        self.title_showing_interval = 2

        self.font_titlemenu = pygame.font.Font(
            str(font_dir / "misaki_gothic.ttf"), 24)
        self.text_titlemenu = {"start_game": {"text": self.sm.game.gametext.get_text("title_game_start"), "pos": None},
                               "game_config": {"text": self.sm.game.gametext.get_text("title_config"), "pos": None},
                               "exit": {"text": self.sm.game.gametext.get_text("title_exit"), "pos": None}}
        self.text_titlemenu["start_game"]["pos"] = [
            SCRN_WIDTH / 2.1 - self.font_titlemenu.size(
                self.text_titlemenu["start_game"]["text"])[0] / 2,
            SCRN_HEIGHT / 3 + self.font_titlemenu.size(self.text_titlemenu["start_game"]["text"])[1]]
        self.text_titlemenu["game_config"]["pos"] = [
            self.text_titlemenu["start_game"]["pos"][0],
            self.text_titlemenu["start_game"]["pos"][1] + 16 + self.font_titlemenu.size(self.text_titlemenu["game_config"]["text"][1])[1]]
        self.text_titlemenu["exit"]["pos"] = [
            self.text_titlemenu["start_game"]["pos"][0],
            self.text_titlemenu["game_config"]["pos"][1] + 16 + self.font_titlemenu.size(self.text_titlemenu["exit"]["text"][1])[1]]
        self.text_surface_start_game = self.font_titlemenu.render(
            self.text_titlemenu["start_game"]["text"], False, WHITE)
        self.text_surface_game_config = self.font_titlemenu.render(
            self.text_titlemenu["game_config"]["text"], False, WHITE)
        self.text_surface_exit = self.font_titlemenu.render(
            self.text_titlemenu["exit"]["text"], False, WHITE)

        self.titlemenu_keys = list(self.text_titlemenu.keys())
        self.titlemenu_list_max_index = len(self.titlemenu_keys) - 1

        self.font_menu_cursor = pygame.font.Font(
            str(font_dir / "misaki_gothic.ttf"), 24)
        self.text_menu_cursor = "->"
        self.current_menu_choice: int = 0
        self.text_surface_menu_cursor = self.font_titlemenu.render(
            self.text_menu_cursor, False, WHITE)

    def calc_menu_cursor_pos(self):
        return [self.text_titlemenu["start_game"]["pos"][0] - self.font_menu_cursor.size(
            self.text_menu_cursor)[0], self.text_titlemenu[self.titlemenu_keys[self.current_menu_choice]]["pos"][1]]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.current_menu_choice > 0:
                self.current_menu_choice -= 1
            elif event.key == pygame.K_DOWN and self.current_menu_choice < self.titlemenu_list_max_index:
                self.current_menu_choice += 1
            elif event.key == pygame.K_z:
                if self.titlemenu_keys[self.current_menu_choice] == "exit":
                    sys.exit()
                if self.titlemenu_keys[self.current_menu_choice] == "game_config":
                    self.sm.set_current_scene("config")

    def run(self, dt):
        self.sm.game.screen.fill((0, 0, 0))
        if not self.title_was_being_showed:
            self.title_showing_delta_frame += 1
            if self.title_showing_delta_frame % self.title_showing_interval == 0:
                self.text_title_pos[1] -= 5 * dt
            if self.text_title_pos[1] <= SCRN_HEIGHT / 5:
                pygame.mixer.music.play(-1, fade_ms=7800)
                self.title_was_being_showed = True
        if self.title_was_being_showed:
            self.sm.game.screen.blit(self.text_surface_start_game,
                                     self.text_titlemenu["start_game"]["pos"])
            self.sm.game.screen.blit(self.text_surface_game_config,
                                     self.text_titlemenu["game_config"]["pos"])
            self.sm.game.screen.blit(self.text_surface_exit,
                                     self.text_titlemenu["exit"]["pos"])
            self.sm.game.screen.blit(self.text_surface_menu_cursor,
                                     self.calc_menu_cursor_pos())
        self.sm.game.screen.blit(self.text_surface_title, self.text_title_pos)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=44100)
        pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode(SCRN_SIZE)
        self.clock = pygame.time.Clock()
        self.gametext = GameLocalizedText()
        self.gameconfig = GameConfig()
        self.gametext.language = self.gameconfig.config["language"]
        self.sm = GameSceneManager(self.screen, self)
        self.sm.append_scene("title", TitleScene(self.sm))
        self.sm.append_scene("config", ConfigScene(self.sm))
        self.sm.set_current_scene("title")

    def run(self) -> None:
        while True:
            dt = self.clock.tick(TARGET_FPS) * 0.001 * TARGET_FPS  # delta time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.sm.current_scene.handle_event(event)
            self.sm.current_scene.run(dt)
            pygame.display.update()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
