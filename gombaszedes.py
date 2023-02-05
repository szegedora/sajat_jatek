import pygame
import random

'''
A játék lényege az, hogy a megadott idő alat  a lehető legtöb gombát szedjük fel.
Ha a karakter odavezettük a gombához a SPACE gombot kell lenyomni hogy felszedjük a gombát.
'''

WIDTH = 1280
HEIGHT = 620
FONT_COLOR = (250, 250, 250)
GAME_TIME = 15000
MAN_SPEED = 6

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mushroom picking')
clock = pygame.time.Clock()

bg_surf = pygame.image.load('img/grass_background.png').convert_alpha()
bg_surf = pygame.transform.rotozoom(bg_surf, 0, 0.5)
bg_rect = bg_surf.get_rect(bottomleft=(0, HEIGHT))

# gombák
mush_surf = pygame.image.load('img/mushroom.png').convert_alpha()
mush_surf = pygame.transform.rotozoom(mush_surf, 0, 2)
mush_rects = []
for _ in range(5):
    mush_rect = mush_surf.get_rect(center=(random.randint(10, WIDTH - 10), random.randint(10, HEIGHT - 10)))
    mush_rects.append(mush_rect)

# karakterfázisok
char_fw = []
char_bw = []
char_l = []
char_r = []
for index in range(12):
    char_surf = pygame.image.load(f'img/character{index + 1}.png').convert_alpha()
    if index < 3:
        char_bw.append(char_surf)
    elif index < 6:
        char_fw.append(char_surf)
    elif index < 9:
        char_l.append(char_surf)
    else:
        char_r.append(char_surf)

char_x = WIDTH / 2
char_y = HEIGHT / 2
char_index = 0
char_rect = char_fw[0].get_rect(center=(char_x, char_y))

game_font = pygame.font.SysFont('arial', 30, bold=True)
title_surf = game_font.render('MUSHROOM PICKING', True, FONT_COLOR)
title_rect = title_surf.get_rect(center=(WIDTH / 2, 200))
run_surf = game_font.render('Press enter to play', True, FONT_COLOR)
run_rect = run_surf.get_rect(center=(WIDTH / 2, HEIGHT - 175))

start_time = pygame.time.get_ticks()
counter = 0
score = 0
direction = [False, True, False, False]
game_active = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg_surf, bg_rect)

    # aktív játékállapot
    if game_active:
        keys = pygame.key.get_pressed()

        # gombák megjelenítése és törlése
        for index, mush_rect in enumerate(mush_rects):
            if char_rect.colliderect(mush_rect) and keys[pygame.K_SPACE]:
                del mush_rects[index]
                score += 1
            screen.blit(mush_surf, mush_rect)

        # új gomba
        if len(mush_rects) < 5:
            mush_rect = mush_surf.get_rect(center=(random.randint(20, WIDTH - 20), random.randint(20, HEIGHT - 20)))
            mush_rects.append(mush_rect)

        # karakter oldalirányú mozgása
        if keys[pygame.K_RIGHT] and char_rect.right <= WIDTH:
            direction = [False, False, True, False]
            char_x += MAN_SPEED
            counter += 1
            if counter % 10 == 0:
                char_index += 1
            if char_index > 2:
                char_index = 0
        if keys[pygame.K_LEFT] and char_rect.left >= 0:
            direction = [False, False, False, True]
            char_x -= MAN_SPEED
            counter += 1
            if counter % 10 == 0:
                char_index += 1
            if char_index > 2:
                char_index = 0

        # karakter előre hátra mozgása
        if keys[pygame.K_UP] and char_rect.top >= 0:
            direction = [True, False, False, False]
            counter += 1
            if counter % 10 == 0:
                char_index += 1
            if char_index > 2:
                char_index = 0
            char_y -= MAN_SPEED
        if keys[pygame.K_DOWN] and char_rect.bottom <= HEIGHT:
            direction = [False, True, False, False]
            counter += 1
            if counter % 10 == 0:
                char_index += 1
            if char_index > 2:
                char_index = 0
            char_y += MAN_SPEED

        # karakter megjelenítése
        if direction[1]:
            char_rect = char_bw[char_index].get_rect(center=(char_x, char_y))
            screen.blit(char_bw[char_index], char_rect)
        elif direction[0]:
            char_rect = char_fw[char_index].get_rect(center=(char_x, char_y))
            screen.blit(char_fw[char_index], char_rect)
        elif direction[3]:
            char_rect = char_l[char_index].get_rect(center=(char_x, char_y))
            screen.blit(char_l[char_index], char_rect)
        elif direction[2]:
            char_rect = char_r[char_index].get_rect(center=(char_x, char_y))
            screen.blit(char_r[char_index], char_rect)

        # pontszám megjelenítése
        score_surf = game_font.render('score: ' + str(score), True, FONT_COLOR)
        score_rect = score_surf.get_rect(topleft=(10, 10))
        screen.blit(score_surf, score_rect)

        # hátralévő idő kiszámítása és megjelenítése
        time_left = int((start_time + GAME_TIME - pygame.time.get_ticks()) / 1000)
        if time_left < 0:
            game_active = False
        time_left_surf = game_font.render('time left: ' + str(time_left), True, FONT_COLOR)
        time_left_rect = time_left_surf.get_rect(topleft=(10, 50))
        screen.blit(time_left_surf, time_left_rect)

    # nyitó és záróképernyő
    else:
        for index, mush_rect in enumerate(mush_rects):
            screen.blit(mush_surf, mush_rect)
        screen.blit(title_surf, title_rect)
        screen.blit(char_bw[0], char_bw[0].get_rect(center=(WIDTH / 2, HEIGHT / 2)))
        screen.blit(run_surf, run_rect)

        # pontszám ha az értéke nagyobb, mint nulla
        if score:
            final_score_surf = game_font.render('SCORE: ' + str(score), True, FONT_COLOR)
            final_score_rect = final_score_surf.get_rect(center=(WIDTH / 2, HEIGHT - 220))
            screen.blit(final_score_surf, final_score_rect)

        # játék indítása
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            score = 0
            start_time = pygame.time.get_ticks()
            char_x = WIDTH / 2
            char_y = HEIGHT / 2
            char_index = 0
            direction = [False, True, False, False]
            game_active = True

    pygame.display.update()
    clock.tick(60)

pygame.quit()
