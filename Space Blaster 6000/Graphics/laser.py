import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, position, speed, WIN_HEIGHT):
        super().__init__()
        self.image = pygame.Surface((4,15))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center = position)
        self.speed = speed
        self.WIN_HEIGHT = WIN_HEIGHT

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > self.WIN_HEIGHT + 15 or self.rect.y < 0:
            self.kill()

