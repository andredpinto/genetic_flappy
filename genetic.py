# Here are the functions used to implement the genetic algorithm on the neural networks

import numpy as np

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
    # Takes a list of 'parent' birds and creates a list of birds to use for the next generation
    offsp_list = [bird for bird in bird_list]   # Add parents to next generation

    for i in range(n_offspring):
        parents = rng.integers(low=0, high=len(bird_list), size=2)
        offsp_list.append(mutate(crossover(bird_list[parents[0]], bird_list[parents[1]])))

    return offsp_list


if __name__ == "__main__":
    dna1 = rng.normal(size=10)
    print("dna1 = ", dna1)
    dna2 = rng.normal(size=10)
    print("dna2 = ", dna2)
    print('=========================')

    print(generate([dna1, dna2], 6))