import pygame.sprite


class Sprite(pygame.sprite.Sprite):
    # TODO make sprite class which can animation
    # TODO make test this class
    def __init__(self, width, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images: list[pygame.Surface] = []
        self.images.append(pygame.Surface([width, height]))
        self.index: int = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
