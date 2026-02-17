import pygame
import sys
import numpy as np
import random
from collections import deque
import json
from pathlib import Path

from globals import *
from assets import *
from genetic import *

pygame.init()

# Game font
game_font = pygame.font.Font(None, 40)

# Screen init
screen= pygame.display.set_mode((width, height))
pygame.display.set_caption("Bird Uprising")
pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(400, 400, 30, 30))

# ======= BIRD INIT =======
bird_stamp = 1     # Bird counter

# This dictionary will associate the "smart" birds (bird class and corresponding neural network)
# With their scores (frames they were alive), starting at 0
birds_fitness = {}

# Loading save file, if it exists
file_path = Path(save_file)

if file_path.exists() and file_path.stat().st_size > 0: # Save file exists and is not empty
    with open(save_file, "r") as f:
        data = json.load(f)

    n_birds = len(data)

    saved_birds = []
    for b in data:
        new_bird = smartBird(bird_x, 300, screen, bird_stamp, input_number)
        bird_stamp += 1
        new_bird.setDNA(np.array(b))
        saved_birds.append(new_bird)

    if n_birds < generation_size:
        bird_lst, bird_stamp = create_generation(saved_birds, generation_size, screen, bird_stamp)
    else:
        bird_lst = saved_birds[:generation_size]
        bird_stamp += generation_size

    birds_fitness = {b : 0 for b in bird_lst}

    

# If no save file is present, randomly create birds
else:
    for i in range(generation_size):
        birds_fitness[smartBird(bird_x, 300, screen, number=bird_stamp, input_size=input_number)] = 0
        bird_stamp += 1

    bird_lst = birds_fitness.keys()
# =========================

tubes_list = deque()    # Tubes on screen
active_tubes = deque()  # Tubes in front of the bird

def reset():
    # Game reset
    global game_active, dead_birds, gen_count
    game_active = True
    dead_birds=0
    tubes_list.clear()
    active_tubes.clear()

    gen_count+=1
    print (f"Generation number {gen_count}") # só para debug

    pygame.time.set_timer(pygame.USEREVENT, tube_frequency)     # reset timer, else first tube may generate out of place after reset

    for b in bird_lst:
        b.jump()    # Initial jump
        b.rect.center = (bird_x, 300)   # Resets bird position
        b.y = 300
        b.vel = 0
        b.alive = True
        b.score = 0

pygame.time.set_timer(pygame.USEREVENT, tube_frequency)     # Timer for tube creation
gen_count = 0

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

        # Move Tubes
        for tube in tubes_list:
            tube.move()

        # Remove not-active tubes
        while len(active_tubes) and active_tubes[0].inactive_check():
            active_tubes.popleft()

        # Check active tube
        if len(active_tubes):
            cur_tube = active_tubes[0]  # Set active tube (the one directly in front of the bird)
        else:
            cur_tube = Tube(height/2, screen, ghost=True)   # Temporary "ghost tube", roughly in the middle of the screen
            # Needed for when or if there are no generated tubes (like in the beggining of the game)

        # ===== BIRD MOVEMENT ===== 
        for b in bird_lst:
            if not b.alive: continue

            birds_fitness[b] += 1

            # Verify colision with active tube
            if not cur_tube.ghost:
                if b.rect.colliderect(cur_tube.rect1) or b.rect.colliderect(cur_tube.rect2) or b.y<0 or b.y+30>=floor_y:    # bird height is 30
                    b.alive= False
                    dead_birds+=1 # Incremento o núnero de pássaros que morreram
                    
                    if b.score>best_score:
                        best_score=b.score # Verifico se conseguiram a melhor pontuação até agora (corresponde ao ultimo pássaro a morer)

                    # Checks if game end conditions are met
                    if optimize: end_cond = generation_size - dead_birds <= elite_number
                    else: end_cond = dead_birds >= generation_size
                    if end_cond:
                        game_active= False
                        is_game_over= True

            if cur_tube.count_pont():
                b.score+=1

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

        # Remove offscreen tubes
        while len(tubes_list) and tubes_list[0].offscreen_check():
            tubes_list.popleft()
                
    
    else:
        if is_game_over:
            # Saving best birds
            best = get_best(birds_fitness)
            save = [b.getDNA().tolist() for b in best]
            with open(save_file, "w") as f:
                json.dump(save, f, indent=4)

            # Next Generation
            bird_lst, bird_stamp = create_generation(birds_fitness, generation_size, screen, bird_stamp)
            birds_fitness = {b : 0 for b in bird_lst}   # Reset scores
            reset()

        # Not game over and not game active means its game start
        else:
            for b in bird_lst:
                b.rect = pygame.Rect(b.x-13, b.y, 30, 30)
                pygame.draw.rect(screen, (255, 100, 0), b.rect)
                b.screen.blit(b.msg_surface, b.msg_surface.get_rect(center=(b.x+1, b.y+12)))
            msg_surface = game_font.render("Press 'S' to start", True, (255, 255, 255))     # Message displayed on screen
            msg_rect = msg_surface.get_rect(center=(width/2, height/2))
            screen.blit(msg_surface, msg_rect)


    floor(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)