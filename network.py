import networkx as nx
from pyvis.network import Network

# Path to your .edges file
edges_file_path = 'aves-barn-swallow-contact-network.edges'

# Read data from the .edges file
with open(edges_file_path, 'r') as file:
    edges_data = [line.split() for line in file]

# Create a directed graph from the edges data
G = nx.DiGraph()
for edge in edges_data:
    source, target, weight = edge
    G.add_edge(source, target, weight=float(weight))

# Dijkstra's algorithm to find shortest paths
source_node = source # Replace this with the actual source node in your graph

# Compute shortest paths and distances from the source node
shortest_paths = nx.single_source_dijkstra_path(G, source_node)
shortest_distances = nx.single_source_dijkstra_path_length(G, source_node)

# Highlight the shortest paths in the visualization
for target_node, path in shortest_paths.items():
    for i in range(len(path) - 1):
        edge_color = "#00FF00"  # Green color for the shortest path edges
        G.edges[path[i], path[i + 1]]['color'] = edge_color

# Network analysis
node_degrees = dict(G.degree())
node_centrality = nx.degree_centrality(G)

# Create a Pyvis network
net = Network(height='800px', width='100%', notebook=True)

# Add nodes and edges to the Pyvis network
for node in G.nodes():
    net.add_node(node, label=node, title=f'Degree: {node_degrees[node]}', color=node_degrees[node], size=node_centrality[node] * 20, attribute='value')

for edge in G.edges(data=True):
    net.add_edge(edge[0], edge[1], value=edge[2]['weight'], title=f'Weight: {edge[2]["weight"]}', width=edge[2]['weight'], attribute='value', color=edge[2].get('color', None))

# Set Pyvis physics layout for better visualization
net.force_atlas_2based()

# Add legend and title
options = {
    "nodes": {
        "borderWidth": 2,
        "color": {
            "highlight": {
                "background": "#FF0000"
            }
        }
    },
    "edges": {
        "color": {
            "inherit": True
        },
        "smooth": {
            "type": "continuous"
        }
    },
    "interaction": {
        "hover": True,
        "navigationButtons": True,
        "keyboard": {
            "enabled": True
        },
        "zoomView": False
    },
    "manipulation": {
        "enabled": True
    },
    "physics": {
        "enabled": True,
        "stabilization": {
            "iterations": 1000,
            "updateInterval": 100
        }
    }
}

try:
    net.set_options(options)
except Exception as e:
    print(f"An error occurred while setting options: {e}")

# Save or display the interactive plot
net.show('swallow_bird_network_pyvis_with_dijkstra.html')
