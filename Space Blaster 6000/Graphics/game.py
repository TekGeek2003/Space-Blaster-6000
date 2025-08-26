import pygame, random
from space_blaster import spaceblaster
from obstacle import Obstacle
from obstacle import grid
from alien import Alien
from laser import Laser
from alien import MysteryShip

class Game:
    def __init__(self, WIN_WIDTH, WIN_HEIGHT, offset):
        self.WIN_WIDTH = WIN_WIDTH
        self.WIN_HEIGHT = WIN_HEIGHT
        self.offset = offset
        self.space_blaster_group = pygame.sprite.GroupSingle()
        self.space_blaster_group.add(spaceblaster(self.WIN_WIDTH, self.WIN_HEIGHT, self.offset))
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()
        self.lives = 3
        self.run = True
        self.score = 0
        self.highscore = 0
        self.explosion_sound = pygame.mixer.Sound("Space Blaster 6000 sounds/Sounds_explosion.ogg")
        self.load_highscore()
        pygame.mixer.music.load("Space Blaster 6000 sounds/music.ogg")
        pygame.mixer.music.play(-1)
        

    def create_obstacles(self):
        obstacle_width = len(grid[0]) * 3
        gap = (self.WIN_WIDTH + self.offset - (4 * obstacle_width))/5
        obstacles = []
        for i in range(4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.WIN_HEIGHT - 100)
            obstacles.append(obstacle)
        return obstacles

    def create_aliens(self):
        for row in range(5):
            for column in range(11):
                x = 75 + column * 55
                y = 110 + row * 55

                if row == 0:
                    alien_type = 3
                elif row in (1,2):
                    alien_type = 2
                else:
                    alien_type = 1

                alien = Alien(alien_type, x + self.offset/2, y)
                self.aliens_group.add(alien)

    def move_aliens(self):
        self.aliens_group.update(self.aliens_direction)

        alien_sprites = self.aliens_group.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= self.WIN_WIDTH + self.offset/2:
                self.aliens_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left < self.offset/2:
                self.aliens_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    def alien_shoot_laser(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprie = Laser(random_alien.rect.center, -6, self.WIN_HEIGHT)
            self.alien_lasers_group.add(laser_sprie)

    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(self.WIN_WIDTH, self.offset))

    def check_for_collisions(self):
        # Space Blaster
        if self.space_blaster_group.sprite.lasers_group:
           for laster_sprite in self.space_blaster_group.sprite.lasers_group:
                
                aliens_hit = pygame.sprite.spritecollide(laster_sprite, self.aliens_group, True)
                if aliens_hit:
                    self.explosion_sound.play()
                    for alien in aliens_hit:
                        self.score += alien.type * 100
                        self.check_for_highscore()
                        laster_sprite.kill()
                    
                if pygame.sprite.spritecollide(laster_sprite, self.mystery_ship_group, True):
                    self.score += 500
                    self.explosion_sound.play()
                    self.check_for_highscore()
                    laster_sprite.kill()

                for Obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laster_sprite, Obstacle.blocks_group, True):
                        laster_sprite.kill()

        # Alien Lasers
        if self.alien_lasers_group:
            for laster_sprite in self.alien_lasers_group:
                if pygame.sprite.spritecollide(laster_sprite, self.space_blaster_group, False):
                    laster_sprite.kill()
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over()    

                for Obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laster_sprite, Obstacle.blocks_group, True):
                        laster_sprite.kill()

        if self.aliens_group:
            for alien in self.aliens_group:
                for Obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, Obstacle.blocks_group, True)

                if pygame.sprite.spritecollide(alien, self.space_blaster_group, False):
                    self.game_over()

    def game_over(self):
        self.run = False

    def reset(self):
        self.run = True
        self.lives = 3
        self.space_blaster_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.obstacles = self.create_obstacles()
        self.score = 0 

    def check_for_highscore(self):
       if self.score > self.highscore:
        self.highscore = self.score

        with open("highscore.txt", "w") as file:
            file.write(str(self.highscore))

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as file:
                self.highscore = int(file.read())
        except FileNotFoundError:
            self.highscore = 0





