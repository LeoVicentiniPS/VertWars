import pygame
import math
from graph import Graph
from troop import TroopGroup

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
        self.og_owner = owner
        self.power = 0.0  # Recurso
        self.font = pygame.font.Font(None, 24) # Texto da cidade
        self.roads = []
        self.allies = []
        self.graph = None

    def reset(self):
        self.owner = self.og_owner
        self.power = 0.0
        self.roads = []
        self.allies = []
        self.graph = None

    def is_enemy(self):
        return self.owner == 'enemy' 

    def is_player(self):
        return self.owner == 'player' 

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

    def _get_next_node(self, tupl):
        return True if tupl not in self.roads and (tupl[0] in self.allies or tupl[1] in self.allies) else False 

    def conquest(self, cities):
        cities_copy = [*cities]
        
        cities_not_conquered = [city for city in cities_copy if city.owner != self.owner]
        
        if (len(cities_not_conquered)>1):
            cities_copy.pop(0)
            self.allies = [cities_copy.index(city) for city in cities_copy if city.owner == self.owner]
            if (self.graph == None):
                self.graph = Graph(cities_copy)
            mst = self.graph.prim_mst()
            self.roads = [road for road in mst if road[0] in self.allies and road[1] in self.allies ]
            next_route_node = next(filter(self._get_next_node, mst), None)
            nearest_city = next_route_node[0] if next_route_node[0] in self.allies else next_route_node[1]
            target_city = next_route_node[0] if nearest_city == next_route_node[1] else next_route_node[1]
            return (nearest_city+1, target_city+1)
        else:
            player_city = cities_copy.pop(0)
            distances = [math.sqrt((player_city.x - city.x)**2 + (player_city.y - city.y)**2) for city in cities_copy]
            min_distance = min(distances)
            return (distances.index(min_distance)+1, 0)
        


    