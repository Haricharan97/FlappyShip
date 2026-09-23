import pygame
import random
import math

pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width,height))

clock = pygame.time.Clock()

font = pygame.font.Font(None, 70)
small_font = pygame.font.Font(None, 40)

boat_x = 150
boat_y = 300

boat_width = 80
boat_height = 40

boat_speed = 0

gravity = 0.5
jump = -8

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
high_score = 0
passed1 = False
passed2 = False

coins = 0

coin_size = 20

coin1_x = obstacle1_x + obstacle_width // 2
coin1_y = top1 + gap // 2

coin2_x = obstacle2_x + obstacle_width // 2
coin2_y = top2 + gap // 2

coin3_x = (obstacle1_x + obstacle2_x) // 2
coin3_y = 250

coin1_collected = False
coin2_collected = False
coin3_collected = False

treasure_x = width + 100
treasure_y = random.randint(100, 450)
treasure_size = 28
treasure_active = False
treasure_timer = 0

wave_offset = 0

water = 360

game_over = False

start = 0
playing = 1
paused = 2

game_state = start

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_over == True:

                if event.key == pygame.K_RETURN:

                    boat_y = 300
                    boat_speed = 0

                    obstacle1_x = 800
                    obstacle2_x = 1250

                    top1 = random.randint(75, 375)
                    bottom1 = top1 + gap

                    top2 = random.randint(75, 375)
                    bottom2 = top2 + gap

                    score = 0
                    passed1 = False
                    passed2 = False

                    coins = 0

                    coin1_x = (obstacle1_x + obstacle_width) // 2
                    coin1_y = top1 + gap // 2

                    coin2_x = (obstacle2_x + obstacle_width) // 2
                    coin2_y = top2 + gap // 2

                    coin3_x = (obstacle1_x + obstacle2_x) // 2
                    coin3_y = 250

                    coin1_collected = False
                    coin2_collected = False
                    coin3_collected = False

                    treasure_active = False
                    treasure_timer = 0

                    treasure_x = width + 100
                    treasure_y = random.randint(100,500)

                    obstacle_speed = 4 
                    wave_offset = 0

                    game_over = False
                    game_state = playing

            elif game_state == start:

                    if event.key == pygame.K_SPACE:
                        game_state = playing
                        boat_speed = jump

            elif game_state == playing:

                        if event.key == pygame.K_SPACE:
                            boat_speed = jump

                        if event.key == pygame.K_ESCAPE:
                            game_state = paused
    
            elif game_state == paused:

                        if event.key == pygame.K_ESCAPE:
                            game_state = playing

    if game_over == False and game_state == playing:

        boat_speed = boat_speed + gravity
        boat_y = boat_y + boat_speed

        obstacle1_x = obstacle1_x - obstacle_speed
        obstacle2_x = obstacle2_x - obstacle_speed

        wave_offset = wave_offset + obstacle_speed

        coin1_x = obstacle1_x + obstacle_width // 2
        coin2_x = obstacle2_x + obstacle_width // 2
        coin3_x = coin3_x - obstacle_speed

        if coin3_x < -coin_size:
             coin3_x = width + 250
             coin3_y = random.randint(120, 480)
             coin3_collected = False

        treasure_timer = treasure_timer + 1

        if treasure_active == False and treasure_timer > 180:

            if random.randint(1,100) <= 3:
                treasure_active = True
                treasure_x = width + 50
                treasure_y = random.randint(100, 500)
                treasure_timer = 0

        if treasure_active == True:
                treasure_x = treasure_x - obstacle_speed

        if treasure_x < -treasure_size:
                 treasure_active = False
                 treasure_timer = 0

        if obstacle1_x < boat_x and passed1 == False:
            score = score + 1
            passed1 = True

            if score > high_score:
                 high_score = score

            obstacle_speed = 4 + score * 0.2

            if obstacle_speed > 8:
                 obstacle_speed = 8

        if obstacle2_x < boat_x and passed2 == False:
            score = score + 1
            passed2 = True

            if score > high_score:
                 high_score = score

            obstacle_speed = 4 + score * 0.2

            if obstacle_speed > 8:
                 obstacle_speed = 8
        
        if obstacle1_x < -obstacle_width:

            obstacle1_x = obstacle2_x + 600

            top1 = random.randint(75, 375)
            bottom1 = top1 + gap

            passed1 = False

            coin1_y = top1 + gap // 2
            coin1_collected = False

        if obstacle2_x < -obstacle_width:

            obstacle2_x = obstacle1_x + 600

            top2 = random.randint(75, 375)
            bottom2 = top2 + gap

            passed2 = False

            coin2_y = top2 + gap // 2
            coin2_collected = False


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

    coin1_rect = pygame.Rect(
         coin1_x - coin_size // 2,
         coin1_y - coin_size //2,
         coin_size,
         coin_size
    )

    coin2_rect = pygame.Rect(
        coin2_x - coin_size // 2,
        coin2_y - coin_size //2,
        coin_size,
        coin_size
    )

    coin3_rect = pygame.Rect(
        coin3_x - coin_size // 2,
        coin3_y - coin_size //2,
        coin_size,
        coin_size
    )

    treasure_rect = pygame.Rect(
         treasure_x - treasure_size // 2,
         treasure_y - treasure_size // 2,
         treasure_size,
         treasure_size
    )

    if game_state == playing and game_over == False:

        if boat_y < 0:
            game_over = True

        if boat_y + boat_height>= height:
             game_over = True

        if boat_rect.colliderect(top_rect1) or boat_rect.colliderect(bottom_rect1):
            game_over = True

        if boat_rect.colliderect(top_rect2) or boat_rect.colliderect(bottom_rect2):
            game_over = True

        if boat_rect.colliderect(coin1_rect) and coin1_collected == False:
             coins = coins + 1
             coin1_collected = True

        if boat_rect.colliderect(coin2_rect) and coin2_collected == False:
             coins = coins + 1
             coin2_collected = True

        if boat_rect.colliderect(coin3_rect) and coin3_collected == False:
             coins = coins + 1
             coin3_collected = True

        if treasure_active == True:
             if boat_rect.colliderect(treasure_rect):
                  coins = coins + 5
                  treasure_active = False
                  treasure_timer = 0

    screen.fill((70,150,220))

    back_points = [(0, height)]

    for i in range(0, width + 10, 10):

         wave_y = (
              water
              + math.sin((i + wave_offset)*0.02)*15
              +math.sin((i + wave_offset)*0.04)*8
         )

         back_points.append((i, wave_y + 40))

    back_points.append((width, height))

    pygame.draw.polygon(
         screen,
         (8,55,82),
         back_points
    )

    middle_points = [(0,height)]

    for i in range(0, width +10, 10):

         wave_y = (
              water
              + math.sin((i + wave_offset) * 0.02) * 15
              + math.sin((i + wave_offset) * 0.04) * 8
         )

         middle_points.append((i, wave_y + 20))

    middle_points.append((width, height))

    pygame.draw.polygon(
         screen,
         (10, 91, 120),
         middle_points
    )

    front_points = [(0, height)]

    for i in range(0, width + 10, 10):

         wave_y = (
              water
              + math.sin((i + wave_offset) * 0.02) * 15
              +math.sin((i + wave_offset) * 0.04) * 8
         )

         front_points.append((i, wave_y))

    front_points.append((width, height))

    pygame.draw.polygon(
         screen,
         (35,135,157),
         front_points
    )

    for i in range(0, width, 30):

         wave_y = (
              water
              + math.sin((i + wave_offset) * 0.02) * 15
              +math.sin((i + wave_offset) * 0.04) * 8
         )

         pygame.draw.rect(
              screen,
              (115, 205, 204),
              (i, wave_y, 15, 5)
         )

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

    if coin1_collected == False:

         pygame.draw.circle(
              screen,
              (255, 220, 0),
              (int(coin1_x), int(coin1_y)),
              10
         )

    if coin2_collected == False:

         pygame.draw.circle(
              screen,
              (255, 220, 0),
              (int(coin2_x), int(coin2_y)),
              10
         )

    if coin3_collected == False:

         pygame.draw.circle(
              screen,
              (255, 220, 0),
              (int(coin3_x), int(coin3_y)),
              10
         )

    if treasure_active == True:
         pygame.draw.circle(
              screen,
              (100,55,20),
              (
                   int(treasure_x),
                   int(treasure_y)
              ),
              16
         )

         pygame.draw.circle(
              screen,
              (180,100,35),
              (
                   int(treasure_x),
                   int(treasure_y)
              ),
              9
         )

         pygame.draw.circle(
              screen,
              (255, 190, 50),
              (
                   int(treasure_x),
                   int(treasure_y)
              ),
              4
         )

    score_text = font.render(
        str(score),
        True,
        ( 255, 255, 255)
    )

    screen.blit(score_text, (380, 30))

    coin_text = small_font.render(
         "Coins: " + str(coins),
         True,
         (255, 220, 0)
    )

    screen.blit(coin_text, (20,20))

    high_score_text = small_font.render(
         "High Score: " + str(high_score),
         True,
         (255,255,255)
    )

    screen.blit(high_score_text, (580,20))

    if game_state == start:

        title = font.render(
            "FLAPPY SHIP",
            True,
            (255, 255, 255)
        )

        start_text = small_font.render(
            "PRESS SPACE TO START",
            True,
            (255, 255, 255)
        )

        screen.blit(title, (250,220))
        screen.blit(start_text, (245, 310))

    if game_state == paused:

        paused_text = font.render(
            "PAUSED",
            True,
            (255, 255, 255)
        )

        continue_text = small_font.render(
            "PRESS ESC TO CONTINUE",
            True,
            (255, 255, 255)
        )

        screen.blit(paused_text, (290, 220))
        screen.blit(continue_text, (245, 310))

    if game_over == True:

        text = font.render(
                "GAME OVER",
                True,
                (255, 255, 255)
            )

        restart_text = small_font.render(
                "PRESS ENTER TO RESTART",
             True,
            (255, 255, 255)
        )

        screen.blit(text, (240,250))
        screen.blit(restart_text, (220, 320))

    pygame.display.flip()

pygame.quit()