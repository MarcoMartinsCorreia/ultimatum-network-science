import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

N = 100    # Number of players (NODES)
M = 4      # Number of edges to attach from a new node to existing nodes
G = 50000   # Number of generations (rounds)
MUT_RATE = 0.00  # mutation probability

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
            self.q = random.random()
            self.p = self.q

        elif self.type == "B":      # Pragmatic player (p = 1 - q)
            self.q = random.random()
            self.p = 1 - self.q

        elif self.type == "C":      # Independent player (p, q independent)
            self.p = random.random()
            self.q = random.random()

        self.payoff = 0  # money each player gets each round (resets every round)

    def reset_payoff(self):
        self.payoff = 0
    
    def set_strategy(self, p, q):
        """Copy or learn strategy, respecting the player's type"""
        if self.type == "A":
            self.q = q
            self.p = q
        elif self.type == "B":
            self.q = q
            self.p = 1 - q
        elif self.type == "C":
            self.p = p
            self.q = q

    def mutate(self, rate=MUT_RATE):
        """Small random mutation in strategy"""
        if random.random() < rate:
            if self.type == "C":
                self.p = min(max(self.p + np.random.normal(0, 0.05), 0), 1)
                self.q = min(max(self.q + np.random.normal(0, 0.05), 0), 1)
            elif self.type == "A":
                self.q = min(max(self.q + np.random.normal(0, 0.05), 0), 1)
                self.p = self.q
            elif self.type == "B":
                self.q = min(max(self.q + np.random.normal(0, 0.05), 0), 1)
                self.p = 1 - self.q


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


"""
Function evolve_strategies_replicator:
    Implements the replicator dynamics update rule as in Sinatra et al. (2009).
"""
def evolve_strategies_replicator(graph, population):
    new_strategies = {}

    for i in graph.nodes(): 
        player_i = population[i]  
        neighbors = list(graph.neighbors(i))
        if not neighbors:
            continue

        j = random.choice(neighbors)
        player_j = population[j]

        Pi = player_i.payoff
        Pj = player_j.payoff
        ki = graph.degree[i]
        kj = graph.degree[j]

        if Pj > Pi:
            prob = (Pj - Pi) / (2 * max(ki, kj))
            if random.random() < prob:
                new_strategies[i] = (player_j.p, player_j.q)

    for i, (p, q) in new_strategies.items():
        population[i].set_strategy(p, q)
        population[i].mutate()  # <-- mutation applied after copying


# -------------------------------
# Graph and population
# -------------------------------
ba = nx.barabasi_albert_graph(N, M)  # scale-free network 

# Option 1: all players of type C
population = {node: Player(node, player_type="B") for node in ba.nodes()}

# -------------------------------
# Simulation
# -------------------------------
history = []

for gen in range(G):
    run_round(ba, population)

    # Only evolve every 2 generations
    if gen % 25 == 0 and gen > 0:
        evolve_strategies_replicator(ba, population)

    if gen % 10 == 0:
        avg_p = np.mean([p.p for p in population.values()])
        avg_q = np.mean([p.q for p in population.values()])
        history.append((gen, avg_p, avg_q))

        if gen % 10000 == 0:
            print(f"Generation {gen}: Avg Offer (p) = {avg_p:.3f}, Avg Threshold (q) = {avg_q:.3f}")

            # --- Histogram of p and q distributions ---
            ps = [pl.p for pl in population.values()]
            qs = [pl.q for pl in population.values()]
            plt.hist(ps, bins=20, alpha=0.5, label="Offers (p)")
            plt.hist(qs, bins=20, alpha=0.5, label="Thresholds (q)")
            plt.xlabel("Value")
            plt.ylabel("Frequency")
            plt.legend()
            plt.title(f"Strategy Distributions at Generation {gen}")
            plt.show()


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
