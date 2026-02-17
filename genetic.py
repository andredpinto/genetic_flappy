# Here are the functions used to implement the genetic algorithm on the neural networks

import numpy as np

from assets import smartBird
from globals import *

rng = np.random.default_rng()   # Use a seed for reproducible results

def mutate(dna : np.ndarray, rate=0.1):
    n_indices = round(dna.size*rate)
    indices = rng.integers(low=0, high=dna.size, size=n_indices)
    # This method of generating numbers may result in duplicated indices
    # I chose to consider this a feature (wink wink), where a value may be mutated more than one time
    # For generating non-repeated values, use np.random.choice, with replace=False 
    # (this is probably deprecated, but i dont want to search for another method)

    dna[indices] += rng.normal(size=n_indices)
    # You could use a for loop to iterate over the indices, but this (fancy) way
    # makes use of numpy's vectorized operations

    return dna

def crossover(a : np.ndarray, b : np.ndarray):
    # This is only a possible implementation of a crossover function (Uniform Crossover)
    # For more options, look into Single-Point Crossover and Arithmetic Crossover

    # Gets two neural network's DNA and returns one that is a (random) combination of both
    assert a.size == b.size

    mask = rng.random(a.size) > 0.5
    # This is an array of booleans
    # rng.random creates an array of n values in the interval (0,1(

    offspring = np.where(mask, a, b)
    # I think you can figure out what np.where does

    return offspring


def generate(bird_list : list, n_offspring : int) -> list:
    # Takes a list of 'parent' birds (NOT actually birds, but their DNA) and creates a list of birds to use for the next generation
    offsp_list = []

    for i in range(n_offspring):
        parents = rng.integers(low=0, high=len(bird_list), size=2)
        offsp_list.append(mutate(crossover(bird_list[parents[0]], bird_list[parents[1]])))

    return offsp_list


def get_best(bird_scores: dict)->list:
     # Returns best birds (number depends on elite_number)
        leaderboard = sorted(bird_scores.items(), key=lambda x: x[1], reverse=True) # Sort birds by score (descending)

        return [b[0] for b in leaderboard[:elite_number]]   # Get best birds


def create_generation(bird_scores, gen_size, screen, bird_stamp)->tuple:
    # Receives bird scores dictionary {smartBird : score} and returns list of birds in new generation + bird stamp number
    if isinstance(bird_scores, dict):
        new_gen = get_best(bird_scores) # Add parents (elite) to next generation

    elif isinstance(bird_scores, list):
        new_gen = bird_scores

    else:
        raise ValueError("bird_scores must be either a list or a dictionary")

    elite = [b.getDNA() for b in new_gen]

    for dna in generate(elite, gen_size-elite_number):
            new_bird = smartBird(bird_x, 300, screen, bird_stamp, input_number)
            bird_stamp += 1
            new_bird.setDNA(dna)
            new_gen.append(new_bird)

    return new_gen, bird_stamp



if __name__ == "__main__":
    dna1 = rng.normal(size=10)
    print("dna1 = ", dna1)
    dna2 = rng.normal(size=10)
    print("dna2 = ", dna2)
    print('=========================')

    print(generate([dna1, dna2], 6))