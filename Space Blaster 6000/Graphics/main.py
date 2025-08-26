import pygame, sys, random
from game import Game

pygame.init()

WIN_WIDTH = 750
WIN_HEIGHT = 700
OFFSET = 50

GREY = (29, 29, 27)
YELLOW = (243, 216, 63)

font = pygame.font.Font("Font/monogram.ttf", 40)
level_surface = font.render("TekGeekGamez", False, YELLOW)
game_over_surface = font.render("GAME OVER", False, YELLOW)
score_text_surface = font.render("SCORE", False, YELLOW)
highscore_text_surface = font.render("HIGH SCORE", False, YELLOW)

WIN = pygame.display.set_mode((WIN_WIDTH + OFFSET, WIN_HEIGHT + 2*OFFSET))
pygame.display.set_caption("Space Blaster 6000")

clock = pygame.time.Clock()

game = Game(WIN_WIDTH, WIN_HEIGHT, OFFSET)

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 300)

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000,8000))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SHOOT_LASER and game.run:
            game.alien_shoot_laser()

        if event.type == MYSTERYSHIP and game.run:
            game.create_mystery_ship()
            pygame.time.set_timer(MYSTERYSHIP, random.randint(4000,8000))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game.run == False:
            game.reset()

    # Updating
    if game.run:
        game.space_blaster_group.update()
        game.move_aliens()
        game.alien_lasers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collisions()


    
    # Drawing
    WIN.fill(GREY)

    # UI
    pygame.draw.rect(WIN, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
    pygame.draw.line(WIN, YELLOW, (25, 730), (775, 730), 3)

    if game.run:
        WIN.blit(level_surface, (570, 740, 50, 50))
    else:
        WIN.blit(game_over_surface, (570, 740, 50, 50))

    x = 50
    for life in range(game.lives):
        WIN.blit(game.space_blaster_group.sprite.image, (x, 745))
        x += 50

    WIN.blit(score_text_surface, (50, 15, 50, 50))
    formatted_score = str(game.score).zfill(5)
    score_surface = font.render(formatted_score, False, YELLOW)
    WIN.blit(score_surface, (50, 40, 50, 50))
    WIN.blit(highscore_text_surface, (550, 15, 50, 50))
    formatted_highscore = str(game.highscore).zfill(5)
    highscore_surface = font.render(formatted_highscore, False, YELLOW)
    WIN.blit(highscore_surface, (625, 40, 50, 50))


    game.space_blaster_group.draw(WIN)
    game.space_blaster_group.sprite.lasers_group.draw(WIN)
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(WIN)
    game.aliens_group.draw(WIN)
    game.alien_lasers_group.draw(WIN)
    game.mystery_ship_group.draw(WIN)
    
    pygame.display.update()
    clock.tick(60)