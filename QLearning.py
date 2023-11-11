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
    q_table = {}
    for vehicle in vehicles:
        for start_node in graph.nodes.values():  # For each possible start node
            for end_node in graph.nodes.values():  # For each possible end node
                # Initialize Q-values for actions from start_node to all possible end nodes
                q_table[(start_node.id, vehicle.destination, end_node.id)] = \
                    {next_node: 0 for next_node in graph.nodes[end_node.id].edges}
    return q_table


def choose_next_node(q_table, current_node, destination, epsilon):
    # Retrieve the Q-values for the current state
    current_actions = q_table.get((current_node, destination, current_node), {})
    
    # If there are no actions for the current state, return None or a default action
    if not current_actions:
        return None
    
    # Exploration or exploitation
    if np.random.uniform(0, 1) < epsilon:  # Exploration
        next_node = np.random.choice(list(current_actions.keys()))
    else:  # Exploitation
        next_node = max(current_actions, key=current_actions.get)
    return next_node



def update_q_table(q_table, graph, vehicle, next_node, alpha, gamma):
    # Define the current state using the vehicle's current node and destination.
    current_state = (vehicle.current_node, vehicle.destination, vehicle.current_node)
    
    # Define the next state using the next node to move to and the vehicle's destination.
    next_state = (next_node, vehicle.destination, next_node)
    
    # If the next state is not in the Q-table, initialize it with zero values for all possible actions.
    if next_state not in q_table:
        q_table[next_state] = {neighbor: 0 for neighbor in graph.nodes[next_node].edges}
    
    # Get the reward, which is the negative of the travel time (since we want to minimize travel time).
    reward = -travel_time(graph, vehicle.current_node, next_node)
    
    # Get the current Q-value for the current state and action (moving to the next node).
    current_q = q_table[current_state][next_node]
    
    # Check if there are any actions for the next state and find the maximum Q-value.
    # If there are no actions (empty dict), set max_future_q to 0.
    max_future_q = max(q_table[next_state].values()) if q_table[next_state] else 0
    
    # Update the Q-value for the current state and action using the Q-learning formula.
    q_table[current_state][next_node] = (1 - alpha) * current_q + alpha * (reward + gamma * max_future_q)



# def travel_time(graph, start, end):
#     # Make sure an edge exists before calculating travel time
#     if end in graph.nodes[start].edges:
#         base_time = 1
#         edge_delay = graph.nodes[start].edges[end].vehicles * 0.01
#         node_delay = 3 if graph.nodes[end].is_intersection else 0
#         return base_time + edge_delay + node_delay
#     else:
#         return float('inf')  # Return infinite cost if there is no direct edge bettewn the start and end nodes

def travel_time(graph, start, end):
    print(f"Calculating travel time from {start} to {end}")
    if end in graph.nodes[start].edges:
        base_time = 1
        edge_delay = graph.nodes[start].edges[end].vehicles * 0.01
        node_delay = 3 if graph.nodes[end].is_intersection else 0
        total_time = base_time + edge_delay + node_delay
        print(f"Travel time from {start} to {end}: {total_time}")
        return total_time
    else:
        print(f"No direct edge from {start} to {end}, returning inf")
        return float('inf')


# def q_learning(graph, vehicles, q_table, alpha, gamma, epsilon):
#     total_time = 0
#     for vehicle in vehicles:
#         while vehicle.current_node != vehicle.destination:
#             next_node = choose_next_node(q_table, vehicle.current_node, vehicle.destination, epsilon)
            
#             # If there is no next node, break out of the loop or handle the case as needed
#             if next_node is None:
#                 print(f"No possible actions for vehicle at node {vehicle.current_node}")
#                 break
            
#             update_q_table(q_table, graph, vehicle, next_node, alpha, gamma)
#             vehicle.current_node = next_node  # Move to the next node
#             total_time += travel_time(graph, vehicle.current_node, next_node)  # Update the total time
#     return total_time



def q_learning(graph, vehicles, q_table, alpha, gamma, epsilon):
    total_time = 0
    for vehicle in vehicles:
        print(f"Vehicle starting at {vehicle.current_node} heading to {vehicle.destination}")
        while vehicle.current_node != vehicle.destination:
            next_node = choose_next_node(q_table, vehicle.current_node, vehicle.destination, epsilon)
            
            if next_node is None:
                print(f"No possible actions for vehicle at node {vehicle.current_node}")
                break
            
            print(f"Moving from {vehicle.current_node} to {next_node}")
            update_q_table(q_table, graph, vehicle, next_node, alpha, gamma)
            vehicle.current_node = next_node  # Move to the next node
            travel_cost = travel_time(graph, vehicle.current_node, next_node)
            print(f"Travel cost from {vehicle.current_node} to {next_node}: {travel_cost}")
            total_time += travel_cost  # Update the total time
            if total_time == float('inf'):
                print("Encountered an infinite travel cost. Breaking loop.")
                break
    return total_time



# Main function to run the algorithm

def main():
    graph = Graph()

    # Define nodes and whether they are intersections or not.
    for i in range(1, 7):
        graph.add_node(i, i == 1 or i == 6 or i == 3)  # Nodes 1, 6, and 3 are intersections.

    # Define edges between nodes.
    graph.add_edge(1, 2)
    graph.add_edge(1, 5) #
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(3, 5)
    graph.add_edge(4, 5)
    graph.add_edge(5, 6)
    graph.add_edge(6, 1)

    # Define the vehicles, their starting positions, and destinations.
    vehicles = [Vehicle(1, 5)]

    # Print the graph structure after initialization
    for node_id, node in graph.nodes.items():
        print(f"Node {node_id} has edges to: {list(node.edges.keys())}")

    q_table = initialize_q_table(graph, vehicles)

    # Parameters for Q-learning
    alpha = 0.1  # Learning rate
    gamma = 0.6  # Discount factor
    epsilon = 0.1  # Exploration rate

    total_time = q_learning(graph, vehicles, q_table, alpha, gamma, epsilon)
    print(f"Total time taken for all vehicles: {total_time}")

# Run the main function
main()
