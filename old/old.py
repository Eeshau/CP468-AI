


#
# OLD VERSION !!!!!!!!
#


import heapq  # Importing heapq for potential use in distance calculations
from collections import deque  # Importing deque for BFS distance calculation

# Defining a class for nodes in the graph
class Node:
    def __init__(self, identifier):
        self.identifier = identifier  # Unique identifier for the node
        self.neighbors = []  # List to store neighboring nodes
        self.occupied = False  # Attribute to indicate whether the node is occupied by a vehicle

    def occupy(self):
        self.occupied = True  # Method to set the node as occupied

    def vacate(self):
        self.occupied = False  # Method to set the node as unoccupied



# Defining a class for the graph
class Graph:
    def __init__(self):
        self.nodes = {}  # Dictionary to store nodes indexed by their identifiers

    def add_node(self, identifier):
        node = Node(identifier)  # Creating a new node
        self.nodes[identifier] = node  # Adding the new node to the dictionary
        return node

    def add_edge(self, node1, node2):
        self.nodes[node1].neighbors.append(self.nodes[node2])  # Adding node2 as a neighbor to node1


# Function to calculate a simplistic traffic time
def get_traffic_time(node1, node2, vehicles_locations):
    traffic_time = len(vehicles_locations) * 3  # Arbitrarily scaling traffic time by the number of vehicles
    return traffic_time


# Function to get a fixed delay at intersections
def get_delay(node):
    return 10 if node in intersection_nodes else 0  # Returning a fixed delay if node is an intersection


# Function to calculate distance using BFS
def bfs_distance(node1, node2):
    visited = set()  # Set to store visited nodes
    queue = deque([(node1, 0)])  # Queue to hold nodes and their distances from node1
    while queue:
        node, dist = queue.popleft()  # Popping the front node from the queue
        if node == node2:
            return dist  # Returning the distance if node2 is found
        if node not in visited:
            visited.add(node)  # Marking the node as visited
            for neighbor in node.neighbors:
                queue.append((neighbor, dist + 1))  # Enqueuing neighbors and updating distances

# Implementing the BNART algorithm
def BNART(graph, dead_end_nodes, vehicles_locations, destination_node, traversed_nodes):
    n = vehicles_locations[-1]  # Assuming the vehicle is at the last location in the list
    neighbors = n.neighbors  # Getting neighbors of the current node
    best = float('inf')  # Initializing the best value to infinity
    b = None  # Initializing the best neighbor to None

    for neighbor in neighbors:
        if neighbor not in traversed_nodes and neighbor not in dead_end_nodes:  # Ensuring neighbor is not in dead-end or traversed list
            traffic_time = get_traffic_time(neighbor, n, vehicles_locations)  # Calculating traffic time
            delay = get_delay(neighbor)  # Getting delay at neighbor node
            distance = bfs_distance(neighbor, destination_node)  # Calculating distance to destination
            norm_value = (traffic_time + delay + distance)  # Summing traffic time, delay, and distance
            if norm_value < best:  # Checking if this is a better neighbor
                best = norm_value
                b = neighbor

    vehicles_locations.append(b)  # Updating vehicle locations with the selected neighbor
    traversed_nodes.append(b)  # Updating traversed nodes with the selected neighbor
    return b  # Returning the selected neighbor

# Example Usage:
graph = Graph()
intersection_nodes = set()
for i in range(10):
    node = graph.add_node(i)
    if i % 2 == 0:  # Assuming even nodes are intersections for simplicity
        intersection_nodes.add(node)
for i in range(9):
    graph.add_edge(i, i + 1)  # Adding edges to the graph

dead_end_nodes = []  # Assume no dead-end nodes for simplicity
vehicles_locations = [graph.nodes[0]]  # Assume the vehicle starts at node 0
destination_node = graph.nodes[9]  # Assume the destination is node 9
traversed_nodes = []  # List to store nodes traversed by the vehicle

best_neighbor = BNART(graph, dead_end_nodes, vehicles_locations, destination_node, traversed_nodes)  # Calling BNART
print(f'Best neighbor node: {best_neighbor.identifier}')  # Printing the identifier of the best neighbor node





def test_code():
    graph = Graph()  # Creating a new Graph instance

    # Adding nodes to the graph from 0 to 24 to represent a 5x5 grid
    for i in range(25):
        graph.add_node(i)

    # Adding edges to the graph based on the image
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (5, 6), (6, 7), (7, 8), (8, 9),
        (10, 11), (11, 12), (12, 13), (13, 14),
        (15, 16), (16, 17), (17, 18), (18, 19),
        (20, 21), (21, 22), (22, 23), (23, 24),
        (0, 5), (5, 10), (10, 15), (15, 20),
        (1, 6), (6, 11), (11, 16), (16, 21),
        (2, 7), (7, 12), (12, 17), (17, 22),
        (3, 8), (8, 13), (13, 18), (18, 23),
        (4, 9), (9, 14), (14, 19), (19, 24)
    ]
    for edge in edges:
        graph.add_edge(*edge)  # Adding edges to the graph

    intersection_nodes = {graph.nodes[i] for i in range(25) if i % 5 != 4 and i < 20}  # Assuming nodes 0-19 are intersections for simplicity
    dead_end_nodes = []  # Assume no dead-end nodes for simplicity
    vehicles_locations = [graph.nodes[0]]  # Assume the vehicle starts at node 0
    destination_node = graph.nodes[24]  # Assume the destination is node 24
    traversed_nodes = []  # List to store nodes traversed by the vehicle

    best_neighbor = BNART(graph, dead_end_nodes, vehicles_locations, destination_node, traversed_nodes)  # Calling BNART
    print(f'Best neighbor node: {best_neighbor.identifier}')  # Printing the identifier of the best neighbor node

# Call the test function to run the test
test_code()