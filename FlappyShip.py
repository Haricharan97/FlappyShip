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

max_fall_speed = 10

obstacle_width = 60
obstacle_speed = 4

gap = 180

obstacle1_x = 800
top1 = random.randint(75, 375)
bottom1 = top1 + gap

obstacle2_x = 1250
top2 = random.randint(75, 375)
bottom2 = top2 + gap

obstacle1_move = 1
obstacle2_move = -1

obstacle_vertical_speed = 0.7

level = 1

level1_gap = 180
level2_gap = 180
level3_gap = 160
level4_gap = 145

score = 0
high_score = 0
passed1 = False
passed2 = False

coins = 0

coin_size = 20

coin_gap = 190
coin_margin = 35
coin_list = []

def coin_blocked(x):

    clr = coin_size // 2 + 25
    l1 = obstacle1_x - clr
    r1 = obstacle1_x + obstacle_width + clr
    l2 = obstacle2_x - clr
    r2 = obstacle2_x + obstacle_width + clr

    return (
         l1 <= x <= r1
         or
         l2 <= x <= r2
    )

def safe_x(x):
     clr = coin_size // 2 + 25

     if obstacle1_x - clr <= x <= obstacle1_x + obstacle_width + clr:
          x = obstacle1_x + obstacle_width + clr

     if obstacle2_x - clr <= x <= obstacle2_x + obstacle_width + clr:
          x = obstacle2_x + obstacle_width + clr

     return x

def near_obs(x):
     if abs(x - obstacle1_x) <= abs(x - obstacle2_x):
          return 1

     return 2

def coin_y(obs, frac):
     if obs == 1:
          gt = top1
          gb = bottom1
     else:
          gt = top2
          gb = bottom2

     st = gt + coin_size // 2 + 12
     sb = gb - coin_size // 2 - 12

     if sb > st:
          return st + frac * (sb - st)

     return (gt + gb) / 2

def new_coin(x):

     x = safe_x(x)
     obs = near_obs(x)
     frac = random.random()
     y = coin_y(obs, frac)

     return [x, y, obs, frac]

def spawn_coins():
     cs = []
     for i in range(8):
          x = width + 100 + i * coin_gap
          cs.append(new_coin(x))
     return cs

coin_list = spawn_coins()

treasure_x = width + 100
treasure_y = random.randint(100, 300)
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

                    level = 1
                    gap = level1_gap
                    obstacle_vertical_speed = 0.7

                    top1 = random.randint(75, 375)
                    bottom1 = top1 + gap

                    top2 = random.randint(75, 375)
                    bottom2 = top2 + gap

                    obstacle1_move = 1
                    obstacle2_move = -1

                    score = 0
                    passed1 = False
                    passed2 = False

                    coins = 0

                    coin_list = spawn_coins()

                    treasure_active = False
                    treasure_timer = 0

                    treasure_x = width + 100
                    treasure_y = random.randint(100,300)

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

        if score < 5:
             level = 1
             gap = level1_gap
             obstacle_vertical_speed = 0.7

        elif score < 10:
             level = 2
             gap = level2_gap
             obstacle_vertical_speed = 0.8

        elif score < 15:
             level = 3 
             gap = level3_gap
             obstacle_vertical_speed = 0.8

        else:
             level = 4
             gap = level4_gap
             obstacle_vertical_speed = 1.0

        boat_speed = boat_speed + gravity

        if boat_speed > max_fall_speed:
             boat_speed = max_fall_speed

        boat_y = boat_y + boat_speed

        obstacle1_x = obstacle1_x - obstacle_speed
        obstacle2_x = obstacle2_x - obstacle_speed

        if level >= 2:

            top1 = top1 + obstacle1_move * obstacle_vertical_speed

            if top1 >= 375:

                top1 = 375
                obstacle1_move = -1

            elif top1 <= 75:
                 top1 = 75

                 obstacle1_move = 1

            top2 = top2 + obstacle2_move * obstacle_vertical_speed

            if top2 >= 375:
                 top2 = 375
                 obstacle2_move = -1

            elif top2 <= 75:
                 top2 = 75
                 obstacle2_move = 1

        bottom1 = top1 + gap
        bottom2 = top2 + gap

        wave_offset = wave_offset + obstacle_speed

        for c in coin_list:
             c[0] -= obstacle_speed

        mx = max(c[0] for c in coin_list)

        for c in coin_list:
             if c[0] < -coin_size:
                  mx += coin_gap
                  nd = new_coin(mx)
                  c[0], c[1], c[2], c[3] = nd
        
        for c in coin_list:
             if coin_blocked(c[0])          :
                  mx = max(
                       max(x[0] for x in coin_list),
                       obstacle1_x + obstacle_width,
                       obstacle2_x + obstacle_width
                  )

                  mx += coin_gap
                  nd = new_coin(mx)
                  c[0], c[1], c[2], c[3] = nd

        treasure_timer = treasure_timer + 1
     
        if treasure_active == False and treasure_timer > 180:

             if random.randint(1, 100) <= 3:
                  treasure_active = True
                  treasure_x = width + 120
             
             if abs(treasure_x - obstacle1_x) < obstacle_width + treasure_size + 35:
                  treasure_x = (
                       obstacle1_x
                       + obstacle_width
                       + obstacle_width
                       + treasure_size
                       + 35
                  )

             if abs(treasure_x - obstacle2_x) < obstacle_width + treasure_size + 35:
                  treasure_x = (
                       obstacle2_x
                       + obstacle_width
                       + obstacle_width
                       + treasure_size
                       + 35
                  )

             if near_obs (treasure_x) == 1:
                  treasure_y = random.randint(
                       int(top1 + treasure_size + 15),
                       int(bottom1 - treasure_size - 15)
                  )
             else:
                  treasure_y = random.randint(
                       int(top2 + treasure_size + 15) ,
                       int(bottom2 - treasure_size - 15)
                  )

             treasure_timer = 0
        if treasure_active == True:
             treasure_x = treasure_x - obstacle_speed
             if obstacle1_x - (treasure_size + 30) <= treasure_x <= obstacle1_x + obstacle_width + (treasure_size + 30):
                  treasure_x = (
                       obstacle1_x
                       + obstacle_width
                       + treasure_size
                       + 30
                  )
             if obstacle2_x - (treasure_size + 30) <= treasure_x <= obstacle2_x + obstacle_width + (treasure_size + 30):
                  treasure_x = (
                       obstacle2_x
                       + obstacle_width
                       + treasure_size
                       + 30
                  )
          
        if treasure_x < -treasure_size:
                 treasure_active = False
                 treasure_timer = 0

        if obstacle1_x + obstacle_width < boat_x and passed1 == False:

            score = score + 1
            passed1 = True

            if score > high_score:
                  high_score = score

            obstacle_speed = 4 + score * 0.2

            if level == 4:

                if obstacle_speed > 9:
                    obstacle_speed = 9

            else:

                if obstacle_speed > 8:
                    obstacle_speed = 8

        if obstacle2_x + obstacle_width < boat_x and passed2 == False:
            score = score + 1
            passed2 = True

            if score > high_score:
                high_score = score

            obstacle_speed = 4 + score * 0.2

            if level == 4:

                if obstacle_speed > 9:
                    obstacle_speed = 9

            else:
                
                if obstacle_speed > 8:
                    obstacle_speed = 8
        
        if obstacle1_x < -obstacle_width:

            obstacle1_x = obstacle2_x + 600

            top1 = random.randint(75, 375)
            bottom1 = top1 + gap

            passed1 = False

            obstacle1_move = random.choice([-1,1])

        if obstacle2_x < -obstacle_width:

            obstacle2_x = obstacle1_x + 600

            top2 = random.randint(75, 375)
            bottom2 = top2 + gap

            passed2 = False

            obstacle2_move = random.choice([-1,1])


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
              
    treasure_rect = pygame.Rect(
         treasure_x - treasure_size // 2,
         treasure_y - treasure_size // 2,
         treasure_size,
         treasure_size
    )

    if game_state == playing and game_over == False:

        if boat_y < 0:
            game_over = True

        elif boat_y + boat_height>= height:
             game_over = True

        elif boat_rect.colliderect(top_rect1) or boat_rect.colliderect(bottom_rect1):
            game_over = True

        elif boat_rect.colliderect(top_rect2) or boat_rect.colliderect(bottom_rect2):
            game_over = True

        if game_over == False:

            for coin in coin_list:

                 coin_rect = pygame.Rect(
                      int(coin[0] - coin_size // 2),
                      int(coin[1] - coin_size // 2) ,
                      coin_size,
                      coin_size
                 )

                 if boat_rect.colliderect(coin_rect):
                      coins += 1
                      mx = max(
                           max(c[0] for c in coin_list),
                           obstacle1_x + obstacle_width,
                           obstacle2_x + obstacle_width
                      )

                      mx += coin_gap
                      nd = new_coin(mx)
                      coin[0], coin[1], coin[2], coin[3] = nd

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
              + math.sin((i + wave_offset)*0.04)*8
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
         (35, 135, 157),
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


    pygame.draw.polygon(
         screen,
         (100, 50, 30),
         [
              (boat_x + boat_width - 5, boat_y + 15),
              (boat_x + boat_width + 8, boat_y + 22),
              (boat_x + boat_width - 15, boat_y + boat_height - 5)
         ]
    )

    pygame.draw.polygon(
         screen,
         (60, 30, 15),
         [
              (boat_x + boat_width - 5, boat_y + 15),
              (boat_x + boat_width + 8, boat_y + 22),
              (boat_x + boat_width - 15, boat_y + boat_height - 5)
         ],
         1
    )

    pygame.draw.rect(
         screen,
         (180, 95, 45),
         (boat_x + 5, boat_y + 10, boat_width - 10, 8)
    )
     
    pygame.draw.polygon(
            screen,
            (125, 65, 35),
            [
                 (boat_x, boat_y + 15),
                 (boat_x + boat_width - 5, boat_y + 15),
                 (boat_x + boat_width - 15, boat_y + boat_height),
                 (boat_x + 15, boat_y + boat_height)
            ]
        )

    pygame.draw.polygon(
         screen,
         (95, 45, 25),
         [
              (boat_x + 10, boat_y + boat_height - 10),
              (boat_x + boat_width - 15, boat_y + boat_height - 10),
              (boat_x + boat_width - 15, boat_y + boat_height),
              (boat_x + 15, boat_y + boat_height)
         ]
    )

    pygame.draw.polygon(
         screen,
         (60, 30, 15),
         [
              (boat_x, boat_y + 15),
              (boat_x + boat_width - 5, boat_y + + 15),
              (boat_x + boat_width - 15, boat_y + boat_height),
              (boat_x + 15, boat_y + boat_height)
         ],
         2
    )

    pygame.draw.rect(
         screen,
         (60, 30, 15),
         (boat_x + 5, boat_y + 10, boat_width - 10, 8),
         1
    )

    pygame.draw.rect(
         screen,
         (230, 230, 220),
         (boat_x + 25, boat_y, 30, 15)
    )

    pygame.draw.rect(
         screen,
         (150, 150, 140),
         (boat_x + 25, boat_y, 30, 15),
         1
    )


    pygame.draw.rect(
         screen,
         (150, 40, 30),
         (boat_x + 23, boat_y - 4, 34, 5)
    )


    pygame.draw.rect(
          screen,
          (80, 170, 220),
          (boat_x + 35, boat_y + 3, 10, 8)
     )

    pygame.draw.rect(
         screen,
         (255, 255, 255),
         (boat_x + 39, boat_y + 4, 2, 6)
    )

    pygame.draw.circle(
         screen,
         (80, 170, 220),
         (boat_x + 15, boat_y + 22),
         4
    )

    pygame.draw.circle(
         screen,
         (60, 30, 15),
         (boat_x + 15, boat_y + 22),
         4,
         1
    )

    pygame.draw.line(
         screen,
         (90, 60, 30),
         (boat_x + boat_width // 2, boat_y - 4),
         (boat_x + boat_width // 2, boat_y - 45),
         3
    )

    pygame.draw.polygon(
         screen,
         (245, 245, 235),
         [
              (boat_x + boat_width // 2, boat_y - 45),
              (boat_x + boat_width // 2, boat_y - 6),
              (boat_x + boat_width // 2 + 25, boat_y - 12)
         ]
    )

    pygame.draw.polygon(
         screen,
         (150, 150, 140),
         [
              (boat_x + boat_width // 2, boat_y - 45),
              (boat_x + boat_width // 2, boat_y - 6),
              (boat_x + boat_width // 2 + 25, boat_y - 12)
         ],
         1
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

    for coin_x, coin_y_pos, coin_obs, coin_frac in coin_list:
         pygame.draw.circle(
              screen,
              (255, 220, 0),
              (
                   int(coin_x),
                   int(coin_y_pos)
              ),
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

