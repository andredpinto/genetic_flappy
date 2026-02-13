import pygame
import sys
import numpy as np
import random
import time

from globals import *
from assets import *

pygame.init()
# Game font
game_font = pygame.font.Font(None, 40)

# Screen init
screen= pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy gay")
pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(400, 400, 30, 30))


bird_lst=[] # Lista com todos os pássaros que vão jogar ao mesmo tempo
for i in range(1,bird_number+1):
    bird_lst.append(bird(300,300,screen, i))

tubes_list=[] #lista de tubos com tamanhos aleatórios

pygame.time.set_timer(pygame.USEREVENT, tube_frequency) #frequencia com que cria tubos (3s)

step = 0
delay = 400  # ms
next_time = pygame.time.get_ticks() + delay

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s or event.key == pygame.K_r:
                game_active = True
                false_num=0
                best_score=0
                tubes_list=[] #reseta a lista

                for b in bird_lst:
                    b.jump() #dá um salto inicial
                    b.rect.center = (300, 300) #reseta posição
                    b.y = 300
                    b.vel = 0
                    b.alive = True
                    b.score = 0
                    step = 0
                    next_time = pygame.time.get_ticks() + delay
        
        if event.type == pygame.USEREVENT and game_active:
            tubes_list.append(tube(random.randrange(100, 501, 20), screen)) #colocar na lista um novo tubo a cada 3s
    
    current_time = pygame.time.get_ticks()

    if game_active and step < len(movimento) and current_time >= next_time:

        # Aplica salto a todos os 1's da linha
        for j, val in enumerate(movimento[step]):
            if val == 1:
                bird_lst[j].jump()  # salto aplicado imediatamente
            print (val)
        step += 1
        next_time += delay  # espera 0.5s para a próxima linha

    screen.fill(blue)
    if game_active:
        for b in bird_lst:
            if not b.alive: continue

            b.move()

        for cur_tube in tubes_list[:]:
            cur_tube.move()
          
            for b in bird_lst:
                if not b.alive: continue
                if b.rect.colliderect(cur_tube.rect1) or b.rect.colliderect(cur_tube.rect2) or b.y<0 or b.y+30>668:
                    b.alive= False
                    false_num+=1 # Incremento o núnero de pássaros que morreram
                   
                    if b.score>best_score:
                        best_score=b.score # Verifico se conseguiram a melhor pontuação até agora (corresponde ao ultimo pássaro a morer)

                    if false_num==bird_number:    # Verificar se todos os pássaros já morreram
                        game_active= False
                        is_game_over= True

                if cur_tube.count_pont():
                    b.score+=1

            if cur_tube.check() and len(tubes_list): 
                tubes_list.remove(cur_tube) # retirar tubos da lista quando saem do ecrã
                
                
    
    else:
        for b in bird_lst:
            b.rect = pygame.Rect(b.x-13, b.y, 30, 30)
            pygame.draw.rect(screen, (255, 100, 0), b.rect)
            b.screen.blit(b.msg_surface, b.msg_surface.get_rect(center=(b.x+1, b.y+12)))
        msg_surface = game_font.render("Press 'S' to start", True, (255, 255, 255)) #mensagem com indicação para iniciar o jogo
        msg_rect = msg_surface.get_rect(center=(width/2, height/2))
        screen.blit(msg_surface, msg_rect)
        if is_game_over: game_over(best_score, screen)

    floor(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

# fim do loop

pygame.quit()
sys.exit()