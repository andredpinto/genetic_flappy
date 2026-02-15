from globals import *
import pygame
from neural_network import *

class Bird:
    def __init__(self, x, y, screen, number=None):
        self.x=x
        self.y=y
        self.screen=screen
        self.vel= 0
        self.rect = pygame.Rect(x, y, 30, 30)
        self.number = number
        if number:
            self.msg_surface = pygame.font.SysFont(None, 35).render(str(number) , True, (0,0,0))    # Escrever um número para identificar cada quadrado
        self.score=0 # pontuação de cada pássaro
        self.alive= True
    
    def jump(self):
        self.vel=-6 # intensity of the jump
                    # higher (absolute) values make the bird jump higher
    
    def move(self):
        self.vel+= 0.25 # the higher the number, the stronger the gravity pull
        self.y += self.vel
        self.rect.y = int(self.y)
        pygame.draw.rect(self.screen, (255, 100, 0), self.rect)
        if self.number:
            self.screen.blit(self.msg_surface, self.msg_surface.get_rect(center=(self.x+1, self.y+12)))


class smartBird(Bird, NeuralNetwork):
    # This class joins the Bird and NeuralNetwork classes, for convenience
    def __init__(self, x, y, screen, number, input_size):
        Bird.__init__(self, x, y, screen, number)
        NeuralNetwork.__init__(self, input_size)


class Tube:
    def __init__(self, size, screen, ghost = False):
        # size defines the size of the top tube
        # the bigger the size value, the lower the opening between the tubes will be
        self.x= width
        self.y1= -2 # top of the screen
        self.y2= size+170
        self.size=size
        self.screen=screen
        self.espessura=80
        self.vel= game_speed #velocidade inicial do tubo
        # Ghost attribute makes tube not visible
        self.ghost = ghost
        if not ghost:
            self.rect1 = pygame.Rect(self.x, self.y1, self.espessura, size) #largura e altura do tubo superior
            self.rect2 = pygame.Rect(self.x, self.y2, self.espessura, height-size-170) #tamanho do tubo inferior
    
    def move(self):
        #self.vel+= 0.005 #velocidade com que se move
        self.x -= self.vel
        self.rect1.x = int(self.x)
        self.rect2.x = int(self.x)
        
        if not self.ghost:
            #desenho do tubo superior
            pygame.draw.rect(self.screen, green, self.rect1) 
            pygame.draw.rect(self.screen, dark_green, (self.x, 0, 10, self.size-2)) #sombra lateral
            pygame.draw.rect(self.screen, (0,0,0), self.rect1, 2) #contorno
            
            #desenho do tubo inferior
            pygame.draw.rect(self.screen, green , self.rect2) 
            pygame.draw.rect(self.screen, dark_green, (self.x, self.y2, 10, height)) #sombra lateral
            pygame.draw.rect(self.screen, (0,0,0), self.rect2, 2) #contorno

    def offscreen_check(self):
        # Checks if tube is out of screen
        return self.x+100 < 0

    def inactive_check(self):
        # Checks if tube is in front of bird
        return self.x + self.espessura < bird_x
        
    def count_pont(self): #contador de pontuação
        return self.x+self.espessura==300 #se o quadrado passar pelo tubo sem bater


def floor(screen):
    global floor_x

    #desenho da terra
    pygame.draw.rect(screen, brown , pygame.Rect(0, floor_y, 750, 80))
    #pygame.draw.line(screen, (0,0,0), (0, 670), (750, 670), 2)
    
    #desenho da relva
    floor_x -= game_speed
    
   
    if floor_x <= -40:
        floor_x = 0 #se o chão andou mais de 40 pixeis (tamanho do padrão), volta ao zero
    
    for i in range(0, width + 50, 40): 
        pos_x = i + floor_x
        
        pygame.draw.rect(screen, light_green, (pos_x, floor_y, 40, 15)) #verde claro da relva
        pygame.draw.rect(screen, dark_green, (pos_x + 20, floor_y, 20, 15))  #verde escuro da relva
        pygame.draw.line(screen, (0,0,0), (pos_x, 685), (pos_x+40, 685), 2)#linha preta
    
    pygame.draw.line(screen, (0,0,0), (0, 670), (width, floor_y), 3) #linha preta no topo do chão


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

# Some auxiliar functions for the neural network

def norm_dist(a, b, n):
    # Returns difference (distance) from a to b, normalized with the n value, for input for the Neural Network
    return (b-a)/n

def tube_vert_dist(bird : Bird, tube : Tube):
    return norm_dist(bird.y, tube.y2, height)

def tube_horiz_dist(bird : Bird, tube : Tube):
    return norm_dist(bird.x, tube.x, width)

def floor_dist(bird : Bird):
    return norm_dist(bird.y, floor_y, height)

def norm_speed(bird : Bird):
    # Normalized bird speed, max speed empirically verified, may change
    max_bird_speed = 18.
    return bird.vel / max_bird_speed

def log_dist(bird : Bird, tube : Tube):
    # For debugging purposes
    print("Vertical distance to tube", tube_vert_dist(bird, tube))
    print("Horizontal distance to tube", tube_horiz_dist(bird, tube))
    print("Distance to floor", floor_dist(bird))
    print("Relative bird speed", norm_speed(bird))
    print("============================")