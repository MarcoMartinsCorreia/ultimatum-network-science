# Ultimatum Game Evolution on a Scale-Free Network

This project simulates the evolution of strategies in the **Ultimatum Game** played on a **Barabási–Albert (scale-free) network**. Players interact with their neighbors, earn payoffs, and evolve their strategies according to replicator dynamics.

---

## Table of Contents

- [Overview](#overview)  
- [Player Types](#player-types)  
- [Simulation](#simulation)  
- [Dependencies](#dependencies)  
- [Usage](#usage)  
- [Results](#results)  

---

## Overview

The simulation models `N` players as nodes in a network, connected through `M` edges per new node (Barabási–Albert model). Each player participates in repeated rounds of the Ultimatum Game with neighbors and updates their strategy based on payoffs.

Key parameters:

- `N`: Number of players (nodes)  
- `M`: Number of edges for new nodes in the network  
- `G`: Number of generations (rounds)  
- `MUT_RATE`: Mutation probability (optional)  

---

## Player Types

Each player has a unique strategy consisting of:

- `p`: Offer as a proposer  
- `q`: Acceptance threshold as a responder  

Three player types are supported:

1. **Type A – Empathy**: `p = q`  
2. **Type B – Pragmatic**: `p = 1 - q`  
3. **Type C – Independent**: `p` and `q` are independent  

Players earn a payoff during each round depending on whether their offers are accepted.

---

## Simulation

The simulation consists of:

1. **Network Creation**: Generates a scale-free network using `networkx`.  
2. **Gameplay**: For each generation, players interact with their neighbors, playing the Ultimatum Game.  
3. **Strategy Evolution**: Every 2 generations, strategies are updated using **replicator dynamics**: a player may adopt the strategy of a more successful neighbor.  
4. **Data Collection**: Tracks the average offer (`p`) and acceptance threshold (`q`) every 10 generations.  
5. **Visualization**: Shows histograms of strategy distributions and plots the evolution of average strategies over generations.

---

## Dependencies

- Python 3.8+  
- [NetworkX](https://networkx.org/)  
- [Matplotlib](https://matplotlib.org/)  
- [NumPy](https://numpy.org/)  

Install dependencies via pip:

```bash
pip install networkx matplotlib numpy
