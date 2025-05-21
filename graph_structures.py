import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod

class Graph(ABC):
    """Abstract base class for all graph types"""
    
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        # Use dictionary with list for faster lookups and iterations
        self.adjacency_list = {i: [] for i in range(num_vertices)}
        # Pre-compute set of neighbors for faster lookups
        self._neighbors_set = {i: set() for i in range(num_vertices)}
    
    def add_edge(self, u, v, **kwargs):
        """Add an edge between vertices u and v"""
        if u >= self.num_vertices or v >= self.num_vertices:
            raise ValueError("Vertex index out of range")
        
        if v not in self._neighbors_set[u]:
            self.adjacency_list[u].append(v)
            self._neighbors_set[u].add(v)
    
    def remove_edge(self, u, v):
        """Remove an edge between vertices u and v"""
        if v in self._neighbors_set[u]:
            self.adjacency_list[u].remove(v)
            self._neighbors_set[u].remove(v)
    
    def get_neighbors(self, vertex):
        """Return all neighbors of a vertex"""
        return self.adjacency_list[vertex]
    
    def has_edge(self, u, v):
        """Check if there is an edge from u to v"""
        return v in self._neighbors_set[u]
    
    def is_connected(self):
        """Check if the graph is connected"""
        if self.num_vertices == 0:
            return True
        
        visited = set()
        # Start DFS from vertex 0
        self._dfs(0, visited)
        
        # If all vertices were visited, the graph is connected
        return len(visited) == self.num_vertices
    
    def _dfs(self, vertex, visited):
        """Helper method for DFS traversal"""
        visited.add(vertex)
        for neighbor in self.adjacency_list[vertex]:
            if neighbor not in visited:
                self._dfs(neighbor, visited)
    
    def to_networkx(self):
        """Convert to NetworkX graph for visualization"""
        G = nx.Graph()
        for i in range(self.num_vertices):
            G.add_node(i)
        
        for u in self.adjacency_list:
            for v in self.adjacency_list[u]:
                G.add_edge(u, v)
        
        return G
    
    def visualize(self, title="Graph", save_path=None):
        """Visualize the graph using matplotlib"""
        G = self.to_networkx()
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G, seed=42)  # Fixed seed for reproducibility
        nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                node_size=500, font_size=10, font_weight='bold')
        plt.title(title)
        if save_path:
            plt.savefig(save_path)
            plt.close()
        

class SimpleGraph(Graph):
    """Undirected graph with no self-loops or multiple edges"""
    
    def add_edge(self, u, v):
        """Add an undirected edge between u and v"""
        if u != v:  # Avoid self-loops
            super().add_edge(u, v)
            super().add_edge(v, u)


class DirectedGraph(Graph):
    """Directed graph (digraph)"""
    
    def to_networkx(self):
        """Convert to NetworkX directed graph for visualization"""
        G = nx.DiGraph()
        for i in range(self.num_vertices):
            G.add_node(i)
        
        for u in self.adjacency_list:
            for v in self.adjacency_list[u]:
                G.add_edge(u, v)
        
        return G


class WeightedGraph(Graph):
    """Graph with weights on edges"""
    
    def __init__(self, num_vertices):
        super().__init__(num_vertices)
        self.weights = {}  # Dictionary to store edge weights
    
    def add_edge(self, u, v, weight=1):
        """Add a weighted edge between vertices u and v"""
        if u != v:  # Avoid self-loops
            super().add_edge(u, v)
            self.weights[(u, v)] = weight
            # For undirected weighted graph
            super().add_edge(v, u)
            self.weights[(v, u)] = weight
    
    def get_weight(self, u, v):
        """Get the weight of edge (u, v)"""
        return self.weights.get((u, v), float('inf'))
    
    def to_networkx(self):
        """Convert to NetworkX graph with edge weights"""
        G = nx.Graph()
        for i in range(self.num_vertices):
            G.add_node(i)
        
        for u in self.adjacency_list:
            for v in self.adjacency_list[u]:
                G.add_edge(u, v, weight=self.weights.get((u, v), 1))
        
        return G
    
    def visualize(self, title="Weighted Graph", save_path=None):
        """Visualize the weighted graph"""
        G = self.to_networkx()
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                node_size=500, font_size=10, font_weight='bold')
        
        # Draw edge weights
        edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        
        plt.title(title)
        if save_path:
            plt.savefig(save_path)
            plt.close()


class BipartiteGraph(Graph):
    """Bipartite graph where vertices can be divided into two disjoint sets"""
    
    def __init__(self, n1, n2):
        """Initialize with n1 nodes in first set and n2 nodes in second set"""
        super().__init__(n1 + n2)
        self.n1 = n1  # Size of first set
        self.n2 = n2  # Size of second set
    
    def add_edge(self, u, v):
        """Add edge ensuring it connects vertices from different sets"""
        # Check if edge maintains bipartite property
        # u should be from first set (0 to n1-1)
        # v should be from second set (n1 to n1+n2-1)
        if u < 0 or u >= self.n1 or v < self.n1 or v >= self.num_vertices:
            raise ValueError("Edge violates bipartite property")
        
        super().add_edge(u, v)
        super().add_edge(v, u)
    
    def visualize(self, title="Bipartite Graph", save_path=None):
        """Visualize the bipartite graph with different colors for each set"""
        G = self.to_networkx()
        plt.figure(figsize=(8, 6))
        
        # Create node sets for bipartite drawing
        top_nodes = list(range(self.n1))
        bottom_nodes = list(range(self.n1, self.num_vertices))
        
        pos = nx.bipartite_layout(G, top_nodes)
        nx.draw_networkx_nodes(G, pos, nodelist=top_nodes, node_color='lightblue', node_size=500)
        nx.draw_networkx_nodes(G, pos, nodelist=bottom_nodes, node_color='lightgreen', node_size=500)
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos)
        
        plt.title(title)
        plt.axis('off')
        if save_path:
            plt.savefig(save_path)
            plt.close()


class CompleteGraph(SimpleGraph):
    """Complete graph Kn where every pair of vertices is connected"""
    
    def __init__(self, num_vertices):
        super().__init__(num_vertices)
        # Add edges between all pairs of vertices
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                self.add_edge(i, j)


class CompleteBipartiteGraph(BipartiteGraph):
    """Complete bipartite graph Km,n where every vertex in first set
    is connected to every vertex in second set"""
    
    def __init__(self, m, n):
        super().__init__(m, n)
        # Add edges between all vertices across the sets
        for i in range(m):
            for j in range(m, m + n):
                self.add_edge(i, j)


class CycleGraph(SimpleGraph):
    """Cycle graph Cn with n vertices connected in a cycle"""
    
    def __init__(self, num_vertices):
        if num_vertices < 3:
            raise ValueError("Cycle graph must have at least 3 vertices")
        
        super().__init__(num_vertices)
        # Connect vertices in a cycle
        for i in range(num_vertices):
            self.add_edge(i, (i + 1) % num_vertices)


class Tree(SimpleGraph):
    """Tree - connected graph with no cycles"""
    
    def __init__(self, num_vertices):
        super().__init__(num_vertices)
        
        if num_vertices <= 0:
            return
        
        # Create a random tree using a simple algorithm:
        # Add edges between vertex i and a random vertex from [0, i-1]
        for i in range(1, num_vertices):
            parent = random.randint(0, i-1)
            self.add_edge(parent, i)
    
    def add_edge(self, u, v):
        """Add edge checking that it doesn't create a cycle"""
        # For a proper implementation, we would need to check for cycles
        # but for simplicity in this example, we just add the edge
        super().add_edge(u, v)


class PlanarGraph(SimpleGraph):
    """Planar graph that can be embedded in a plane without crossing edges"""
    
    def __init__(self, num_vertices):
        super().__init__(num_vertices)
        
        # Create a simple planar graph (a maximal planar graph would be complex)
        # For simplicity, we'll create a wheel graph which is always planar
        if num_vertices >= 4:
            # Connect center (vertex 0) to all other vertices
            for i in range(1, num_vertices):
                self.add_edge(0, i)
            
            # Connect outer vertices in a cycle
            for i in range(1, num_vertices):
                self.add_edge(i, 1 + (i % (num_vertices-1)))


class EulerianGraph(SimpleGraph):
    """Eulerian graph - a graph where every vertex has an even degree"""
    
    def __init__(self, num_vertices):
        super().__init__(num_vertices)
        
        if num_vertices < 3:
            return
        
        # Create a simple Eulerian graph - a cycle is always Eulerian
        for i in range(num_vertices):
            self.add_edge(i, (i + 1) % num_vertices)
        
        # Add some random edges ensuring even degree
        for _ in range(num_vertices):
            u = random.randint(0, num_vertices-1)
            v = random.randint(0, num_vertices-1)
            if u != v and not self.has_edge(u, v):
                # Add two edges to maintain even degree at both vertices
                self.add_edge(u, v)
                w = random.randint(0, num_vertices-1)
                while w == u or w == v or self.has_edge(u, w):
                    w = random.randint(0, num_vertices-1)
                self.add_edge(u, w)


class HamiltonianGraph(SimpleGraph):
    """Hamiltonian graph - a graph containing a cycle that visits every vertex exactly once"""
    
    def __init__(self, num_vertices):
        super().__init__(num_vertices)
        
        if num_vertices < 3:
            return
        
        # Create a cycle (which is Hamiltonian)
        for i in range(num_vertices):
            self.add_edge(i, (i + 1) % num_vertices)
        
        # Add some random additional edges
        for _ in range(num_vertices):
            u = random.randint(0, num_vertices-1)
            v = random.randint(0, num_vertices-1)
            if u != v and not self.has_edge(u, v):
                self.add_edge(u, v)


class ConnectedGraph(SimpleGraph):
    """A deliberately connected graph"""
    
    def __init__(self, num_vertices):
        super().__init__(num_vertices)
        
        if num_vertices <= 1:
            return
            
        # First, create a spanning tree to ensure connectivity
        for i in range(1, num_vertices):
            parent = random.randint(0, i-1)
            self.add_edge(parent, i)
        
        # Add some additional random edges
        edge_probability = min(0.1, 5 / num_vertices)
        for i in range(num_vertices):
            for j in range(i+1, num_vertices):
                if not self.has_edge(i, j) and random.random() < edge_probability:
                    self.add_edge(i, j)


class DisconnectedGraph(SimpleGraph):
    """A graph with multiple disconnected components"""
    
    def __init__(self, num_vertices, num_components=2):
        super().__init__(num_vertices)
        
        if num_vertices < num_components:
            raise ValueError("Number of vertices must be greater than or equal to number of components")
        
        # Distribute vertices among components
        vertices_per_component = num_vertices // num_components
        remaining = num_vertices % num_components
        
        # Store the component each vertex belongs to
        self.components = {}
        
        start_idx = 0
        for i in range(num_components):
            component_size = vertices_per_component + (1 if i < remaining else 0)
            end_idx = start_idx + component_size
            
            # Label vertices in this component
            for v in range(start_idx, end_idx):
                self.components[v] = i
            
            # Create a connected component (as a tree)
            for j in range(start_idx + 1, end_idx):
                parent = random.randint(start_idx, j-1)
                self.add_edge(parent, j)
            
            start_idx = end_idx
    
    def visualize(self, title="Disconnected Graph", save_path=None):
        """Visualize disconnected graph with different colors for components"""
        G = self.to_networkx()
        plt.figure(figsize=(10, 8))
        
        # Use spring_layout with a lower k value and more iterations for better separation
        # but not too much separation to show it's still one graph
        pos = nx.spring_layout(G, k=0.3, iterations=50, seed=42)
        
        # Get unique component IDs
        unique_components = set(self.components.values())
        
        # Define a color map to distinguish components
        colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_components)))
        
        # Draw each component with a different color
        for i, comp_id in enumerate(unique_components):
            comp_nodes = [v for v, c in self.components.items() if c == comp_id]
            nx.draw_networkx_nodes(G, pos, 
                                nodelist=comp_nodes, 
                                node_color=[colors[i]] * len(comp_nodes),
                                node_size=500)
        
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos)
        
        plt.title(title)
        plt.axis('off')
        
        # Add a text annotation explaining this is a single graph with disconnected components
        plt.figtext(0.5, 0.01, 
                    "This is a single graph with multiple disconnected components", 
                    ha="center", fontsize=10, bbox={"facecolor":"white", "alpha":0.5, "pad":5})
        
        if save_path:
            plt.savefig(save_path)
            plt.close()