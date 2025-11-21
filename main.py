import pygame
import random
from city import City
from troop import TroopGroup 
from graph import Graph

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

COLOR_WHITE = (0, 0, 0)
GAME_TITLE = "VertWars"
FPS = 60


# Inicialização
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

bg = pygame.image.load("background.jpg")

ENEMYACTION = pygame.USEREVENT + 1
WIN = pygame.USEREVENT + 3
LOSE = pygame.USEREVENT + 4
pygame.time.set_timer(ENEMYACTION, 2000)

enemy = City(800, 700, 'enemy')
player = City(100, 100, 'player')
lvl = 0

# Listas
cities = [
    player,
    City(random.randint(150, 750), random.randint(150, 650), 'neutral'),
    City(random.randint(150, 750), random.randint(150, 650), 'neutral'),
    City(random.randint(150, 750), random.randint(150, 650), 'neutral'),
    City(random.randint(150, 750), random.randint(150, 650), 'neutral'),
    City(random.randint(150, 750), random.randint(150, 650), 'neutral'),
    enemy,
]



selected_city = None
troop_groups = []
running = True

def show_go_screen(win):
    screen.blit(bg, (0, 0))
    text_surface = pygame.font.Font(None, 24).render("Press space bar to play again" if not win else "Press space bar to next lvl", True, COLOR_WHITE)
    screen.blit(text_surface, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 7 / 8))
    pygame.display.flip()
    done = False
    running = True

    player.reset()
    enemy.reset()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if(win): lvl += 1
                    cities = [
                        player,
                        *[City(random.randint(150, 750), random.randint(150, 650), 'neutral') for i in range (5+lvl)],
                        enemy,
                    ]
                    done = True

        clock.tick(FPS)
    return running


# Game Loop
while running:

    win = not any(city.is_enemy() for city in cities)
    lose = not any(city.is_player() for city in cities)

    if (win):
        pygame.event.post(pygame.event.Event(WIN, {}))
    if (lose):
        pygame.event.post(pygame.event.Event(LOSE, {}))

    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == WIN:
            show_go_screen(True)

        if event.type == LOSE:
            show_go_screen(False)

        if event.type == ENEMYACTION:
            enemy_city, target_city = enemy.conquest(cities)
            new_troop = TroopGroup(cities[enemy_city], cities[target_city])
            troop_groups.append(new_troop)
            

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
                    if selected_city.power > 10 and clicked_city != selected_city :
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
    screen.blit(bg, (0, 0))

    for city in cities:
        is_selected = (city == selected_city)
        city.draw(screen, is_selected)

    for troop in troop_groups:
        troop.draw(screen)

    # Coisa pra funcionar
    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()