import pygame.font


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
        self.orientaion: str = "vertical"
        self.spacing: int = 0

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


class UIGameMenu(UIBoxLayout):
    def __init__(self, default_menu_choice: int = 0,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__choice_num = default_menu_choice

    @property
    def choice_num(self):
        return self.__choice_num

    @choice_num.setter
    def choice_num(self, value):
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

    def current_choice(self) -> Widget:
        return self.layout[self.choice_num]

    def menu_item_num(self) -> int:
        return len(self.layout)

    def menu_cursor_pos(self, cursor_size: list, anchor: str = "left"):
        """
         Args:
            anchor (str): 'left' or 'right'
        """
        if anchor == "left":
            cursor_pos_x = self.current_choice().pos[0] - cursor_size[0]
            cursor_pos_y = self.current_choice().pos[1]
        elif anchor == "right":
            cursor_pos_x = self.current_choice(
            ).pos[0] + self.current_choice().size[0]
            cursor_pos_y = self.current_choice().pos[1]
        return cursor_pos_x, cursor_pos_y
