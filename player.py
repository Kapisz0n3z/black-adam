# player.py

import pygame
from weapon import Bullet

class Player:
    def __init__(self, x, y, speed=5, hp=100):
        self.x = x
        self.y = y
        self.speed = speed
        self.hp = hp
        self.radius = 12
        self.bullets = []
        self.cooldown_timer = 0

    def update_cooldown(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

    def move(self, dx, dy, obstacles, width, height, collision_func):
        new_x = self.x + dx
        new_y = self.y + dy

        collision = False
        for obs in obstacles:
            if collision_func(new_x, new_y, self.radius, obs.rect):
                collision = True
                break

        if not collision:
            self.x = max(0, min(width, new_x))
            self.y = max(0, min(height, new_y))

    def shoot(self, target_pos):
        if self.cooldown_timer == 0:
            mx, my = target_pos
            import math
            angle = math.atan2(my - self.y, mx - self.x)
            bullet = Bullet(self.x, self.y, math.cos(angle)*10, math.sin(angle)*10)
            self.bullets.append(bullet)
            self.cooldown_timer = 10

    def update(self, enemies, obstacles, width, height, collision_func):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_w]: dy -= self.speed
        if keys[pygame.K_s]: dy += self.speed
        if keys[pygame.K_a]: dx -= self.speed
        if keys[pygame.K_d]: dx += self.speed

        self.move(dx, dy, obstacles, width, height, collision_func)
        self.update_cooldown()

        # update pocisków
        for b in self.bullets[:]:
            b.x += b.vx
            b.y += b.vy
            for e in enemies[:]:
                import math
                dist = math.hypot(b.x - e.x, b.y - e.y)
                if dist < b.radius + e.radius:
                    e.take_damage(20)
                    if e.hp <= 0:
                        enemies.remove(e)
                    if b in self.bullets:
                        self.bullets.remove(b)
                    break
            if b.x < 0 or b.x > width or b.y < 0 or b.y > height:
                if b in self.bullets:
                    self.bullets.remove(b)

    def draw(self, screen):
        pygame.draw.circle(screen, (0,160,255), (int(self.x), int(self.y)), self.radius)
        for b in self.bullets:
            b.draw(screen)
