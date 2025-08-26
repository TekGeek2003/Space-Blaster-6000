import pygame
from laser import Laser

class spaceblaster(pygame.sprite.Sprite):
    def __init__(self, WIN_WIDTH, WIN_HEIGHT, offset):
        super().__init__()
        self.offset = offset
        self.WIN_WIDTH = WIN_WIDTH
        self.WIN_HEIGHT = WIN_HEIGHT
        self.image = pygame.image.load("Graphics/space blaster 6000.png")
        self.rect = self.image.get_rect(midbottom = ((self.WIN_WIDTH + self.offset)/2, self.WIN_HEIGHT))
        self.speed = 6
        self.lasers_group = pygame.sprite.Group()
        self.laser_ready = True
        self.laser_time = 0
        self.laser_delay = 300
        self.laser_sound = pygame.mixer.Sound("Space Blaster 6000 sounds/laser.ogg")

    def get_user_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.laser_ready:
            self.laser_ready = False
            laser = Laser(self.rect.center, 5, self.WIN_HEIGHT)
            self.lasers_group.add(laser)
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()
        

    def update(self):
        self.get_user_input()
        self.constrain_movement()
        self.lasers_group.update()
        self.recharge_laser()

    def constrain_movement(self):
        if self.rect.right > self.WIN_WIDTH:
            self.rect.right = self.WIN_WIDTH
        if self.rect.left < self.offset:
            self.rect.left = self.offset

    def recharge_laser(self):
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_delay:
                self.laser_ready = True

    def reset(self):
        self.rect = self.image.get_rect(midbottom = ((self.WIN_WIDTH + self.offset)/2, self.WIN_HEIGHT))
        self.lasers_group.empty()


