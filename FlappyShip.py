import pygame

pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width,height))

clock = pygame.time.Clock()

boat_x = 150
boat_y = 300

boat_width = 80
boat_height = 40

boat_speed = 0

gravity = 0.5
jump = -8

obstacle_x = 800
obstacle_y = 350

obstacle_width = 60
obstacle_height = 40

obstacle_speed = 4

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                boat_speed = jump

    boat_speed = boat_speed + gravity
    boat_y = boat_y + boat_speed

    if boat_y < 0:
            boat_y = 0
            boat_speed = 0

    if boat_y  > height - boat_height:
            boat_y = height - boat_height
            boat_speed = 0

    obstacle_x = obstacle_x - obstacle_speed

    if obstacle_x < -obstacle_x < -obstacle_width:
         obstacle_x = width

    screen.fill((70,150,220))

    pygame.draw.rect(
            screen,
            (120,70,30),
            (boat_x, boat_y, boat_width, boat_height)
        )

    pygame.draw.rect(
         screen,
         (80,80,80),
         (obstacle_x, obstacle_y, obstacle_width, obstacle_height)
    )

    pygame.display.flip()

pygame.quit