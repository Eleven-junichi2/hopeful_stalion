import pygame
import pygame.sprite


class Sprite(pygame.sprite.Sprite):
    # TODO make sprite class which can animation
    # TODO make setter for "image" property
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images: list[pygame.Surface] = []
        self.images.append(pygame.Surface([0, 0]))
        self.index: int = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
