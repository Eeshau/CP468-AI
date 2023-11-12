# Revised simulation considering the new requirements from the image provided.

class TrafficGraph:
    def __init__(self):
        self.edges = {}  # dictionary to hold edges and their respective travel times

    def add_edge(self, from_node, to_node, intersection=False):
        # Edges are one-directional. Intersection edges take 3 seconds to traverse.
        edge_time = 3 if intersection else 1
        self.edges[(from_node, to_node)] = Edge(edge_time, intersection)

    def get_edge(self, from_node, to_node):
        return self.edges.get((from_node, to_node), None)

    def update_congestion(self):
        # Update the congestion delay for all edges based on the number of vehicles
        for edge in self.edges.values():
            edge.update_travel_time()

class Edge:
    def __init__(self, base_time, intersection):
        self.base_time = base_time
        self.intersection = intersection
        self.vehicles = 0
        self.travel_time = base_time

    def enter(self):
        self.vehicles += 1

    def exit(self):
        self.vehicles = max(self.vehicles - 1, 0)

    def update_travel_time(self):
        # Time is the base time plus a congestion delay of 0.01s for each vehicle on the edge.
        self.travel_time = self.base_time + 0.01 * self.vehicles

class Vehicle:
    def __init__(self, start, destination):
        self.current = start
        self.destination = destination
        self.total_time = 0

    def move(self, next_node, graph):
        edge = graph.get_edge(self.current, next_node)
        if edge:
            edge.enter()  # Vehicle enters the edge
            self.total_time += edge.travel_time  # Add the travel time of the edge to the vehicle's total time
            self.current = next_node  # Move the vehicle to the next node
            edge.exit()  # Vehicle exits the edge

# Simulation function considering simultaneous movement of vehicles
def simulate_traffic(graph, vehicles, agent):
    # Run until all vehicles reach their destination
    while any(vehicle.current != vehicle.destination for vehicle in vehicles):
        graph.update_congestion()  # Update congestion delay based on the number of vehicles
        for vehicle in vehicles:
            if vehicle.current != vehicle.destination:
                current_state = vehicle.current
                action = agent.choose_action(current_state)  # Choose next edge based on Q-values
                vehicle.move(action[1], graph)  # Move vehicle to next node
                reward = -graph.get_edge(*action).travel_time  # Negative reward of travel time
                next_state = vehicle.current
                agent.learn(current_state, action, reward, next_state)

    # Output the results after all vehicles have reached their destinations
    total_time = sum(v.total_time for v in vehicles)
    for i, vehicle in enumerate(vehicles):
        print(f"Vehicle {i} has reached its destination node {vehicle.destination} in time {vehicle.total_time:.2f} s")
    print(f"Total time taken for all vehicles: {total_time:.2f} s")

# Initialize the traffic graph with intersection nodes
graph = TrafficGraph()
graph.add_edge(1, 2)
graph.add_edge(2, 3, intersection=True)  # Intersection node
graph.add_edge(3, 4)
graph.add_edge(4, 5, intersection=True)  # Intersection node
graph.add_edge(5, 6)
graph.add_edge(6, 1, intersection=True)  # Intersection node

# Initialize vehicles
vehicles = [Vehicle(1, 5), Vehicle(5, 1), Vehicle(3, 5)]

# Initialize the Q-learning agent
agent = QLearningAgent(graph)

# Run the simulation
simulate_traffic(graph, vehicles, agent)