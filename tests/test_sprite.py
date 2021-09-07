import pytest
import pygame

from hopeful_stalion.gamesystem import sprite

# TODO make sprite class abstract class


class NotImagesDefinedSprite(sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass


class CorrectSprite(sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images = [pygame.Surface([0, 0]), ]


def test_sprite():
    # with pytest.raises(AttributeError):
    sprite_instance = NotImagesDefinedSprite()
    # sprite_instance = CorrectSprite()
    # sprite_instance.anim_index = 1
    # with pytest.raises(TypeError):
    #     CorrectSprite()
