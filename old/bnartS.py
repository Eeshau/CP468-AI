# For all intersection nodes there is a delay TDelay → There can only be one car at each intersection node. Delay of 3
# For all edges there is another delay C% which is based off of how many cars are traversing that specific edge. Delay percent of the number of cars on the link
# Following the papers values: the node delay is set to 3, the edge multiplier is number of vehicles as a percent
# Each vehicle=1%
# Don't need to do 3* the amount of vehicles on the intersection because there will only be one vehicle at an intersection at a given time. (3*1=3)
# Visited is a set of nodes that have been visited
# Graph is a dictionary of all the nodes
# To add an edge we add the (x,y) to the nodes neighbors array



class Node:
    def __init__(self, id, is_intersection):
        self.id = id  # Unique identifier for the node
        self.is_intersection = is_intersection  # Boolean to indicate if this node is an intersection
        self.neighbors = []  # List to store neighboring nodes
        self.occupied = False  # Boolean to indicate if this node is occupied by a vehicle

    def occupy(self):
        self.occupied = True  # Method to mark the node as occupied

    def vacate(self):
        self.occupied = False  # Method to mark the node as unoccupied

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)  # Method to add a neighboring node


class Graph:
    def __init__(self):
        self.nodes = {}  # Dictionary to store all nodes in the graph

    def add_node(self, id, is_intersection):
        self.nodes[id] = Node(id, is_intersection)  # Method to add a node to the graph

    def add_edge(self, start, end):
        if start in self.nodes and end in self.nodes:
            self.nodes[start].add_neighbor(end)  # Method to add an edge by adding a neighbor to a node



# def local_search(graph, vehicles):
#     visited = set()  # Set to store visited nodes
#     total_time = 0  # Variable to keep track of the total time spent

#     for vehicle in vehicles:  # Iterating through each vehicle
#         current = vehicle['start']  # Current node is the starting point of the vehicle
#         destination = vehicle['end']  # Destination node of the vehicle
#         while current != destination:  # Loop until the current node is not the destination node
#             visited.add(current)  # Mark the current node as visited
#             # Select the next node based on the minimum cost to travel
#             next_node = min(graph.nodes[current].neighbors, key=lambda x: cost_to_travel(graph, x, visited))
#             # Update the total time with the time taken to travel to the next node
#             total_time += travel_time(graph, current, next_node, visited)
#             current = next_node  # Update the current node to the next node

#     return total_time  # Return the total time spent


def local_search(graph, vehicles):
    total_time = 0  # Variable to keep track of the total time spent
    vehicle_times = {i: 0 for i in range(len(vehicles))}  # Dictionary to store the time taken for each vehicle

    # Initialize current nodes and destinations for each vehicle
    current_nodes = {i: vehicle['start'] for i, vehicle in enumerate(vehicles)}
    destinations = {i: vehicle['end'] for i, vehicle in enumerate(vehicles)}

    # Continue until all vehicles have reached their destinations
    while current_nodes:
        # Dictionary to store the next node for each vehicle
        next_nodes = {}

        for i, current in current_nodes.items():
            # If this vehicle has reached its destination, print the message and remove it from the current_nodes dict
            if current == destinations[i]:
                print(f"Vehicle {i} has reached its destination node {destinations[i]} in time {vehicle_times[i]}")
                del current_nodes[i]
            else:
                # Otherwise, find the next node for this vehicle
                next_node = min(graph.nodes[current].neighbors, key=lambda x: cost_to_travel(graph, x, set()))
                travel_time_cost = travel_time(graph, current, next_node, set())
                total_time += travel_time_cost
                vehicle_times[i] += travel_time_cost
                next_nodes[i] = next_node

        # Update the current nodes for the next iteration
        current_nodes = next_nodes

        # Add a delay for each vehicle based on the number of vehicles on the same edge
        for i, current in current_nodes.items():
            vehicles_on_edge = sum(1 for j, other_current in current_nodes.items() if i != j and other_current == current)
            delay = vehicles_on_edge * 0.01
            total_time += delay
            vehicle_times[i] += delay

    return total_time  # Return the total time spent




def cost_to_travel(graph, node, visited):
    if node in visited:  # If the node has been visited, return infinity
        return float('inf')
    if graph.nodes[node].is_intersection:  # If it's an intersection, return a fixed delay of 3
        return 3
    return 1  # Otherwise, return a fixed cost of 1


def travel_time(graph, start, end, visited):
    if graph.nodes[end].is_intersection:  # If the destination node is an intersection, set a fixed delay of 3
        delay = 3
    else:
        delay = 0  # Otherwise, no delay

    # Calculate the delay based on the number of vehicles on this edge
    vehicles_on_edge = sum([1 for v in visited if end in graph.nodes[v].neighbors])
    delay += vehicles_on_edge * 0.01  # Update the delay based on the number of vehicles on the edge

    return delay  # Return the delay




def main():
    graph = Graph()  # Create a graph object
    
    # Setting up the graph based on a mock setup
    for i in range(1, 7):
        graph.add_node(i, i == 1 or i == 6)  # Add nodes to the graph
    

    # #CASE 1: circle no intersections, all vechiles need a 3 second delay for reaching end node + decimal delay on each edge
    # graph.add_edge(1, 2)  # Add edges to the graph
    # graph.add_edge(2, 3)
    # graph.add_edge(3, 4)
    # graph.add_edge(4, 5)
    # ###
    # graph.add_edge(5,1)


    # #CASE 2: vehile 1 has 2 options to get to desintation, 1 option is shorter and another is longer the code should choose the shortest path
    # graph.add_edge(1, 2)  # Add edges to the graph
    # graph.add_edge(2, 3)
    # graph.add_edge(3, 4)
    # graph.add_edge(4, 5)
    # ###
    # #graph.add_edge(5,1)
    # graph.add_edge(5,6)
    # graph.add_edge(6,1)



    #CASE 3: vehile that doesn't move
    graph.add_edge(1, 2)  # Add edges to the graph
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    ###
    #graph.add_edge(5,1)
    graph.add_edge(5,6)
    graph.add_edge(6,1)




    # Define the vehicles with their starting and ending nodes
    #vehicles = [{'start': 1, 'end': 5}, {'start': 5, 'end': 1}, {'start': 3, 'end': 5}]
    vehicles = [{'start': 1, 'end': 5}, {'start': 5, 'end': 1}, {'start': 5, 'end': 1}]

    total_time = local_search(graph, vehicles)  # Call the local_search function
    print(f"Total time taken for all vehicles: {total_time}")  # Print the total time taken



main()  # Call the main function
