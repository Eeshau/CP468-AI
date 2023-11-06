# ----------------------
# CP468 AI ASSIGNMENT 1 QUESTION 4 - Modified to use Q-learning
# ----------------------

import numpy as np

class Edge:
    def __init__(self):
        self.vehicles = 0  # Initialize the count of vehicles on this edge to zero.

class Node:
    def __init__(self, id, is_intersection):
        self.id = id  # Unique identifier for this node.
        self.is_intersection = is_intersection  # Flag to determine if this node is an intersection.
        self.edges = {}  # Edges associated with this node.

    def add_edge(self, end):
        self.edges[end] = Edge()  # Add an edge to a given end node.

class Vehicle:
    def __init__(self, start, end):
        self.current_node = start  # Current node of the vehicle.
        self.destination = end  # Destination node of the vehicle.

class Graph:
    def __init__(self):
        self.nodes = {}  # All nodes in the graph.

    def add_node(self, id, is_intersection):
        self.nodes[id] = Node(id, is_intersection)  # Add a node to the graph.

    def add_edge(self, start, end):
        if start in self.nodes and end in self.nodes:
            self.nodes[start].add_edge(end)  # Add an edge between nodes.

# Q-learning specific functions

def initialize_q_table(graph, vehicles):
    # Initialize Q-table with zeros
    # States are represented by current node and destination, actions are possible next nodes
    q_table = {}
    for vehicle in vehicles:
        for node in graph.nodes.values():
            q_table[(vehicle.current_node, vehicle.destination, node.id)] = {next_node: 0 for next_node in node.edges}
    return q_table

def choose_next_node(q_table, current_node, destination):
    # Choose the best action from Q-table with a random factor for exploration
    current_actions = q_table[(current_node, destination, current_node)]
    if np.random.uniform(0, 1) < epsilon:  # Exploration
        next_node = np.random.choice(list(current_actions.keys()))
    else:  # Exploitation
        next_node = max(current_actions, key=current_actions.get)
    return next_node

def update_q_table(q_table, graph, vehicle, next_node, alpha, gamma):
    # Update Q-table based on the formula
    current_state = (vehicle.current_node, vehicle.destination, vehicle.current_node)
    next_state = (next_node, vehicle.destination, next_node)
    reward = -travel_time(graph, vehicle.current_node, next_node)  # Using negative of travel time as reward
    # Q-learning update formula
    current_q = q_table[current_state][next_node]
    max_future_q = max(q_table[next_state].values()) if next_state in q_table else 0
    q_table[current_state][next_node] = (1 - alpha) * current_q + alpha * (reward + gamma * max_future_q)

# Existing functions with some modifications

def travel_time(graph, start, end):
    base_time = 1
    edge_delay = graph.nodes[start].edges[end].vehicles * 0.01
    node_delay = 3 if graph.nodes[end].is_intersection else 0
    return base_time + edge_delay + node_delay

def q_learning(graph, vehicles, q_table, alpha, gamma, epsilon):
    # Initialize variables
    total_time = 0
    for vehicle in vehicles:
        while vehicle.current_node != vehicle.destination:
            next_node = choose_next_node(q_table, vehicle.current_node, vehicle.destination)
            update_q_table(q_table, graph, vehicle, next_node, alpha, gamma)
            vehicle.current_node = next_node  # Move to the next node
            total_time += travel_time(graph, vehicle.current_node, next_node)  # Update the total time
    return total_time

# Main function to run the algorithm

def main():
    graph = Graph()
    for i in range(1, 7):
        graph.add_node(i, i in [1, 3, 6])
    graph.add_edge(1, 2)
    # ... Add remaining edges ...

    vehicles = [Vehicle(1, 5)]
    q_table = initialize_q_table(graph, vehicles)

    # Parameters for Q-learning
    alpha = 0.1  # Learning rate
    gamma = 0.6  # Discount factor
    epsilon = 0.1  # Exploration rate

    total_time = q_learning(graph, vehicles, q_table, alpha, gamma, epsilon)
    print(f"Total time taken for all vehicles: {total_time}")

# Run the main function
main()
