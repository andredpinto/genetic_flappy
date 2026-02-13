import numpy as np

rng = np.random.default_rng()   # Use a seed for reproducible results

# Activation functions and their vectorized versions

def ReLU(x):
    return np.maximum(x,0)

def step(x):
    return (x>=0).astype(float)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Classes

# The activation function passed to the Layer class must be vectorized,
# to allow operations on entire arrays (behaviour similar to map() function)
class Layer:
    def __init__(self, input_size, size, activation):
        # The initial values for the matrixes are random
        self.weights = rng.normal(size=(size, input_size))
        self.biases = rng.normal(size=(size,1))
        self.activation = activation

    def forwardPass(self, input : np.ndarray) -> np.ndarray:
        # Receives outputs from neurons in previous layer (input) and outputs the values
        # from the neurons in its layer (as N x 1 matrixes (numpy arrays), where N is the number of neurons)
        return self.activation(self.weights @ input + self.biases)
        # @ is the same as np.dot(), matrix multiplication
    
    def show(self):
        print(self.weights)
        print(self.biases)


# This is an implementation of a simple neural network for our specific use case
# with N inputs and 1 output, with a single hidden layer with variable size
# (Basically a classifier with N inputs)
class NeuralNetwork:
    def __init__(self, input_size, hidden_layer_size=5):
        self.hidden_layer_size = hidden_layer_size
        self.hidden_layer = Layer(input_size, hidden_layer_size, ReLU)
        self.output_layer = Layer(hidden_layer_size, 1, sigmoid)

    def think(self, input : np.ndarray):
        # Outputs a number between 0 and 1, based on the input (sigmoid activation function)
        return self.output_layer.forwardPass(self.hidden_layer.forwardPass(input))
    
    def getDNA(self):
        # returns a list of all of the weight values for the network
        return np.concatenate([
            self.hidden_layer.weights.flatten(),
            self.hidden_layer.biases.flatten(),
            self.output_layer.weights.flatten(),
            self.output_layer.biases.flatten()
        ]
        )
    
    def setDNA(self, data : np.ndarray):
        # inverse of getDNA: receives a list with values and associates them with the weights and biases of the network
        hl = self.hidden_layer
        ol = self.output_layer

        hl.weights = data[:hl.weights.size].reshape(hl.weights.shape)
        i = hl.weights.size
        hl.biases = data[i : i+hl.biases.size].reshape(hl.biases.shape)
        i += hl.biases.size
        ol.weights = data[i : i+ol.weights.size].reshape(ol.weights.shape)
        i += ol.weights.size
        ol.biases = data[i :].reshape(ol.biases.shape)

        # This implementation is fine for our use-case, with only one hidden layer.
        # However, if you wish to upgrade this network implementation, with more hidden layers,
        # you should add a "layer_list" attribute to the Network object
        # This method should then be refactored to use a cycle instead of manually slicing the input array


# Debugging
if __name__ == "__main__":
    myNetwork = NeuralNetwork(3)
    print(myNetwork.getDNA())