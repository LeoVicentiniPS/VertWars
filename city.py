import pygame
import math

pygame.font.init

COLOR_PLAYER = (50, 255, 50)  
COLOR_NEUTRAL = (150, 150, 150)
COLOR_ENEMY = (255, 50, 50)    
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)


class City:
    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.radius = 20  # Tamanho da cidade
        self.owner = owner  # player, enemy, ou 'neutral'
        self.power = 0.0  # Recurso
        self.font = pygame.font.Font(None, 24) # Texto da cidade
        
    def update(self):
        # Lógica in-game
        if self.owner == 'neutral' and self.power >= 100:
            self.power = 100
        else:
            growth_rate = 0.02 if self.owner == 'neutral' else 0.1
            self.power += growth_rate

    def draw(self, screen, is_selected):
        if self.owner == 'player':
            color = COLOR_PLAYER
        elif self.owner == 'enemy':
            color = COLOR_ENEMY
        else:
            color = COLOR_NEUTRAL
            
        # pygame.draw.circle(surface, color, center_tuple, radius)
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)
        
        text_surface = self.font.render(str(int(self.power)), True, COLOR_BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x, self.y)
        screen.blit(text_surface, text_rect)

        if is_selected:
            pygame.draw.circle(screen, COLOR_WHITE, (self.x, self.y), self.radius + 2, 3)
            
    # Verifica mouse dentro do raio do circulo
    def is_clicked(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        distance = math.sqrt((self.x - mouse_x)**2 + (self.y - mouse_y)**2)
        return distance <= self.radius
