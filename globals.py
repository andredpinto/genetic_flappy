# Global 
game_active= False
is_game_over= False
false_num=0 # Número de pássaros mortos
best_score=0 # Pontuação do melhor pássaro

# Screen settings
width=750
height=750
floor_y=670
floor_x=0
bird_x = 300

# Game Settings
game_speed= 2
tube_frequency = 1850   # milliseconds

# Color palette
blue= (40, 116, 178)
green= (0, 180, 0)
dark_green = (0, 130, 0)
light_green = (100, 200, 100)
brown=  (120, 64, 8)
dark_brown = (120, 64, 8)
purple= (159, 95, 159)

# Genetic algorithm and neural network options
input_number = 4    # Number of inputs for neural network
generation_size = 100
elite_number = 10    # Birds that pass to the next generation
assert elite_number < generation_size