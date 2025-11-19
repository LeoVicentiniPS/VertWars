import pygame
import math

COLOR_PLAYER = (50, 255, 50) 
COLOR_ENEMY = (255, 50, 50)   

TROOP_SPEED = 2

class TroopGroup:
    def __init__(self, source_city, target_city):
        self.owner = source_city.owner
        self.source = source_city
        self.target = target_city
        self.x = source_city.x
        self.y = source_city.y
        # Atributos
        self.radius = 8 
        self.power = source_city.power / 2.0
        source_city.power /= 2.0
        self.is_alive = True
        # Caminho
        dx = self.target.x - self.source.x
        dy = self.target.y - self.source.y
        distance = math.sqrt(dx**2 + dy**2)
        # Tirar esse if daqui depois
        if distance > 0:
            self.vel_x = (dx / distance) * TROOP_SPEED
            self.vel_y = (dy / distance) * TROOP_SPEED
        else:
            self.vel_x = 0
            self.vel_y = 0

    def update(self):
        # Movimento
        self.x += self.vel_x
        self.y += self.vel_y
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        # Chegada
        if distance < self.target.radius:
            self.handle_arrival()

    def handle_arrival(self):
        self.is_alive = False
        # Reforço
        if self.target.owner == self.owner:
            self.target.power += self.power
        # Ataque
        else:
            self.target.power -= self.power
            if self.target.power < 0:
                self.target.owner = self.owner
                self.target.power = abs(self.target.power)

    def draw(self, screen):
        color = COLOR_PLAYER if self.owner == 'player' else COLOR_ENEMY  
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)