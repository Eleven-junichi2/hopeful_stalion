from hopeful_stalion.gamesystem import sprite


def test_sprite():
    sprite_ = sprite.Sprite(0, 0)
    assert sprite_.image.get_size() == (0, 0)
