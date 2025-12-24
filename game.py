# game.py

import pygame
from player import Player
from level import Level
from utils import circle_rect_collision

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DOJEBANA 2D STRZELANKA")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 24)

player = Player(WIDTH//2, HEIGHT//2, hp=100)



ENEMY_SOUNDS = [
    pygame.mixer.Sound("sounds/ide_po_cb.mp3"),
    pygame.mixer.Sound("sounds/ty_gnoju.mp3"),
    pygame.mixer.Sound("sounds/bullet.mp3")
]
level = Level(WIDTH, HEIGHT, enemy_sounds=ENEMY_SOUNDS)
level.spawn_wave()

score = 0
running = True

while running:
    clock.tick(60)
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.shoot(pygame.mouse.get_pos())

    # UPDATE
    player.update(level.enemies, level.obstacles, WIDTH, HEIGHT, circle_rect_collision)
    for e in level.enemies[:]:
        e.update(player, level.obstacles, circle_rect_collision)

    if not level.enemies:
        level.next_wave()

    # DRAW
    level.draw(screen)
    player.draw(screen)

    hud = FONT.render(f"HP: {player.hp}  SCORE: {score}  WAVE: {level.wave}", True, (255,255,255))
    screen.blit(hud, (10,10))

    if player.hp <= 0:
        over = FONT.render("GAME OVER", True, (255,0,0))
        screen.blit(over, (WIDTH//2 - 80, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()

pygame.quit()
