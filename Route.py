import streamlit as st
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO

# Function to read the graph from a text file
def read_graph(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    num_vertices = int(lines[0].strip())
    edges = []
    for line in lines[1:]:
        vertex1, vertex2, distance = map(int, line.strip().split())
        edges.append((vertex1, vertex2, distance))
    return num_vertices, edges

# Function to read building mappings from a text file
def read_building_mapping(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    num_buildings = int(lines[0].strip())
    mapping = {}
    reverse_mapping = {}
    for line in lines[1:]:
        vertex, code = line.strip().split()
        mapping[int(vertex)] = code
        reverse_mapping[code] = int(vertex)
    return num_buildings, mapping, reverse_mapping

# Function to create an adjacency matrix
def create_adjacency_matrix(num_vertices, edges):
    adj_matrix = [[float('inf')] * num_vertices for _ in range(num_vertices)]
    for vertex1, vertex2, distance in edges:
        adj_matrix[vertex1][vertex2] = distance
        adj_matrix[vertex2][vertex1] = distance
    return adj_matrix

# Dijkstra's Algorithm to find shortest path
def dijkstra(adj_matrix, start_vertex):
    num_vertices = len(adj_matrix)
    distances = [float('inf')] * num_vertices
    distances[start_vertex] = 0
    priority_queue = [(0, start_vertex)]
    predecessors = [-1] * num_vertices

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in enumerate(adj_matrix[current_vertex]):
            if weight != float('inf'):
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))

    return distances, predecessors

# Function to get the shortest path from the predecessors list
def shortest_path(predecessors, start_vertex, end_vertex):
    path = []
    current_vertex = end_vertex
    while current_vertex != -1:
        path.append(current_vertex)
        current_vertex = predecessors[current_vertex]
    path.reverse()
    return path

# Read graph and building data
num_vertices, edges = read_graph('graph.txt')
num_buildings, building_mapping, reverse_building_mapping = read_building_mapping('mappings.txt')

# Create the adjacency matrix
adj_matrix = create_adjacency_matrix(num_vertices, edges)

# Streamlit application
st.title("Northeastern University Boston Campus - Shortest Path Finder")

st.sidebar.header("Select Buildings")

# Dropdowns to select start and end buildings
start_building_code = st.sidebar.selectbox("Start Building", list(reverse_building_mapping.keys()))
end_building_code = st.sidebar.selectbox("End Building", list(reverse_building_mapping.keys()))

if st.sidebar.button("Find Shortest Path"):
    start_vertex = reverse_building_mapping[start_building_code]
    end_vertex = reverse_building_mapping[end_building_code]

    distances, predecessors = dijkstra(adj_matrix, start_vertex)
    path = shortest_path(predecessors, start_vertex, end_vertex)

    if distances[end_vertex] == float('inf'):
        st.error("No path found between the selected buildings.")
    else:
        st.success(f"Shortest path from {start_building_code} to {end_building_code}:")
        path_codes = [building_mapping[v] if v in building_mapping else str(v) for v in path]
        st.write(" -> ".join(path_codes))
        st.write(f"Total distance: {distances[end_vertex]} ft")
        
        # Plot and display the graph
        G = nx.Graph()
        for vertex1, vertex2, distance in edges:
            G.add_edge(vertex1, vertex2, weight=distance)
        labels = {vertex: code for vertex, code in building_mapping.items()}
        pos = nx.spring_layout(G, seed=42, k=2)
        
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, labels=labels, node_size=1000, node_color='skyblue', font_size=8, font_weight='bold', font_color='black', edge_color='gray')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
        
        # Highlight the shortest path
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

        # Save plot to a bytes buffer
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        st.image(buf, caption="Campus Map with Shortest Path", use_column_width=True)
        plt.close()
