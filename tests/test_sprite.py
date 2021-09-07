import pytest
import pygame

from hopeful_stalion.gamesystem import sprite

# TODO make sprite class abstract class


class NotImagesDefinedSprite(sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ImagesDefinedButEmptySprite(sprite.Sprite):
    images = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CorrectSprite(sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images = [pygame.Surface([0, 0]), ]


def test_sprite():
    with pytest.raises(NotImplementedError):
        NotImagesDefinedSprite()
    with pytest.raises(sprite.ImagesHasNoItemError):
        ImagesDefinedButEmptySprite()
