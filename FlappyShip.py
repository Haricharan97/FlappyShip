import pygame
import random

pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width,height))

clock = pygame.time.Clock()

font = pygame.font.Font(None, 70)

boat_x = 150
boat_y = 300

boat_width = 80
boat_height = 40

boat_speed = 0

gravity = 0.5
jump = -8

obstacle_x = 800

obstacle_width = 60
obstacle_speed = 4

gap = 180

obstacle1_x = 800
top1 = random.randint(75, 375)
bottom1 = top1 + gap

obstacle2_x = 1250
top2 = random.randint(75, 375)
bottom2 = top2 + gap

score = 0
passed1 = False
passed2 = False

game_over = False

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                boat_speed = jump

    if game_over == False:

        boat_speed = boat_speed + gravity
        boat_y = boat_y + boat_speed

        obstacle1_x = obstacle1_x - obstacle_speed
        obstacle2_x = obstacle2_x - obstacle_speed

        if obstacle1_x < boat_x and passed1 == False:
            score = score + 1
            passed1 = True

        if obstacle2_x < boat_x and passed2 == False:
            score = score + 1
            passed2 = True
        
        if obstacle1_x < -obstacle_width:

            obstacle1_x = obstacle2_x + 600

            top1 = random.randint(75, 375)
            bottom1 = top1 + gap

            passed1 = False

        if obstacle2_x < -obstacle_width:

            obstacle2_x = obstacle1_x + 600

            top2 = random.randint(75, 375)
            bottom2 = top2 + gap

            passed2 = False


    boat_rect = pygame.Rect(
         boat_x,
         boat_y,
         boat_width,
         boat_height
    )

    top_rect1 = pygame.Rect(
        obstacle1_x,
        0,
        obstacle_width,
        top1
    )

    bottom_rect1 = pygame.Rect(
        obstacle1_x,
        bottom1,
        obstacle_width,
        height - bottom1
    )

    top_rect2 = pygame.Rect(
        obstacle2_x,
        0,
        obstacle_width,
        top2
    )

    bottom_rect2 = pygame.Rect(
        obstacle2_x,
        bottom2,
        obstacle_width,
        height - bottom2
    )

    if boat_y < 0:
         game_over = True

    if boat_y + boat_height >= height:
        game_over = True

    if boat_rect.colliderect(top_rect1) or boat_rect.colliderect(bottom_rect1):
        game_over = True

    if boat_rect.colliderect(top_rect2) or boat_rect.colliderect(bottom_rect2):
        game_over = True

    screen.fill((70,150,220))

    pygame.draw.rect(
            screen,
            (120,70,30),
            (boat_x, boat_y, boat_width, boat_height)
        )

    pygame.draw.rect(
         screen,
         (80,80,80),
         (obstacle1_x, 0, obstacle_width, top1)
    )

    pygame.draw.rect(
         screen,
         (80,80,80),
         (obstacle1_x, bottom1, obstacle_width, height - bottom1)
    )

    pygame.draw.rect(
        screen,
        (80, 80, 80),
        (obstacle2_x, 0, obstacle_width, top2)
    )

    pygame.draw.rect(
        screen,
        (80, 80, 80),
        (obstacle2_x, bottom2, obstacle_width, height - bottom2)
    )

    score_text = font.render(
        str(score),
        True,
        ( 255, 255, 255)
    )

    screen.blit(score_text, (380, 30))

    if game_over == True:
        text = font.render(
            "GAME OVER",
            True,
            (255,255,255)
        )

        screen.blit(text, (240,250))

    pygame.display.flip()

pygame.quit()