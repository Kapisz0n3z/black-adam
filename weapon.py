# weapon.py

import math

class Bullet:
    def __init__(self, x, y, vx, vy, radius=5):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        import pygame
        pygame.draw.circle(screen, (255,255,0), (int(self.x), int(self.y)), self.radius)


class Weapon:
    def __init__(self, cooldown=60, bullet_speed=5):
        self.cooldown = cooldown
        self.bullet_speed = bullet_speed
        self.timer = 0

    def update_cooldown(self):
        if self.timer > 0:
            self.timer -= 1

    def fire(self, x, y, target):
        if self.timer == 0:
            tx, ty = target
            angle = math.atan2(ty - y, tx - x)
            bullet = Bullet(x, y, math.cos(angle)*self.bullet_speed, math.sin(angle)*self.bullet_speed)
            self.timer = self.cooldown
            return bullet
        return None
