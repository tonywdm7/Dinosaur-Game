import pygame
import random

pygame.init()

score = 0
font = pygame.font.Font(None, 36)
BLACK = (0, 0, 0)

cloud_speed = 0.5
cactus_speed = 0.5
enemy_speed = 0.5

WIDTH, HEIGHT = 600, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))

dino_image = pygame.image.load("dino.png")
cactus_image = pygame.image.load("cactus.png")
cloud_image = pygame.image.load("cloud.png")
gameover_image = pygame.image.load("gameover.png")
enemy_image = pygame.image.load("enemy.png")

button_width, button_height = gameover_image.get_width(), gameover_image.get_height()

button_x = WIDTH // 2 - button_width // 2
button_y = HEIGHT // 2 - button_height // 2

cloud_x = WIDTH
cloud_y = random.randint(0, 100)
cloud_scale = random.uniform(0.5, 1.5)

dino_x = 20
dino_y = HEIGHT - 50
speed_y = 0
dino_jumping = False

cactus_list = []
enemy_list = []
next_enemy_time = 1
next_cactus_time = 1

def jump():
    global speed_y, dino_jumping
    if not dino_jumping:
        speed_y = -2.1
        dino_jumping = True

def create_cactus():
    cactus_x = WIDTH
    cactus_y = HEIGHT - 50
    cactus_list.append([cactus_x, cactus_y])

def create_enemy():
    enemy_x = WIDTH
    enemy_y = HEIGHT - 50
    enemy_list.append([enemy_x, enemy_y])



create_cactus()
create_enemy()

button_show = False
paused = False

def draw_button():
    if button_show:
        global paused
        screen.blit(gameover_image, (button_x, button_y))
        paused = True

def press_button():
    global paused
    global button_show
    global score
    score = 0
    while len(cactus_list) != 0:
        cactus_list.pop(0)
    while len(enemy_list) != 0:  #
        enemy_list.pop(0)
    paused = False
    button_show = False
    create_cactus()

button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not paused:
                jump()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos) and button_show:
                press_button()

    cloud_x -= cloud_speed
    if cloud_x + cloud_image.get_width() * cloud_scale < 0:
        cloud_x = WIDTH
        cloud_y = random.randint(0, 100)
        cloud_scale = random.uniform(0.5, 1.5)

    if not paused:
        for i in range(len(cactus_list)):
            cactus_x, cactus_y = cactus_list[i]
            cactus_x -= cactus_speed
            if cactus_x + cactus_image.get_width() < 0:
                cactus_list.pop(i)
                break
            cactus_list[i] = (cactus_x, cactus_y)

        for enemy in enemy_list:  #
            enemy_x, enemy_y = enemy
            enemy_x -= enemy_speed
            if enemy_x + enemy_image.get_width() < 0:
                enemy_list.pop(enemy_list.index(enemy))
                break
            enemy_list[enemy_list.index(enemy)] = (enemy_x, enemy_y)

    ###

    if cactus_list[-1][0] < WIDTH - 450:
        next_cactus_time -= 0.1
        if next_cactus_time <= 0:
            create_cactus()
            next_cactus_time = random.randint(1, 40)

    if enemy_list[-1][0] < WIDTH - 450:
        next_enemy_time -= 0.1
        if next_enemy_time <= 0:
            create_enemy()
            next_enemy_time = random.randint(1, 40)

    dino_y += speed_y
    speed_y += 0.03
    if dino_y >= HEIGHT - 50:
        dino_y = HEIGHT - 50
        speed_y = 0
        dino_jumping = False

    for cactus_x, cactus_y in cactus_list:
        if dino_x + dino_image.get_width() > cactus_x and \
                dino_x < cactus_x + cactus_image.get_width() and \
                dino_y + dino_image.get_height() > cactus_y and \
                dino_y < cactus_y + cactus_image.get_height():
            button_show = True

    for enemy_x, enemy_y in enemy_list:
        if dino_x + dino_image.get_width() > enemy_x and \
                dino_x < enemy_x + enemy_image.get_width() and \
                dino_y + dino_image.get_height() > enemy_y and \
                dino_y < enemy_y + enemy_image.get_height():
            button_show = True

    scaled_cloud = pygame.transform.scale(cloud_image, (int(cloud_image.get_width() * cloud_scale),
                                                        int(cloud_image.get_height() * cloud_scale)))

    screen.fill((255, 255, 255))
    screen.blit(dino_image, (dino_x, dino_y))
    screen.blit(scaled_cloud, (cloud_x, cloud_y))

    for cactus in cactus_list:
        screen.blit(cactus_image, (cactus[0], cactus[1]))

    for enemy in enemy_list:
        screen.blit(enemy_image, (enemy[0], enemy[1]))

    if not paused:
        score += 0.0100
    score_rounded = int(score)
    score_text = font.render(str(score_rounded), True, BLACK)
    screen.blit(score_text, (20, 20))

    draw_button()

    pygame.display.flip()
    pygame.time.Clock().tick(1000)