import pygame
import sys
import numpy as np
import random

from bird import bird

pygame.init()

# Screen settings
width=750
height=750
floor_x=0
game_active= False
is_game_over= False
game_speed= 2
score=0

game_font = pygame.font.Font(None, 40)

# Color palette
blue= (40, 116, 178)
green= (0, 180, 0)
dark_green = (0, 130, 0)
light_green = (100, 200, 100)
brown=  (120, 64, 8)
dark_brown = (120, 64, 8)
purple= (159, 95, 159)

# Screen init
screen= pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy gay")
pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(400, 400, 30, 30))

class tube:
    def __init__(self, size):
        self.x1= width
        self.y1= -2
        self.x2= width
        self.y2= size+170
        self.size=size
        self.espessura=80
        self.vel= game_speed #velocidade inicial do tubo
        self.rect1 = pygame.Rect(self.x1, self.y1, self.espessura, size) #largura e altura do tubo superior
        self.rect2 = pygame.Rect(self.x2, self.y2, self.espessura, height-size-170) #tamanho do tubo inferior
    
    def move(self):
        #self.vel+= 0.005 #velocidade com que se move
        self.x1 -= self.vel
        self.x2 -= self.vel
        self.rect1.x = int(self.x1)
        self.rect2.x = int(self.x2)
        
        #desenho do tubo superior
        pygame.draw.rect(screen, green, self.rect1) 
        pygame.draw.rect(screen, dark_green, (self.x1, 0, 10, self.size-2)) #sombra lateral
        pygame.draw.rect(screen, (0,0,0), self.rect1, 2) #contorno
        
        #desenho do tubo inferior
        pygame.draw.rect(screen, green , self.rect2) 
        pygame.draw.rect(screen, dark_green, (self.x2, self.y2, 10, height)) #sombra lateral
        pygame.draw.rect(screen, (0,0,0), self.rect2, 2) #contorno

    def check(self):
        if self.x1+100 < 0:
            return True
        return False

    def count_pont(self): #contador de pontuação
        if self.x1+self.espessura==300: #se o quadrado passar pelo tubo sem bater
            return True
        return False

def floor():
    global floor_x

    #desenho da terra
    pygame.draw.rect(screen, brown , pygame.Rect(0, 670, 750, 80))
    #pygame.draw.line(screen, (0,0,0), (0, 670), (750, 670), 2)
    
    #desenho da relva
    floor_x -= game_speed
    
   
    if floor_x <= -40:
        floor_x = 0 #se o chão andou mais de 40 pixeis (tamanho do padrão), volta ao zero
    
    for i in range(0, width + 50, 40): 
        pos_x = i + floor_x
        
        pygame.draw.rect(screen, light_green, (pos_x, 670, 40, 15)) #verde claro da relva
        pygame.draw.rect(screen, dark_green, (pos_x + 20, 670, 20, 15))  #verde escuro da relva
        pygame.draw.line(screen, (0,0,0), (pos_x, 685), (pos_x+40, 685), 2)#linha preta
    
    pygame.draw.line(screen, (0,0,0), (0, 670), (width, 670), 3) #linha preta no topo do chão

def game_over(score):
    rect = pygame.Rect(100, 200, 550, 300)
    pygame.draw.rect(screen, purple, rect)
    pygame.draw.rect(screen, (0,0,0), rect, 2) #desenho do retangulo
    msg_surface = pygame.font.SysFont(None, 110).render("GAME OVER", True, (0,0,0)) 
    screen.blit(msg_surface, msg_surface.get_rect(center=(width/2, height/2-85))) #escrever game over
    msg_surface = pygame.font.SysFont(None, 60).render(f"Score: {score}" , True, (0,0,0)) 
    screen.blit(msg_surface, msg_surface.get_rect(center=(width/2, height/2-5))) #escrever a pontuação
    msg_surface = pygame.font.SysFont(None, 35).render("Press 'R' to restart" , True, (0,0,0)) 
    screen.blit(msg_surface, msg_surface.get_rect(center=(width/2, height/2+60))) #como fazer restart

new_bird= bird(300,300,screen)
tubes_list=[] #lista de tubos com tamanhos aleatórios

pygame.time.set_timer(pygame.USEREVENT, 1850) #frequencia com que cria tubos (3s)

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
            tubes_list.append(tube(random.randrange(100, 501, 20))) #colocar na lista um novo tubo a cada 3s

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
        if is_game_over: game_over(score)

    floor()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

# fim do loop

pygame.quit()
sys.exit()
