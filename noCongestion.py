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
def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph.nodes:
        return []
    paths = []
    for node in graph.nodes[start].edges:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def calculate_path_time(graph, path):
    total_time = 0
    for i in range(len(path) - 1):
        total_time += travel_time(graph, path[i], path[i+1])
    return total_time

def q_learning(graph, vehicle):
    all_paths = find_all_paths(graph, vehicle.current_node, vehicle.destination)
    path_times = {tuple(path): calculate_path_time(graph, path) for path in all_paths}
    best_path = min(path_times, key=path_times.get)
    return path_times, best_path

def main():
    graph = Graph()
    # ... [Unchanged code to initialize graph and vehicles]
    # Define nodes and whether they are intersections or not.
    for i in range(1, 7):
        graph.add_node(i, i == 1 or i == 6 or i == 3)  # Nodes 1, 6, and 3 are intersections.

    # Define edges between nodes.
    #TEST CASE 1    vehicles = [Vehicle(1, 5)]
    # graph.add_edge(1, 2)
    # graph.add_edge(2, 3)
    # graph.add_edge(3, 4)
    # graph.add_edge(3, 5)
    # graph.add_edge(4, 5)
    # graph.add_edge(5, 6)
    # graph.add_edge(6, 1)

    #TEST CASE 2         vehicles = [Vehicle(1, 5), Vehicle(5, 1), Vehicle(3, 5)]
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(5, 6)
    graph.add_edge(6, 1)




    # Define the vehicles, their starting positions, and destinations.
    # vehicles = [Vehicle(1, 5)]
    vehicles = [Vehicle(1, 5), Vehicle(5, 1), Vehicle(3, 5)]


    for vehicle in vehicles:
        path_times, best_path = q_learning(graph, vehicle)
        print(f"Vehicle from {vehicle.current_node} to {vehicle.destination}:")
        print("All path times:", path_times)
        print("Best path:", best_path, "with time", path_times[best_path])

# Run the main function.
main()