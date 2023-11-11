import numpy as np
import itertools

# Constants from BNART
TRoad = 1  # Time taken to traverse a segment without congestion
TDelay = 3  # Time delay at intersections
C_percent = 0.01  # Congestion coefficient

class Node:
    def __init__(self, id, is_intersection):
        self.id = id
        self.is_intersection = is_intersection
        self.edges = {}

    def add_edge(self, end):
        if end not in self.edges:
            self.edges[end] = {'vehicles': 0, 'q_value': 0}

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_edge(self, start, end):
        if start in self.nodes and end in self.nodes:
            self.nodes[start].add_edge(end)
            # Since this is a directed graph, we do not automatically add the reverse edge

class Vehicle:
    def __init__(self, start, end):
        self.current = start
        self.destination = end
        self.total_time = 0
        self.path = []

    def move_to(self, node_id):
        self.path.append(node_id)
        self.current = node_id

def calculate_congestion_delay(vehicles):
    return C_percent * vehicles

def update_q_value(graph, start, end, reward, alpha=0.1, gamma=0.9):
    max_q = max(graph.nodes[end].edges[e]['q_value'] for e in graph.nodes[end].edges)
    sample = reward + gamma * max_q
    graph.nodes[start].edges[end]['q_value'] += alpha * (sample - graph.nodes[start].edges[end]['q_value'])

def get_next_node(graph, vehicle):
    current_node = graph.nodes[vehicle.current]
    possible_moves = list(current_node.edges.keys())
    next_node = max(possible_moves, key=lambda x: current_node.edges[x]['q_value'])
    return next_node

def simulate(graph, vehicle, epochs=1000):
    for _ in range(epochs):
        while vehicle.current != vehicle.destination:
            next_node = get_next_node(graph, vehicle)
            current_edge = graph.nodes[vehicle.current].edges[next_node]
            congestion_delay = calculate_congestion_delay(current_edge['vehicles'])
            travel_time = TRoad + congestion_delay
            if graph.nodes[next_node].is_intersection:
                travel_time += TDelay

            vehicle.total_time += travel_time
            vehicle.move_to(next_node)

            # Simulate other vehicles for congestion
            current_edge['vehicles'] += 1

            reward = -travel_time
            update_q_value(graph, vehicle.current, next_node, reward)

            current_edge['vehicles'] -= 1

        vehicle.move_to(vehicle.destination)

# Initialize Graph with Nodes and Edges as per BNART setup
graph = Graph()
nodes = [Node(i, i%5==0) for i in range(1, 21)]  # Example nodes, with every 5th node being an intersection
for node in nodes:
    graph.add_node(node)

# Add directed edges between nodes
edges = [(i, i+1) for i in range(1, 20)]  # Example edges, creating a path from node 1 to node 20
for start, end in edges:
    graph.add_edge(start, end)

# Initialize vehicles
vehicles = [Vehicle(1, 20), Vehicle(5, 15)]  # Example vehicles

# Simulate traffic movement for each vehicle
for vehicle in vehicles:
    simulate(graph, vehicle)
    print(f"Vehicle from {vehicle.path[0]} to {vehicle.path[-1]}: Total time {vehicle.total_time}, Path taken: {vehicle.path}")
