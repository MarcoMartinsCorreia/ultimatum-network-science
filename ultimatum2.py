import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

N = 100    # Number of players (NODES)
M = 4      # Number of edges to attach from a new node to existing nodes
G = 5000   # Number of generations (rounds)

"""
TODO:
- Implement strategy update rules (e.g., imitation, mutation)
- Make simulation for only one type of player (A, B, or C) and mixed types
- Make histogram of p and q distributions during the simulation"""
"""

Class Player:
    Each player has:
    - id: unique identifier
    - type: "A" (Empathy), "B" (Pragmatic), or "C" (Independent)
    - p: offer as proposer
    - q: acceptance threshold as responder
    - payoff: money earned in the current round
"""
class Player: # each Player is a node of the graph
    def __init__(self, node_id, player_type="C"):
        self.id = node_id
        self.type = player_type

        if self.type == "A":        # Empathy player (p = q)
            self.p = random.random()
            self.q = self.p

        elif self.type == "B":      # Pragmatic player (p = 1 - q)
            self.p = random.random()
            self.q = 1 - self.p

        elif self.type == "C":      # Independent player (p, q independent)
            self.p = random.random()
            self.q = random.random()

        self.payoff = 0  # money each player gets each round (resets every round)

    def reset_payoff(self):
        self.payoff = 0
    
    def set_strategy(self, p, q):
        """Copy or learn strategy, respecting the player's type"""
        if self.type == "A":
            self.p = p
            self.q = p
        elif self.type == "B":
            self.p = p
            self.q = 1 - p
        elif self.type == "C":
            self.p = p
            self.q = q

"""
Function run_round:
    Simulates one round of the Ultimatum Game on the given graph with the given population
"""

def run_round(graph, population):
    for player in population.values():
        player.reset_payoff()
    for i in graph.nodes():
        proposer = population[i]
        for j in graph.neighbors(i):
            responder = population[j]
            offer = proposer.p
            threshold = responder.q
            if offer >= threshold:
                proposer.payoff += (1 - offer)
                responder.payoff += offer


# -------------------------------
# Graph and population
# -------------------------------
ba = nx.barabasi_albert_graph(N, M)  # scale-free network 

# Option 1: all players of type C
# population = {node: Player(node, player_type="C") for node in ba.nodes()}

# Option 2: mix of types A, B, C
population = {}
for node in ba.nodes():
    t = random.choice(["A", "B", "C"])  # assign a random type
    population[node] = Player(node, player_type=t)

# -------------------------------
# Simulation
# -------------------------------
history = []

for gen in range(G):
    run_round(ba, population)
    if gen % 10 == 0:
        avg_p = np.mean([p.p for p in population.values()])
        avg_q = np.mean([p.q for p in population.values()])
        history.append((gen, avg_p, avg_q))
        if gen % 500 == 0:
            print(f"Generation {gen}: Avg Offer (p) = {avg_p:.3f}, Avg Threshold (q) = {avg_q:.3f}")

# -------------------------------
# Plotting results
# -------------------------------
history = np.array(history)
plt.plot(history[:, 0], history[:, 1], label='Average p (offer)')
plt.plot(history[:, 0], history[:, 2], label='Average q (threshold)')
plt.xlabel('Generation')
plt.ylabel('Value')
plt.legend()
plt.title('Evolution of Average Strategies (A, B, C players)')
plt.show()
