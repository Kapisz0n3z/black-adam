# level.py

import random
from enemy import Enemy
from weapon import Weapon

class Obstacle:
    def __init__(self, x, y, w, h):
        self.rect = (x, y, w, h)

    def draw(self, screen):
        import pygame
        pygame.draw.rect(screen, (100,100,100), self.rect)


class Level:
    def __init__(self, width, height, enemy_sounds=None):
        self.width = width
        self.height = height
        self.wave = 1
        self.enemies = []
        self.obstacles = []
        self.enemy_sounds = enemy_sounds if enemy_sounds else []
        self.spawn_obstacles()

    def spawn_obstacles(self):
        # przykładowe przeszkody
        for _ in range(5):
            w, h = random.randint(50,150), random.randint(50,150)
            x, y = random.randint(0, self.width-w), random.randint(0, self.height-h)
            self.obstacles.append(Obstacle(x, y, w, h))

    def spawn_wave(self):

        image_path = "images/elo.png"

        num_enemies = self.wave * 3
        for _ in range(num_enemies):
            side = random.choice(["top","bottom","left","right"])
            if side=="top":
                x, y = random.randint(0, self.width), -20
            elif side=="bottom":
                x, y = random.randint(0, self.width), self.height+20
            elif side=="left":
                x, y = -20, random.randint(0, self.height)
            else:
                x, y = self.width+20, random.randint(0, self.height)

            if random.random() < 0.5:
                e = Enemy(
                    x, y,
                    hp=30+self.wave*10,
                    speed=random.uniform(1.5,2.5)+self.wave*0.1,
                    sounds=self.enemy_sounds, image_path=image_path
                )
            else:
                weapon = Weapon(cooldown=max(20,60-self.wave*5), bullet_speed=5+self.wave*0.2)
                e = Enemy(
                    x, y,
                    hp=50+self.wave*15,
                    speed=random.uniform(1,2)+self.wave*0.1,
                    weapon=weapon,
                    sounds=self.enemy_sounds, image_path=image_path
                )
            self.enemies.append(e)

    def next_wave(self):
        self.wave += 1
        self.spawn_wave()

    def draw(self, screen):
        # rysuj przeszkody
        for obs in self.obstacles:
            obs.draw(screen)
        # rysuj wrogów
        for e in self.enemies:
            e.draw(screen)
