# Since this is a conceptual translation of BNART into a Q-learning context,
# we will define a simplified environment to test the algorithm.
# We will create a linear graph with 5 nodes and 2 vehicles, and run the simulation.

class Edge:
    def __init__(self):
        self.vehicles = 0
        self.q_value = 0

    def enter(self):
        self.vehicles += 1

    def exit(self):
        if self.vehicles > 0:
            self.vehicles -= 1

class Node:
    def __init__(self, id, is_intersection):
        self.id = id
        self.is_intersection = is_intersection
        self.edges = {}

    def add_edge(self, end):
        self.edges[end] = Edge()

class Vehicle:
    def __init__(self, start, end):
        self.current = start
        self.destination = end
        self.total_time = 0
        self.path = [start]

    def move_to(self, node_id):
        self.path.append(node_id)
        self.current = node_id

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_edge(self, start, end):
        if start in self.nodes and end in self.nodes:
            self.nodes[start].add_edge(end)

# Constants from BNART
TRoad = 1  # Base time to travel an edge
TDelay = 3  # Additional delay time at intersections
C_percent = 0.01  # Congestion factor per vehicle

def calculate_congestion_delay(edge):
    return C_percent * edge.vehicles

def update_q_value(graph, start, end, reward, alpha=0.1, gamma=0.9):
    current_edge = graph.nodes[start].edges[end]
    max_q = max(edge.q_value for edge in graph.nodes[end].edges.values())
    sample = reward + gamma * max_q
    current_edge.q_value += alpha * (sample - current_edge.q_value)

def get_next_node(graph, vehicle):
    current_node = graph.nodes[vehicle.current]
    next_node = max(current_node.edges, key=lambda x: current_node.edges[x].q_value)
    return next_node

def simulate(graph, vehicle, epochs=100):
    for _ in range(epochs):
        while vehicle.current != vehicle.destination:
            next_node = get_next_node(graph, vehicle)
            current_edge = graph.nodes[vehicle.current].edges[next_node]

            current_edge.enter()
            congestion_delay = calculate_congestion_delay(current_edge)
            travel_time = TRoad + congestion_delay
            if graph.nodes[next_node].is_intersection:
                travel_time += TDelay

            vehicle.total_time += travel_time
            vehicle.move_to(next_node)

            reward = -travel_time  # We want to minimize travel time
            update_q_value(graph, vehicle.current, next_node, reward)

            current_edge.exit()

# Initialize graph with nodes
graph = Graph()
for i in range(1, 6):
    graph.add_node(Node(i, i == 1 or i == 5))

# Add edges between nodes
for i in range(1, 5):
    graph.add_edge(i, i + 1)

# Initialize vehicles
vehicles = [Vehicle(1, 5), Vehicle(2, 5)]

# Simulate traffic movement for each vehicle
for vehicle in vehicles:
    simulate(graph, vehicle)
    print(f"Vehicle from {vehicle.path[0]} to {vehicle.path[-1]}: Total time {vehicle.total_time}, Path taken: {vehicle.path}")

