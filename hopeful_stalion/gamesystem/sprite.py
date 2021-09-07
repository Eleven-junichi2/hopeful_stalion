from abc import ABCMeta

import pygame
import pygame.sprite


class Sprite(pygame.sprite.Sprite, metaclass=ABCMeta):
    """
    'images' list object need to have some Surface object as item because
    'image' attribute is set from item of 'images' indexed by
    anim_index.

    Attributes:
        images list[pygame.Surface]:
        anim_index int:
        image pygame.Surface: draw method blit a surface with this attribute.
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.images: list[pygame.Surface] = []
        self.__anim_index: int = 0

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value: pygame.Surface):
        self.__image = value
        self.__image.get_rect()

    @property
    def anim_index(self):
        return self.__anim_index

    @anim_index.setter
    def anim_index(self, value):
        self.__anim_index = value
        self.image = self.images[self.anim_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
