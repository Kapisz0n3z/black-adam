# enemy.py

import random
import math
from weapon import Bullet
import pygame

class Enemy:
    def __init__(self, x, y, hp=50, speed=2, radius=14, weapon=None, sounds=None, image_path=None):
        self.x = x
        self.y = y
        self.hp = hp
        self.speed = speed
        self.radius = radius
        self.weapon = weapon
        self.bullets = []

        # timer mówienia wroga w klatkach (1-5 sekund przy 60 FPS)
        self.talk_timer = random.randint(1*60, 5*60)
        self.sounds = sounds if sounds else []

        if image_path:

            img = pygame.image.load(image_path).convert()  
            img.set_colorkey((255, 255, 255))  
            new_size = (self.radius*4, self.radius*4)  
            img = pygame.transform.scale(img, new_size)
            self.image = img
            self.radius = new_size[0] // 2  

        else:
            self.image = None

    def update(self, player, obstacles, collision_func):
        # --- ruch wroga z obsługą przeszkód ---
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            new_x = self.x + dx / dist * self.speed
            new_y = self.y + dy / dist * self.speed

            collision = False
            for obs in obstacles:
                if collision_func(new_x, new_y, self.radius, obs.rect):
                    collision = True
                    break
            if not collision:
                self.x = new_x
                self.y = new_y

        # --- strzał w kierunku gracza ---
        if self.weapon:
            self.weapon.update_cooldown()
            bullet = self.weapon.fire(self.x, self.y, (player.x, player.y))
            if bullet:
                self.bullets.append(bullet)

        # --- update pocisków wroga ---
        for b in self.bullets[:]:
            b.x += b.vx
            b.y += b.vy
            dist_to_player = math.hypot(b.x - player.x, b.y - player.y)
            if dist_to_player < b.radius + player.radius:
                player.hp -= 10
                self.bullets.remove(b)
            elif b.x < 0 or b.x > 2000 or b.y < 0 or b.y > 2000:
                self.bullets.remove(b)

        # --- timer mówienia przeciwnika ---
        self.talk_timer -= 1
        if self.talk_timer <= 0 and self.sounds:
            soundy = self.sounds[0:2]
            soundzik = random.choice(soundy)
            soundzik.play()  # odtwarzamy okrzyk wroga
            self.talk_timer = random.randint(1*60, 5*60)

    def draw(self, screen):
        import pygame

        if self.image:
            screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
        else:
            pygame.draw.circle(screen, (255,60,60), (int(self.x), int(self.y)), self.radius)

        for b in self.bullets:
            b.draw(screen)

    # --- nowa metoda dla trafień ---
    def take_damage(self, damage):
        self.hp -= damage
        if len(self.sounds) > 2:
            self.sounds[2].play()  
