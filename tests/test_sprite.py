from hopeful_stalion.gamesystem import sprite
import pygame


def test_sprite():
    sprite_ = sprite.Sprite(0, 0)
    assert sprite_.image == pygame.Surface((0, 0))
