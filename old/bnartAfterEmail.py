class Edge:
    def __init__(self):
        self.vehicles = 0  # Initially, there are no vehicles on the edge

    def enter(self):
        self.vehicles += 1  # Increment the number of vehicles on the edge

    def exit(self):
        self.vehicles -= 1  # Decrement the number of vehicles on the edge
        if self.vehicles < 0:
            self.vehicles = 0  # Ensure vehicles count doesn't go below zero

class Node:
    def __init__(self, id, is_intersection):
        self.id = id
        self.is_intersection = is_intersection
        self.edges = {}  # Edges dictionary 

    def add_edge(self, end):
        self.edges[end] = Edge()  # Create an edge to the destination node

class Vehicle:
    def __init__(self, start, end):
        self.current_node = start
        self.destination = end
        self.time = 0

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, id, is_intersection):
        self.nodes[id] = Node(id, is_intersection)

    def add_edge(self, start, end):
        if start in self.nodes and end in self.nodes:
            self.nodes[start].add_edge(end)

def heuristic_cost_estimate(current, goal):
    #manhattan thing
    return abs(current - goal)

def travel_time(graph, start, end):
    base_time = 1  # Base time for any edge traversal
    edge_delay = graph.nodes[start].edges[end].vehicles * 0.01  # Edge delay due to congestion
    node_delay = 3 if graph.nodes[end].is_intersection else 0   # Node delay due to intersection
    return base_time + edge_delay + node_delay


def local_search(graph, vehicles):
    total_time = 0

    # Store reached vehicles to avoid double processing
    reached_vehicles = set()

    while len(reached_vehicles) < len(vehicles):
        for i, vehicle in enumerate(vehicles):
            # Skip vehicle if it's already reached its destination
            if vehicle in reached_vehicles:
                continue

            # If the vehicle has reached its destination, add it to reached_vehicles
            if vehicle.current_node == vehicle.destination:
                print(f"Vehicle {i} has reached its destination node {vehicle.destination} in time {vehicle.time}")
                reached_vehicles.add(vehicle)
                continue

            next_node = min(
                graph.nodes[vehicle.current_node].edges,
                key=lambda x: heuristic_cost_estimate(x, vehicle.destination)
            )

            # Update edge and time for vehicle's current position
            vehicle.time += travel_time(graph, vehicle.current_node, next_node)
            graph.nodes[vehicle.current_node].edges[next_node].enter()
            
            # Move vehicle to next node
            vehicle.current_node = next_node

    total_time = sum(v.time for v in vehicles)
    return total_time


def main():
    graph = Graph()

    # Nodes
    for i in range(1, 7):
        graph.add_node(i, i == 1 or i == 6 or i==3)

    # Edges
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(3, 5) #SHORTER 
    graph.add_edge(4, 5)
    graph.add_edge(5, 6)
    graph.add_edge(6, 1)

    # Vehicles
   #vehicles = [Vehicle(1, 5), Vehicle(5, 1), Vehicle(3, 5)]
    #vehicles = [Vehicle(2, 4), Vehicle(3, 4), Vehicle(4, 6)]
    vehicles = [Vehicle(1, 5)]

    total_time = local_search(graph, vehicles)
    print(f"Total time taken for all vehicles: {total_time}")

main()
