# ----------------------
# CP468 AI ASSIGNMENT 1 QUESTION 4
# ----------------------

class Edge:
    def __init__(self):
        self.vehicles = 0  # Initialize the count of vehicles on this edge to zero.

    def enter(self):
        self.vehicles += 1  # Increment the number of vehicles on the edge when a new vehicle enters.

    def exit(self):
        self.vehicles -= 1  # Decrement the number of vehicles on the edge when a vehicle exits.
        if self.vehicles < 0:
            self.vehicles = 0  # Ensure that the count of vehicles doesn't go below zero.

class Node:
    def __init__(self, id, is_intersection):
        self.id = id  # Unique identifier for this node.
        self.is_intersection = is_intersection  # Boolean flag to determine if this node is an intersection.
        self.edges = {}  # Dictionary to store edges associated with this node, indexed by their end node.

    def add_edge(self, end):
        self.edges[end] = Edge()  # Create an edge to the given end node and store it in the dictionary.

class Vehicle:
    def __init__(self, start, end):
        self.current_node = start  # The node where the vehicle currently is.
        self.destination = end  # The destination node of the vehicle.
        self.time = 0  # The total time the vehicle has spent so far.

class Graph:
    def __init__(self):
        self.nodes = {}  # Dictionary to store all nodes in the graph, indexed by their id.

    def add_node(self, id, is_intersection):
        self.nodes[id] = Node(id, is_intersection)  # Add a node with the given id and intersection status to the graph.

    def add_edge(self, start, end):
        # Add an edge between the given start and end nodes if both exist in the graph.
        if start in self.nodes and end in self.nodes:
            self.nodes[start].add_edge(end)  # Add the edge from start to end.

def heuristic_cost_estimate(current, goal):
    # Estimate the cost from the current node to the goal node.
    # Using the absolute difference as a simple heuristic.
    return abs(current - goal)

def travel_time(graph, start, end):
    base_time = 1  # Base time cost for traveling between any two adjacent nodes.
    # Calculate delay due to the number of vehicles currently on the edge from start to end.
    edge_delay = graph.nodes[start].edges[end].vehicles * 0.01
    # If the end node is an intersection, there's an added delay.
    node_delay = 3 if graph.nodes[end].is_intersection else 0
    return base_time + edge_delay + node_delay  # Return the total time for this travel segment.

def local_search(graph, vehicles):
    total_time = 0  # Initialize the total time spent by all vehicles.

    # Set to store vehicles that have already reached their destination to avoid double processing.
    reached_vehicles = set()

    # Continue until all vehicles have reached their destinations.
    while len(reached_vehicles) < len(vehicles):
        for i, vehicle in enumerate(vehicles):
            # If the vehicle has already reached its destination, continue to the next vehicle.
            if vehicle in reached_vehicles:
                continue

            # If the vehicle is at its destination, add it to the reached vehicles set.
            if vehicle.current_node == vehicle.destination:
                print(f"Vehicle {i} has reached its destination node {vehicle.destination} in time {vehicle.time}")
                reached_vehicles.add(vehicle)
                continue

            # Find the best next node to move to based on the heuristic.
            next_node = min(
                graph.nodes[vehicle.current_node].edges,
                key=lambda x: heuristic_cost_estimate(x, vehicle.destination)
            )

            # Update the time for the vehicle and move it to the next node.
            vehicle.time += travel_time(graph, vehicle.current_node, next_node)
            graph.nodes[vehicle.current_node].edges[next_node].enter()
            vehicle.current_node = next_node  # Set the vehicle's current position to the next node.

    # Calculate the total time spent by all vehicles.
    total_time = sum(v.time for v in vehicles)
    return total_time  # Return the total time.

def main():
    graph = Graph()  # Create a new graph.

    # Define nodes and whether they are intersections or not.
    for i in range(1, 7):
        graph.add_node(i, i == 1 or i == 6 or i == 3)  # Nodes 1, 6, and 3 are intersections.

    # Define edges between nodes.
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(3, 5)
    graph.add_edge(4, 5)
    graph.add_edge(5, 6)
    graph.add_edge(6, 1)

    # Define the vehicles, their starting positions, and destinations.
    vehicles = [Vehicle(1, 5)]

    # Run the local search to find optimal paths and calculate the total time.
    total_time = local_search(graph, vehicles)
    print(f"Total time taken for all vehicles: {total_time}")

# Run the main function.
main()
