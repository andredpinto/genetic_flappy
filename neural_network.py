import numpy as np

# Activation functions and their vectorized versions

def ReLU(x):
    return max(0,x)

vect_ReLU = np.vectorize(ReLU)

def step(x):
    return 1 if x>=0 else 0

vect_step = np.vectorize(step)


# Classes

# The activation function passed to the Layer class must be vectorized,
# to allow operations on entire arrays (behaviour similar to map() function)
class Layer:
    def __init__(self, input_size, size, activation):
        # The initial values for the matrixes are random
        self.weights = np.random.randint(0, 10, size=(size, input_size))
        self.biases = np.random.randint(-10, 10, size=(size,1))
        self.activation = activation

    def forwardPass(self, input : np.ndarray) -> np.ndarray:
        # Receives outputs from neurons in previous layer (input) and outputs the values
        # from the neurons in its layer (as N x 1 matrixes (numpy arrays), where N is the number of neurons)
        return self.activation(np.add(np.dot(self.weights, input), self.biases))
    
    def show(self):
        print(self.weights)
        print(self.biases)


# This is an implementation of a simple neural network for our specific use case
# with N inputs and 1 binary output, with a single hidden layer with variable size
class NeuralNetwork:
    def __init__(self, input_size, hidden_layer_size):
        self.hidden_layer_size = hidden_layer_size
        self.hidden_layer = Layer(input_size, hidden_layer_size, vect_ReLU)
        self.output_layer = Layer(hidden_layer_size, 1, vect_step)

    def think(self, input : np.ndarray):
        # Outputs 0 or 1 (jump or not jump) based on the input
        # TODO
        pass


# Debugging
if __name__ == "__main__":
    myLayer = Layer(3, 5, vect_ReLU)
    myLayer.show()
    print(myLayer.forwardPass(np.array([[30], [10], [4]])))