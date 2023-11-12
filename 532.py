# Finishing the main function and testing the Q-learning traffic control system.

# Necessary imports
import numpy as np
import random

# Defining classes
class Node:
    def __init__(self, node_id, is_intersection):
        self.id = node_id
        self.is_intersection = is_intersection
        self.edges = {}

    def add_edge(self, destination_node, edge):
        self.edges[destination_node] = edge

class Edge:
    def __init__(self):
        self.vehicles = 0
        self.congestion_delay = 0

    def enter(self):
        self.vehicles += 1
        self.calculate_congestion_delay()

    def exit(self):
        self.vehicles = max(0, self.vehicles - 1)
        self.calculate_congestion_delay()

    def calculate_congestion_delay(self):
        self.congestion_delay = 0.01 * self.vehicles

class Vehicle:
    def __init__(self, vehicle_id, start_node, end_node):
        self.id = vehicle_id
        self.current_node = start_node
        self.destination = end_node
        self.time = 0

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node_id, is_intersection):
        self.nodes[node_id] = Node(node_id, is_intersection)

    def add_edge(self, start_node, end_node):
        if start_node in self.nodes and end_node in self.nodes:
            self.nodes[start_node].add_edge(end_node, Edge())
            self.nodes[end_node].add_edge(start_node, Edge())  # Assuming bidirectional travel

# Helper functions for Q-learning
def calculate_travel_time(graph, start_node, end_node, vehicle_count):
    base_time = 1 if not graph.nodes[start_node].is_intersection else 3
    congestion_delay = 0.01 * vehicle_count
    return base_time + congestion_delay

def get_possible_actions(graph, current_node):
    return list(graph.nodes[current_node].edges.keys())

def update_q_table(graph, vehicle, current_state, q_table, alpha, gamma):
    possible_actions = get_possible_actions(graph, vehicle.current_node)
    next_node = random.choice(possible_actions)
    reward = -calculate_travel_time(graph, vehicle.current_node, next_node, graph.nodes[vehicle.current_node].edges[next_node].vehicles)
    old_value = q_table.get((current_state, next_node), 0)
    future_rewards = [q_table.get((next_node, future_action), 0) for future_action in possible_actions]
    next_max = max(future_rewards) if future_rewards else 0
    new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
    q_table[(current_state, next_node)] = new_value
    return new_value

def find_best_path(graph, start_node, destination, q_table):
    path = [start_node]
    while start_node != destination:
        next_action = max(get_possible_actions(graph, start_node), key=lambda x: q_table.get((start_node, x), 0))
        path.append(next_action)
        start_node = next_action
    return path

def main():
    alpha = 0.1  # Learning rate
    gamma = 0.6  # Discount rate
    iterations = 10000  # Number of iterations for the Q-learning algorithm

    # Initialize the graph
    graph = Graph()
    for i in range(1, 7):
        graph.add_node(i, i in [1, 3, 6])
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (3, 5)]
    for edge in edges:
        graph.add_edge(*edge)

    # Initialize vehicles
    vehicles = [Vehicle(0, 1, 5), Vehicle(1, 5, 1), Vehicle(2, 3, 5)]

    # Initialize Q-table
    q_table = {}

    # Run Q-learning
    for _ in range(iterations):
        for vehicle in vehicles:
            if vehicle.current_node != vehicle.destination:
                update_q_table(graph, vehicle, vehicle.current_node, q_table, alpha, gamma)

    # Output results
    total_time = 0
    for vehicle in vehicles:
        vehicle_path = find_best_path(graph, vehicle.current_node, vehicle.destination, q_table)
        print(f"Vehicle {vehicle.id} has reached its destination node {vehicle.destination} in time {vehicle.time} s")
        total_time += vehicle.time

    print(f"Total time taken for all vehicles: {total_time} s")

# Run the main function to test the Q-learning traffic control system
main()
