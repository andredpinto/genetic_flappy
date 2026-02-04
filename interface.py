import pygame
import sys
import numpy as np
import random

from globals import *
from assets import *

pygame.init()
# Game font
game_font = pygame.font.Font(None, 40)

# Screen init
screen= pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy gay")
pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(400, 400, 30, 30))


new_bird= bird(300,300,screen)
tubes_list=[] #lista de tubos com tamanhos aleatórios

pygame.time.set_timer(pygame.USEREVENT, tube_frequency) #frequencia com que cria tubos (3s)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s or event.key == pygame.K_r:
                game_active = True 
                new_bird.jump() #dá um salto inicial
                tubes_list=[] #reseta a lista
                new_bird.rect.center = (300, 300) #reseta posição
                new_bird.y = 300
                new_bird.vel = 0
                score=0

            if event.key == pygame.K_SPACE:
                if game_active:
                    new_bird.jump()

        if event.type == pygame.USEREVENT and game_active:
            tubes_list.append(tube(random.randrange(100, 501, 20), screen)) #colocar na lista um novo tubo a cada 3s

    screen.fill(blue)
    if game_active:
        new_bird.move()

        for cur_tube in tubes_list[:]:
            cur_tube.move()
            if new_bird.rect.colliderect(cur_tube.rect1) or new_bird.rect.colliderect(cur_tube.rect2) or new_bird.y<0 or new_bird.y+30>668:
                game_active= False
                is_game_over= True

            if cur_tube.check() and len(tubes_list):
                tubes_list.remove(cur_tube)
            
            if cur_tube.count_pont():
                score+=1
    
    else:
        pygame.draw.rect(screen, (255, 100, 0), new_bird.rect)
        msg_surface = game_font.render("Press 'S' to start", True, (255, 255, 255)) #mensagem com indicação para inicial o jogo
        msg_rect = msg_surface.get_rect(center=(width/2, height/2))
        screen.blit(msg_surface, msg_rect)
        if is_game_over: game_over(score, screen)

    floor(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

# fim do loop

pygame.quit()
sys.exit()