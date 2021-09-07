from abc import ABCMeta
import traceback

import pygame
import pygame.sprite


class ImagesHasNoItemError(Exception):
    """This exception raise when images attribute is invalid value."""

    def __str__(self):
        return """'images' list object need to have some Surface object
                as item because 'image' attribute is set from item of 'images'
                indexed by anim_index."""


class Sprite(pygame.sprite.Sprite, metaclass=ABCMeta):
    """
    'images' list object need to have some Surface object as item because
    'image' attribute is set from item of 'images' indexed by anim_index.
    Thus,'images' must be defined as class attribute that contain some Surface
    object.

    Attributes:
        images list[pygame.Surface]:
        anim_index int:
        image pygame.Surface: draw method blit a surface with this attribute.
    
    Example:
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.images: list[pygame.Surface] = []
        self.anim_index: int = 0
        # self.image: pygame.Surface =

    @property
    def images(self):
        raise NotImplementedError(
            "'images' list object must be defined as class attribute that"
            + " contain some Surface objects.")

    @property
    def anim_index(self):
        return self.__anim_index

    @property
    def image(self):
        if self.images == []:
            raise ImagesHasNoItemError
        return self.images[self.anim_index]

    @image.setter
    def image(self, value: pygame.Surface):
        self.__image = value
        self.rect = self.__image.get_rect()

    @anim_index.setter
    def anim_index(self, value):
        self.__anim_index = value
        if self.images == []:
            raise ImagesHasNoItemError
        self.image = self.images[self.anim_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
