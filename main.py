import pygame
import random
from graph import Graph
from city import City
from troop import TroopGroup 

#global variables
COLOR_GREEN = (0, 225, 0)
COLOR_RED = (225, 0, 0)
COLOR_WHITE= (225, 225, 225)
GAME_TITLE = "VertWars"
FPS = 60

#init
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

#set background
bg = pygame.image.load("images/background.jpg")
go_bg = pygame.image.load("images/go_background.jpg")
win_bg = pygame.image.load("images/win_background.png")
start_sc = pygame.image.load("images/start_screen.png")



#set events
ENEMYACTION = pygame.USEREVENT + 1
WIN = pygame.USEREVENT + 3
LOSE = pygame.USEREVENT + 4
pygame.time.set_timer(ENEMYACTION, 2000)

last_main_source_idx = -1 # Para saber qual cidade está com MST

enemy = City(800, 700, 'enemy')
player = City(100, 100, 'player')
lvl = 0

#game variables
running = True
selected_city = None
troop_groups = []
roads = []
cities = [
    player,
    City(random.randint(150, SCREEN_WIDTH - 150), random.randint(150, SCREEN_HEIGHT - 150), 'neutral'),
    City(random.randint(150, SCREEN_WIDTH - 150), random.randint(150, SCREEN_HEIGHT - 150), 'neutral'),
    City(random.randint(150, SCREEN_WIDTH - 150), random.randint(150, SCREEN_HEIGHT - 150), 'neutral'),
    City(random.randint(150, SCREEN_WIDTH - 150), random.randint(150, SCREEN_HEIGHT - 150), 'neutral'),
    City(random.randint(150, SCREEN_WIDTH - 150), random.randint(150, SCREEN_HEIGHT - 150), 'neutral'),
    City(random.randint(150, SCREEN_WIDTH - 150), random.randint(150, SCREEN_HEIGHT - 150), 'neutral'),
    enemy,
]

def show_end_lvl_screen(win):

    screen.blit(pygame.transform.scale(go_bg if not win else win_bg, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
    title = pygame.font.Font(None, 48).render("GAME OVER" if not win else "YOU WIN", True, COLOR_WHITE)
    description = pygame.font.Font(None, 24).render("Press space bar to play again" if not win else "Press space bar to next lvl", True, COLOR_WHITE)
    screen.blit(title, ((SCREEN_WIDTH / 2)-100, (SCREEN_HEIGHT / 2)-50))
    screen.blit(description, ((SCREEN_WIDTH / 2)-90, SCREEN_HEIGHT / 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

    global cities, troop_groups, running, lvl
    running = True
    troop_groups = []

    for city in cities:
        city.reset()

    if win:
        lvl += 1

def show_start_screen():
    # Draw the background
    screen.blit(pygame.transform.scale(start_sc, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
    
    instruction_font = pygame.font.Font(None, 40)
    instruction_text = instruction_font.render("Press SPACE to Start", True, COLOR_WHITE)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))

    background_rect = instruction_rect.inflate(20, 10)
    pygame.draw.rect(screen, (0, 0, 0), background_rect)

    screen.blit(instruction_text, instruction_rect)
    
    pygame.display.flip()
    
    done = False  
    while not done:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE:
                    done = True 
show_start_screen()

def generate_roads():
    global roads
    
    temp_graph = Graph(cities)
    mst_edges = temp_graph.prim_mst()
    
    roads = []

    for u_index, v_index, weight in mst_edges:
        start_city = cities[u_index]
        end_city = cities[v_index]
        roads.append((start_city, end_city))

generate_roads()

def is_connected(city_a, city_b):
    return (city_a, city_b) in roads or (city_b, city_a) in roads

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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == WIN:
            show_end_lvl_screen(True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if event.type == LOSE:
            show_end_lvl_screen(False)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        #IA do inimigo
        if event.type == ENEMYACTION:
            source_idx, target_idx = enemy.conquest(cities)
            # Garante que os índices são válidos e diferentes 
            if source_idx != target_idx and source_idx < len(cities) and target_idx < len(cities):

                last_main_source_idx = source_idx #Cidade principal
                source_city = cities[source_idx]
                target_city = cities[target_idx]

                if source_city.power > 10:
                    new_troop = TroopGroup(source_city, target_city)
                    troop_groups.append(new_troop)

        #Player            
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
                    if selected_city.power > 10 and clicked_city != selected_city and is_connected(selected_city, clicked_city) :
                        new_troop = TroopGroup(selected_city, clicked_city)
                        troop_groups.append(new_troop)
                
                    selected_city = None
            else:
                selected_city = None

    # Updates
    for city in cities:
        city.update()
        if city.owner == 'enemy' and cities.index(city) != last_main_source_idx:
            target = city.attempt_random_attack(roads)
            if target:
                new_troop = TroopGroup(city, target)
                troop_groups.append(new_troop)
                
    for troop in troop_groups:
        troop.update()
        
    troop_groups = [troop for troop in troop_groups if troop.is_alive]

    # Draws
    screen.blit(pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

    for start, end in roads:
        pygame.draw.line(screen, (105, 105, 105), (start.x, start.y), (end.x, end.y), 12)
        pygame.draw.line(screen, (139, 69, 19), (start.x, start.y), (end.x, end.y), 8)

    for city in cities:
        is_selected = (city == selected_city)
        city.draw(screen, is_selected)

    for troop in troop_groups:
        troop.draw(screen)

    #fps tick for game loop
    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()

