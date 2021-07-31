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

# TODO: make config scene to workable
# TODO: make menu cursor workable
# TODO: make screen camera


class Widget:
    """This class use to make UI"""

    def __init__(self, pos: list = [0, 0], size: list = [0, 0],
                 id: str = "") -> None:
        self.pos = pos
        self.size = size
        self.id = id

    def render(self):
        pass


class TextWidget(Widget):
    def __init__(self, font: pygame.font.Font, text="",
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.font = font
        self.__text = text
        self.__update_size_by_text(text)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__update_size_by_text(text)
        self.__text = text

    def __update_size_by_text(self, text):
        self.size = self.font.size(text)

    def render(self, *args, **kwargs) -> pygame.Surface:
        return self.font.render(self.text, *args, **kwargs)


class UILayout(Widget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout: list[Widget] = []


class UIBoxLayout(UILayout):
    """This class makes it easier to lay out Widgets"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.orientaion = "vertical"
        self.spacing = 0

    def add_widget(self, widget: Widget):
        layout_size = len(self.layout)
        layout_max_index = layout_size - 1
        if self.orientaion == "vertical":
            if layout_size == 0:
                widget.pos = [self.pos[0],
                              self.pos[1]]
            elif layout_size > 0:
                last_widget_pos = self.layout[layout_max_index].pos
                last_widget_size = self.layout[layout_max_index].size
                widget.pos = [self.pos[0],
                              last_widget_pos[1] +
                              last_widget_size[1] +
                              self.spacing]
            self.layout.append(widget)
        elif self.orientaion == "horizontal":
            # TODO make layout when horizontal
            pass


# class MenuChoiceNum(int, object):
#     def __iadd__(self, value, menu_item_num):
#         if self.choice_num < self.menu_item_num() - 1:
#             self += value
#         else:
#             self = 0
#             return self

#     def __isub__(self, value):
#         if self > 0:
#             self -= value
#         else:
#             self = self.menu_item_num() - 1
#             return self


class UIGameMenu(UIBoxLayout):
    # TDOO make menu cursor
    def __init__(self, default_menu_choice: int = 0,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__choice_num = default_menu_choice

    @property
    def choice_num(self):
        return self.__choice_num

    @choice_num.setter
    def choice_num(self, value):
        # self.__choice_num = MenuChoiceNum(value)
        # last_choice_num = self.__choice_num
        if value < self.__choice_num:  # __iadd__
            if self.__choice_num > 0:
                self.__choice_num = value
            else:
                self.__choice_num = self.menu_item_num() - 1
        elif value > self.__choice_num:  # __isub__
            if self.__choice_num < self.menu_item_num() - 1:
                self.__choice_num = value
            else:
                self.__choice_num = 0

        # self.__choice_num = value
        # if self.__choice_num

    # def __choice_num__add__(self, value):
    #     if self.choice_num < self.menu_item_num() - 1:
    #         self.choice_num += value
    #     else:
    #         self.choice_num = 0
    #         return self

    # def __choice_num__sub__(self, value):
    #     if self.choice_num > 0:
    #         self.choice_num -= value
    #     else:
    #         self.choice_num = self.menu_item_num() - 1
    #         return self

    def current_choice(self) -> Widget:
        return self.layout[self.choice_num]

    def menu_item_num(self) -> int:
        return len(self.layout)

    def menu_cursor_pos(self, cursor_size: list, anchor: str = "left"):
        """
         Args:
            anchor: you can use 'left' or 'right'
        """
        if anchor == "left":
            cursor_pos_x = self.current_choice().pos[0] - cursor_size[0]
            cursor_pos_y = self.current_choice().pos[1]
        elif anchor == "right":
            cursor_pos_x = self.current_choice(
            ).pos[0] + self.current_choice().size[0]
            cursor_pos_y = self.current_choice().pos[1]
        return cursor_pos_x, cursor_pos_y


class GameMenu:
    """This class makes it easier to code menu UI behavior.(unrecommanded)"""

    def __init__(self, current_choice: int = 0):
        self.current_choice: int = current_choice
        self.menu: dict[str] = {}
        self.home_pos: list[int, int] = [None, None]
        self.menu_spacing: list[int, int] = [0, 0]

    def unset_home_pos_of_ui(self):
        self.home_pos = [None, None]

    def add_to_menu(self, menu_key: str, menu_text: str,
                    pos_x_to_display: int = None, pos_y_to_display: int = None,
                    pos_to_absolute: bool = True):
        """If self.home_pos is set, arguments set position relative to
           home_pos."""
        self.menu[menu_key] = {"text": menu_text,
                               "pos": [(self.home_pos[0] or 0) +
                                       (pos_x_to_display or 0),
                                       (self.home_pos[1] or 0) +
                                       (pos_y_to_display or 0)]}

    def menu_keys(self) -> list:
        return list(self.menu.keys())

    def current_choice_menu_key(self) -> str:
        return self.menu_keys()[self.current_choice]


class NewGameScene(scene_trans.Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ConfigScene(scene_trans.Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.font_menu_cursor = pygame.font.Font(
            str(font_dir / "misaki_gothic.ttf"), 24)
        self.text_menu_cursor = "->"
        self.current_menu_choice: int = 0
        self.text_surface_menu_cursor = self.font_menu_cursor.render(
            self.text_menu_cursor, False, WHITE)
        self.menu_cursor_size = self.font_menu_cursor.size(
            self.text_menu_cursor)

        self.font_menu = pygame.font.Font(
            str(font_dir / "misaki_gothic.ttf"), 24)

        self.menu_ui = UIGameMenu(pos=[SCRN_WIDTH / 2.75, SCRN_HEIGHT / 3.5])
        self.menu_ui.add_widget(TextWidget(
            self.font_menu, text=self.sm.game.gametext.get_text(
                "cancel_config"),
            id="cancel"))
        self.menu_ui.add_widget(TextWidget(
            self.font_menu, text=self.sm.game.gametext.get_text(
                "confirm_config"),
            id="confirm"))

    def show_current_lang(self):
        language = self.sm.game.gameconfig.config["language"]
        if language == "jp":
            result = "日本語"
        elif language == "en":
            result = "English"
        return result

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu_ui.choice_num -= 1
            elif event.key == pygame.K_DOWN:
                self.menu_ui.choice_num += 1
            elif event.key == pygame.K_z:
                if self.menu_ui.current_choice().id == "cancel":
                    self.sm.set_current_scene("title")
                if self.menu_ui.current_choice().id == "confirm":
                    self.sm.set_current_scene("title")

    def run(self, dt):
        self.sm.game.screen.fill((0, 0, 0))
        for widget in self.menu_ui.layout:
            self.sm.game.screen.blit(
                widget.render(False, WHITE), widget.pos)
        self.sm.game.screen.blit(self.text_surface_menu_cursor,
                                 self.menu_ui.menu_cursor_pos(
                                     self.menu_cursor_size, "left"))


class TitleScene(scene_trans.Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pygame.mixer.music.load(str(music_dir / "hopeful_stalion_theme.ogg"))

        self.font_title = pygame.font.Font(
            str(font_dir / "misaki_gothic.ttf"), 48)

        self.text_title = self.sm.game.gametext.get_text("title")
        self.text_surface_title = self.font_title.render(
            self.text_title, False, WHITE)
        self.text_title_pos = [
            SCRN_WIDTH / 2.1 - self.font_title.size(self.text_title)[0] / 2,
            SCRN_HEIGHT / 2 - self.font_title.size(self.text_title)[1]]
        self.title_was_being_showed = False
        self.title_anim_delta_frame = 0
        self.title_anim_interval = 2

        self.font_titlemenu = pygame.font.Font(
            str(font_dir / "misaki_gothic.ttf"), 24)

        self.menu_ui = UIGameMenu(pos=[SCRN_WIDTH / 3, SCRN_HEIGHT / 2.9])
        self.menu_ui.spacing = 16
        self.menu_ui.add_widget(
            TextWidget(self.font_titlemenu,
                       self.sm.game.gametext.get_text("title_game_start"),
                       id="start"))
        self.menu_ui.add_widget(
            TextWidget(self.font_titlemenu,
                       self.sm.game.gametext.get_text("title_config"),
                       id="config"))
        self.menu_ui.add_widget(
            TextWidget(self.font_titlemenu,
                       self.sm.game.gametext.get_text("title_exit"),
                       id="exit"))

        self.font_menu_cursor = pygame.font.Font(
            str(font_dir / "misaki_gothic.ttf"), 24)
        self.text_menu_cursor = "->"
        self.current_menu_choice: int = 0
        self.text_surface_menu_cursor = self.font_titlemenu.render(
            self.text_menu_cursor, False, WHITE)
        self.menu_cursor_size = self.font_menu_cursor.size(
            self.text_menu_cursor)

    def calc_menu_cursor_pos(self):
        return [self.title_menu.menu["start_game"]["pos"][0] -
                self.menu_cursor_size[0],
                self.title_menu.menu[
                    self.title_menu.menu_keys()[
                        self.current_menu_choice]]["pos"][1]]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu_ui.choice_num -= 1
            elif event.key == pygame.K_DOWN:
                self.menu_ui.choice_num += 1
            elif event.key == pygame.K_z:
                if self.menu_ui.current_choice().id == "exit":
                    sys.exit()
                if self.menu_ui.current_choice().id == "config":
                    self.sm.set_current_scene("config")

    def run(self, dt):
        self.sm.game.screen.fill((0, 0, 0))
        if not self.title_was_being_showed:
            self.title_anim_delta_frame += 1
            if self.title_anim_delta_frame % self.title_anim_interval == 0:
                self.text_title_pos[1] -= 5 * dt
            if self.text_title_pos[1] <= SCRN_HEIGHT / 5:
                pygame.mixer.music.play(-1, fade_ms=7800)
                self.title_was_being_showed = True
        if self.title_was_being_showed:
            for widget in self.menu_ui.layout:
                self.sm.game.screen.blit(
                    widget.render(False, WHITE), widget.pos)
            self.sm.game.screen.blit(self.text_surface_menu_cursor,
                                     self.menu_ui.menu_cursor_pos(
                                         self.menu_cursor_size, "left"))
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
