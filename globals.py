# Global 
game_active= False
is_game_over= False

# Screen settings
width=750
height=750
floor_y=670
floor_x=0

# Game Settings
game_speed= 2
tube_frequency = 1850 # aprox 3s

# Color palette
blue= (40, 116, 178)
green= (0, 180, 0)
dark_green = (0, 130, 0)
light_green = (100, 200, 100)
brown=  (120, 64, 8)
dark_brown = (120, 64, 8)
purple= (159, 95, 159)


bird_number=3 # Número de pássaros com que o teste é realizado
false_num=0 # Número de pássaros mortos
best_score=0 # Pontuação do melhor pássaro

movimento= [
    [1, 1, 1],
    [0, 0, 0],
    [1, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 0],
    [0, 1, 1],
    [0, 1, 1],
    [1, 0, 0],
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 1],
    [0, 0, 1],
    [1, 1, 0],
    [1, 1, 1],
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]

