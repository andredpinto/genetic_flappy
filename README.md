# Genetic Flappy Bird 🐦🧠

An elegant, fully customizable clone of the classic Flappy Bird game built in Python using **Pygame**, featuring an autonomous AI training mode driven by a **Genetic Algorithm** and **Neural Networks** implemented entirely from scratch with **NumPy**.

---

## 📖 Project Overview

This repository demonstrates the power of evolutionary algorithms and neural networks by applying them to a real-time game environment. It includes two primary modes of operation:
1. **Human Playable Mode (`game.py`)**: Play the classic Flappy Bird game manually.
2. **Autonomous AI Mode (`neural_game.py`)**: Watch a population of AI agents (birds) simultaneously attempt to navigate obstacles. Through natural selection, mutation, and crossover, the population evolves across generations to achieve superhuman performance.

---

## 🧠 AI & Genetic Algorithm Architecture

Instead of relying on heavy machine learning libraries like TensorFlow or PyTorch, the neural network and genetic operators are built from the ground up using vectorized **NumPy** operations for maximum efficiency and readability.

### Neural Network (`neural_network.py`)
Each bird is controlled by a simple Multi-Layer Perceptron (MLP) acting as a binary classifier:
* **Input Layer (4 Neurons)**: Receives real-time environmental sensors normalized between 0 and 1:
  1. `tube_vert_dist`: Vertical distance from the bird to the bottom opening of the upcoming tube.
  2. `tube_horiz_dist`: Horizontal distance from the bird to the upcoming tube.
  3. `floor_dist`: Vertical distance from the bird to the ground.
  4. `norm_speed`: Current vertical velocity of the bird.
* **Hidden Layer (5 Neurons)**: Uses the **ReLU** (Rectified Linear Unit) activation function to process non-linear relationships.
* **Output Layer (1 Neuron)**: Uses the **Sigmoid** activation function to output a jump probability. If the output exceeds `0.5`, the bird jumps.

### Genetic Algorithm (`genetic.py`)
Evolution occurs across distinct generations of 100 birds (`generation_size`):
* **Fitness Metric**: Measured by the exact number of frames a bird remains alive. Passing tubes grants auxiliary points.
* **Elitism**: The top **10 best-performing birds** (`elite_number`) automatically pass their unaltered DNA (weights and biases) directly to the next generation to prevent regression.
* **Crossover**: The remaining population is generated via **Uniform Crossover**, combining random binary masks of the DNA from two parent networks selected from the elite pool.
* **Mutation**: Offspring undergo random **Gaussian Mutation** at a rate of `10%` (`rate=0.1`), introducing slight weight adjustments to foster exploration of new strategies.
* **Persistence**: At the end of each generation, the elite neural network weights are automatically saved to `apex.json`. Upon restarting, the game loads these stored weights, allowing training to resume seamlessly.

---

## 🗂️ Repository Structure

* **`game.py`**: Standard human-playable Flappy Bird clone.
* **`neural_game.py`**: The main execution script for running the AI evolution simulation.
* **`assets.py`**: Defines standard game entities (`Bird`, `smartBird`, `Tube`, and floor patterns) along with sensor processing logic.
* **`neural_network.py`**: Core MLP neural network implementation featuring custom `Layer` classes, forward passes, and DNA serialization.
* **`genetic.py`**: Functions governing selection, crossover, mutation, and next-generation population synthesis.
* **`globals.py`**: Hyperparameters, color palettes, screen dimensions, and game physics constants.
* **`apex.json`**: Persistent JSON storage containing the best-performing neural networks' parameters.

---

## ⚙️ Setup & Installation Guide

### Requirements
As specified in the original repository configuration:
* **Python**: `3.13.9`
* **Pygame**: `2.6.1`
* **NumPy**

### Installation Steps

1. **Clone the Repository**:
   [TRIPLE-BACKTICK]bash
   git clone https://github.com/andredpinto/genetic_flappy.git
   cd genetic_flappy
   [TRIPLE-BACKTICK]

2. **Create a Virtual Environment (Optional but Recommended)**:
   [TRIPLE-BACKTICK]bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   [TRIPLE-BACKTICK]

3. **Install Dependencies**:
   Install the necessary packages using the provided `requirements.txt`:
   [TRIPLE-BACKTICK]bash
   pip install -r requirements.txt
   [TRIPLE-BACKTICK]

---

## 🚀 Usage Instructions

### Playing as a Human
Run the standard game mode:
[TRIPLE-BACKTICK]bash
python game.py
[TRIPLE-BACKTICK]
* **Start / Restart**: Press **`S`** or **`R`**.
* **Jump**: Press the **`SPACEBAR`**.

### Running the AI Evolution Simulation
Launch the genetic algorithm training dashboard:
[TRIPLE-BACKTICK]bash
python neural_game.py
[TRIPLE-BACKTICK]
* **Start Simulation**: Press **`S`** to initialize the generation.
* **Manual Reset**: Press **`R`** to instantly force a reset and proceed to the next generation.
* **Watch Evolution**: Watch 100 agents play concurrently. As agents collide with obstacles, they are eliminated. Once all 100 agents fail, the system prints the generation count, saves the top performers to `apex.json`, and spawns an evolved batch.

---

## 🛠️ Customization & Hyperparameters

You can easily tweak the AI parameters and game mechanics by editing `globals.py`:
* `game_speed`: Adjusts the horizontal scroll speed.
* `tube_frequency`: Milliseconds between spawning new obstacles.
* `generation_size`: Total number of birds per generation (default: `100`).
* `elite_number`: Number of top birds preserved per generation (default: `10`).

---

## 📜 License

This project is licensed under the **MIT License**. **MIT License**.
