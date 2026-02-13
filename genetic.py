# Here are the functions used to implement the genetic algorithm on the neural networks

import numpy as np

rng = np.random.default_rng()

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
    pass



if __name__ == "__main__":
    dna = rng.normal(size=10)
    print(dna)
    print(mutate(dna, 0.5))