import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

N = 100    # Number of players (NODES)
M = 4      # Number of edges to attach from a new node to existing nodes (   
G = 5000   # Number of generations (rounds)

class Player: # each Player is a node of the graph
    def __init__(self, node_id):
        self.id = node_id
        self.p = random.random() # offer for the division of the reward
        self.q = random.random() # threshold for accepting offers
        self.payoff = 0          # money each player get each round (resets every round)

    def reset_payoff(self): # reset payoff function (called every round)
        self.payoff = 0
    
    def set_strategy(self, p, q): # called every time a Player wants to copy or learn a strategy from the opponent
        self.p = p
        self.q = q

def run_round(graph, population): # function that receives the graph and the list of players to run a round of the game
        for player in population.values(): # reset the payoff of each player
            player.reset_payoff()
        for i in graph.nodes():    # go through all nodes of the graph
            proposer = population[i]    # the player that proposes an offer
            for j in graph.neighbors(i):    # go through all neighbors of the proposer
                responder = population[j]   # the player that receives the offer
                offer = proposer.p          # the offer made by the proposer            
                threshold = responder.q     # the threshold of the responder
                if offer >= threshold:      # if the offer is accepted
                    proposer.payoff += (1 - offer)  # proposer gets the remaining part of the reward
                    responder.payoff += offer       # responder gets the offered part of the reward

                    
    # def evolve_strategies_natural_selection(graph, population):
    #     strategy_updates = []



#ws = nx.watts_strogatz_graph(30, 3, 0) # small world graph
ba = nx.barabasi_albert_graph(N, M) # scale-free network 

population = { node: Player(node) for node in ba.nodes() } # create a dictionary of players with node ids as keys
history = []    # to store the history of the average p and q values over generations

for gen in range(G):
    run_round(ba, population)
    if gen % 10 == 0:
        avg_p = np.mean([p.p for p in population.values()])
        avg_q = np.mean([p.q for p in population.values()])
        history.append((gen, avg_p, avg_q))
        if gen % 500 == 0:
            print(f"Generation {gen}: Avg Offer (p) = {avg_p:.3f}, Avg Threshold (q) = {avg_q:.3f}")
        
# Plotting the results
history = np.array(history)
plt.plot(history[:, 0], history[:, 1], label='Average p (offer)')
plt.plot(history[:, 0], history[:, 2], label='Average q (threshold)')
plt.xlabel('Generation')
plt.ylabel('Value')
plt.legend()
plt.title('Evolution of Average Strategies Over Generations')
plt.show()
