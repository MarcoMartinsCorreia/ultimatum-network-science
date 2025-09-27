# Ultimatum Game Network Simulation

This project implements a simulation of the Ultimatum Game on a scale-free network using the Barabási-Albert model. The simulation includes different types of players with varying strategies for offering and accepting deals.

## Description

The Ultimatum Game is a game theory experiment where two players interact:

- A proposer who offers to split a sum of money
- A responder who can either accept or reject the offer

In this implementation, players are nodes in a network and interact with their neighbors. The simulation includes three types of players:

- **Type A (Empathy)**: Players with equal offer and acceptance threshold (p = q)
- **Type B (Pragmatic)**: Players with complementary offer and acceptance threshold (p = 1 - q)
- **Type C (Independent)**: Players with independent offer and acceptance threshold values

## Requirements

To run this simulation, you need the following Python packages:

```bash
networkx      # For network creation and manipulation
matplotlib    # For plotting results
numpy         # For numerical operations
```

## Installation

1. Make sure you have Python 3.x installed

2. Install the required packages:

```bash
pip install networkx matplotlib numpy
```

## Configuration

The simulation can be configured by adjusting these parameters in `ultimatum2.py`:

- `N`: Number of players (nodes) in the network (default: 100)
- `M`: Number of edges to attach from a new node to existing nodes (default: 4)
- `G`: Number of generations/rounds (default: 5000)

## Usage

Run the simulation with:

```bash
python ultimatum2.py
```

The program will:

1. Create a Barabási-Albert scale-free network
2. Initialize players with random strategies
3. Run the specified number of generations
4. Display progress every 500 generations
5. Plot the evolution of average strategies over time

## Output

The simulation outputs:

- Console updates showing average offer (p) and threshold (q) values every 500 generations
- A plot showing the evolution of average strategies over time

## Repository Information

- **Repository Name**: ultimatum-network-science
- **Owner**: MarcoMartinsCorreia
- **Main Branch**: Main

## License

[Add your license information here]
