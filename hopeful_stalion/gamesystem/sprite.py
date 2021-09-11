from abc import ABCMeta

import pygame
import pygame.sprite

# TODO make Sprite class loadable spritesheet


class ImagesHasNoItemError(Exception):
    """This exception raise when images attribute is invalid value."""

    def __str__(self):
        return """'images' list object need to have some Surface object
                as item because 'image' attribute is set from item of 'images'
                indexed by anim_index."""


def image_from_sheet(
        self, image: pygame.Surface,
        x: int, y: int, w: int, h: int) -> pygame.Surface:
    """extract a image from image like spritesheet.

    Args:
        x (int):
        y (int):
        w (int): width
        h (int): height
    """
    new_image = pygame.Surface((w, h))
    # sprite.set_colorkey(0, 0 ,0)
    new_image.blit(image, (0, 0), (x, y, w, h))
    return new_image


class Sprite(pygame.sprite.Sprite, metaclass=ABCMeta):
    """This abstract class use to define sprite with some images to animation.

    'images' list object need to have some Surface object as item because
    'image' attribute is set from item of 'images' indexed by anim_index.
    Thus, When define a new class that inherit this class, 'images' must
    be defined as class attribute that contain some Surface object.

    Attributes:
        images list[pygame.Surface]:
        anim_index int:
        image pygame.Surface: draw method blit a surface with this attribute.
        rect: rect is made of image.

    Example:

    class NewSprite(Sprite):
        images = [pygame.Surface((0, 0)),]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    # --- in pygame mainloop ---
    new_sprite = NewSprite():
    new_sprite.draw(screen)
    # ---
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.anim_index: int = 0

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
