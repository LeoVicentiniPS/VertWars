import pygame
import random
from city import City 
from troop import TroopGroup 

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
GAME_TITLE = "VertWars"
FPS = 60

# Inicialização
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Listas
cities = [
    City(100, 100, 'player'),
    City(random.randint(150, 750), random.randint(150, 650), 'neutral'),
    City(random.randint(150, 750), random.randint(150, 650), 'neutral'),
    City(random.randint(150, 750), random.randint(150, 650), 'neutral'),
    City(random.randint(150, 750), random.randint(150, 650), 'neutral'),
    City(800, 700, 'enemy')
]
selected_city = None
troop_groups = []

running = True
# Game Loop
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicked_city = None

            for city in cities:
                if city.is_clicked(mouse_pos):
                    clicked_city = city
                    break

            if clicked_city:
                # Primeiro clique para selecionar cidade origem
                if selected_city is None:
                    if clicked_city.owner == 'player':
                        selected_city = clicked_city

                # Segundo clique para selecionar cidade destino
                else:
                    if selected_city.power > 10 and clicked_city != selected_city:
                        new_troop = TroopGroup(selected_city, clicked_city)
                        troop_groups.append(new_troop)
                
                    selected_city = None
            else:
                selected_city = None

    # Updates
    for city in cities:
        city.update()

    for troop in troop_groups:
        troop.update()
        
    troop_groups = [troop for troop in troop_groups if troop.is_alive]

    # Draws
    screen.fill((0, 0, 0)) 

    for city in cities:
        is_selected = (city == selected_city)
        city.draw(screen, is_selected)

    for troop in troop_groups:
        troop.draw(screen)

    # Coisa pra funcionar
    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()