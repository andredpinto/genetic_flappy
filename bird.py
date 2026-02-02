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
