from globals import *
import pygame

class bird:
    def __init__(self, x, y, screen):
        self.x=x
        self.y=y
        self.screen=screen
        self.vel= 0
        self.rect = pygame.Rect(x, y, 30, 30)
    
    def jump(self):
        self.vel=-6 # intensity of the jump
                    # higher (absolute) values make the bird jump higher
    
    def move(self):
        self.vel+= 0.25 # the higher the number, the stronger the gravity pull
        self.y += self.vel
        self.rect.y = int(self.y)
        pygame.draw.rect(self.screen, (255, 100, 0), self.rect)


class tube:
    def __init__(self, size, screen):
        # size defines the size of the top tube
        # the bigger the size value, the lower the opening between the tubes will be
        self.x= width
        self.y1= -2 # top of the screen
        self.y2= size+170
        self.size=size
        self.screen=screen
        self.espessura=80
        self.vel= game_speed #velocidade inicial do tubo
        self.rect1 = pygame.Rect(self.x, self.y1, self.espessura, size) #largura e altura do tubo superior
        self.rect2 = pygame.Rect(self.x, self.y2, self.espessura, height-size-170) #tamanho do tubo inferior
    
    def move(self):
        #self.vel+= 0.005 #velocidade com que se move
        self.x -= self.vel
        self.rect1.x = int(self.x)
        self.rect2.x = int(self.x)
        
        #desenho do tubo superior
        pygame.draw.rect(self.screen, green, self.rect1) 
        pygame.draw.rect(self.screen, dark_green, (self.x, 0, 10, self.size-2)) #sombra lateral
        pygame.draw.rect(self.screen, (0,0,0), self.rect1, 2) #contorno
        
        #desenho do tubo inferior
        pygame.draw.rect(self.screen, green , self.rect2) 
        pygame.draw.rect(self.screen, dark_green, (self.x, self.y2, 10, height)) #sombra lateral
        pygame.draw.rect(self.screen, (0,0,0), self.rect2, 2) #contorno

    def check(self):
        # Checks if tube is out of screen
        if self.x+100 < 0:
            return True
        return False

    def count_pont(self): #contador de pontuação
        if self.x+self.espessura==300: #se o quadrado passar pelo tubo sem bater
            return True
        return False


def floor(screen):
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


def game_over(score, screen):
    rect = pygame.Rect(100, 200, 550, 300)
    pygame.draw.rect(screen, purple, rect)
    pygame.draw.rect(screen, (0,0,0), rect, 2) #desenho do retangulo
    msg_surface = pygame.font.SysFont(None, 110).render("GAME OVER", True, (0,0,0)) 
    screen.blit(msg_surface, msg_surface.get_rect(center=(width/2, height/2-85))) #escrever game over
    msg_surface = pygame.font.SysFont(None, 60).render(f"Score: {score}" , True, (0,0,0)) 
    screen.blit(msg_surface, msg_surface.get_rect(center=(width/2, height/2-5))) #escrever a pontuação
    msg_surface = pygame.font.SysFont(None, 35).render("Press 'R' to restart" , True, (0,0,0)) 
    screen.blit(msg_surface, msg_surface.get_rect(center=(width/2, height/2+60))) #como fazer restart