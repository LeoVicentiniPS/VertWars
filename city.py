import pygame
import math
import random
from graph import Graph

pygame.font.init()

COLOR_PLAYER = (50, 255, 50)  
COLOR_NEUTRAL = (150, 150, 150)
COLOR_ENEMY = (255, 50, 50)    
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

cities_image = [
    pygame.image.load("images/city_1.png"),
    pygame.image.load("images/city_2.png"),
    pygame.image.load("images/city_3.png"),
    pygame.image.load("images/city_4.png")
]
skyland = pygame.image.load("images/skyland.png")

class City:
    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.radius = 20  # Tamanho da cidade
        self.owner = owner  # player, enemy, ou 'neutral'
        self.og_owner = owner
        self.power = 0.0  # Recurso
        self.font = pygame.font.Font(None, 24) # Texto da cidade
        self.roads = []
        self.allies = []
        self.graph = None
        self.attack_timer = random.randint(300, 1000)
        self.update_image()

    def update_image(self):
        # Default index
        img_idx = 0 
        
        if self.owner == 'player':
            img_idx = 3  
        elif self.owner == 'enemy':
            img_idx = 0  
        else:
            img_idx = random.randint(1, 2)
            
        self.image = pygame.transform.scale(cities_image[img_idx], (self.radius*6, self.radius*6))
        self.land = pygame.transform.scale(skyland, (self.radius*6, self.radius*6))

    def reset(self):
        self.owner = self.og_owner
        self.power = 0.0
        self.roads = []
        self.allies = []
        self.graph = None
        self.update_image()

    def is_enemy(self):
        return self.owner == 'enemy' 

    def is_player(self):
        return self.owner == 'player' 

    def update(self):
        # Lógica in-game
        if self.owner == 'neutral' and self.power >= 100:
            self.power = 100
        else:
            growth_rate = 0.02 if self.owner == 'neutral' else 0.04
            self.power += growth_rate

    def draw(self, screen, is_selected):
        if self.owner == 'player':
            color = COLOR_PLAYER
        elif self.owner == 'enemy':
            color = COLOR_ENEMY
        else:
            color = COLOR_NEUTRAL

        #castle image
        castle_center = (self.x-self.radius*3, self.y-self.radius*3)
        land_center = (self.x-self.radius*3, self.y-self.radius*1)
        screen.blit(self.land, land_center)
        screen.blit(self.image, castle_center)
        
        #circle
        circle_center = (self.x-self.radius, self.y-self.radius)
        circle_surface = pygame.Surface((self.radius*2, self.radius*2))
        circle_surface.set_colorkey(COLOR_BLACK)
        circle_surface.set_alpha(180)
        pygame.draw.circle(circle_surface, color, (self.radius, self.radius), self.radius) 
        screen.blit(circle_surface, circle_center)
        
        #power text
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

    def _get_next_node(self, tupl):
        u, v, w = tupl #origem, destino e peso
        u_is_ally = u in self.allies
        v_is_ally = v in self.allies

        is_frontier = (u_is_ally and not v_is_ally) or (v_is_ally and not u_is_ally)
        return is_frontier

    def attempt_random_attack(self, roads):
    
        self.attack_timer -= 1
        if self.attack_timer > 0:
            return None
            
        #Tempo de ataque aleatório
        self.attack_timer = random.randint(300, 1000)
        if self.power < 20:
            return None
            
        #Acha os vértices conectados e retorna um aleatório
        neighbors = []
        for start, end in roads:
            if start == self:
                neighbors.append(end)
            elif end == self:
                neighbors.append(start)
                
        if neighbors:
            return random.choice(neighbors)
            
        return None
    
    def conquest(self, cities):

        self.allies = [cities.index(c) for c in cities if c.owner == self.owner]
        self.graph = Graph(cities)
        mst = self.graph.prim_mst()

        next_route_node = next(filter(self._get_next_node, mst), None)

        if next_route_node:
            u, v, weight = next_route_node

            if u in self.allies:
                source_idx = u
                target_idx = v
            else:
                source_idx = v
                target_idx = u

            if cities[source_idx].power > 10:
                self.roads.append(next_route_node)
                return (source_idx, target_idx)

            return (0, 0) #retorna nada esperando ter 10 de poder
        
        return (0,0)
        


    