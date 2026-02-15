import pygame
import sys
import numpy as np
import random
from collections import deque

from globals import *
from assets import *
from genetic import *

pygame.init()

# Game font
game_font = pygame.font.Font(None, 40)

# Screen init
screen= pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy gay")
pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(400, 400, 30, 30))

# Bird init
bird_stamp = 1     # Bird counter
# This dictionary will associate the "smart" birds (bird class and corresponding neural network)
# With their scores (frames they were alive), starting at 0
birds_fitness = {}
for i in range(generation_size):
    birds_fitness[smartBird(bird_x, 300, screen, number=bird_stamp, input_size=input_number)] = 0
    bird_stamp += 1
bird_lst = birds_fitness.keys()

tubes_list = deque()    # Tubes on screen
active_tubes = deque()  # Tubes in front of the bird

def reset():
    # Game reset
    global game_active, dead_birds, game_start, step
    game_active = True
    dead_birds=0
    tubes_list.clear()
    active_tubes.clear()
    pygame.time.set_timer(pygame.USEREVENT, tube_frequency)     # Timer for tube creation

    for b in bird_lst:
        b.jump()    # Initial jump
        b.rect.center = (bird_x, 300)   # Resets bird position
        b.y = 300
        b.vel = 0
        b.alive = True
        b.score = 0
        step = 0

pygame.time.set_timer(pygame.USEREVENT, tube_frequency)     # Timer for tube creation

# GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Key press handling
        if event.type == pygame.KEYDOWN:
            # Game reset
            if event.key == pygame.K_s or event.key == pygame.K_r:
                reset()
        
        # Tube generation
        if event.type == pygame.USEREVENT and game_active:
            # Add tube after interval determined by tube_frequency variable (globals)
            new_tube = Tube(random.randrange(100, 501, 20), screen)
            tubes_list.append(new_tube)
            active_tubes.append(new_tube)

    

    screen.fill(blue)   # Background

    if game_active:

        # Remove not-active tubes
        while len(active_tubes) and active_tubes[0].inactive_check():
            active_tubes.popleft()

        if len(active_tubes):
            cur_tube = active_tubes[0]  # Set active tube (the one directly in front of the bird)
        else:
            cur_tube = Tube(height/2, screen, ghost=True)   # Temporary "ghost tube", roughly in the middle of the screen
            # Needed for the start of the game, when no tubes are generated

        # ===== BIRD MOVEMENT ===== 
        for b in bird_lst:
            if not b.alive: continue

            birds_fitness[b] += 1

            # NEURAL NETWORK DECISION
            sensors = np.array([
                tube_vert_dist(b, cur_tube),
                tube_horiz_dist(b, cur_tube),
                floor_dist(b),
                norm_speed(b)
            ]).reshape((input_number,1))

            decision = b.think(sensors)

            if decision > 0.5: b.jump()

            b.move()

        # Move Tubes
        for tube in tubes_list:
            tube.move()

        # Verify colision 
        if len(tubes_list):
            # For each bird
            for b in bird_lst:
                if not b.alive: continue
                if b.rect.colliderect(cur_tube.rect1) or b.rect.colliderect(cur_tube.rect2) or b.y<0 or b.y+30>668:
                    b.alive= False
                    dead_birds+=1 # Incremento o núnero de pássaros que morreram
                   
                    if b.score>best_score:
                        best_score=b.score # Verifico se conseguiram a melhor pontuação até agora (corresponde ao ultimo pássaro a morer)

                    if dead_birds==generation_size:    # Verificar se todos os pássaros já morreram
                        game_active= False
                        is_game_over= True

                if cur_tube.count_pont():
                    b.score+=1

        # Remove offscreen tubes
        while len(tubes_list) and tubes_list[0].offscreen_check():
            tubes_list.popleft()
                
    
    else:
        for b in bird_lst:
            b.rect = pygame.Rect(b.x-13, b.y, 30, 30)
            pygame.draw.rect(screen, (255, 100, 0), b.rect)
            b.screen.blit(b.msg_surface, b.msg_surface.get_rect(center=(b.x+1, b.y+12)))
        msg_surface = game_font.render("Press 'S' to start", True, (255, 255, 255)) #mensagem com indicação para iniciar o jogo
        msg_rect = msg_surface.get_rect(center=(width/2, height/2))
        screen.blit(msg_surface, msg_rect)

        # GENERATION PASS LOGIC
        if is_game_over:
            bird_lst, bird_stamp = create_generation(birds_fitness, generation_size, screen, bird_stamp)
            birds_fitness = {b : 0 for b in bird_lst}   # Reset scores
            reset()

    floor(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

# fim do loop

pygame.quit()
sys.exit()