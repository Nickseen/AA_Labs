"""
Data generation module for graph algorithm testing
"""

import random
from graph_structures import (SimpleGraph, DirectedGraph, WeightedGraph, BipartiteGraph,
                            CompleteGraph, CompleteBipartiteGraph, CycleGraph, Tree,
                            PlanarGraph, EulerianGraph, HamiltonianGraph, ConnectedGraph, DisconnectedGraph)


def generate_test_suite(sizes, graph_types):
    """
    Generate a test suite of graphs with different sizes and types
    
    Parameters:
    -----------
    sizes : list
        List of graph sizes to generate
    graph_types : list
        List of graph types to generate
        
    Returns:
    --------
    test_graphs : dict
        Dictionary mapping (graph_type, size) tuples to graph instances
    """
    test_graphs = {}
    
    for size in sizes:
        for graph_type in graph_types:
            print(f"Generating {graph_type} graph with {size} vertices...")
            
            if graph_type == "simple":
                graph = SimpleGraph(size)
                # Add random edges - approximately 2*size edges for sparse graph
                edge_count = min(size * 2, size * (size - 1) // 2)
                for _ in range(edge_count):
                    u = random.randint(0, size - 1)
                    v = random.randint(0, size - 1)
                    if u != v:  # Avoid self-loops
                        graph.add_edge(u, v)
            
            elif graph_type == "directed":
                graph = DirectedGraph(size)
                # Add random edges
                edge_count = min(size * 2, size * (size - 1))
                for _ in range(edge_count):
                    u = random.randint(0, size - 1)
                    v = random.randint(0, size - 1)
                    if u != v:  # Avoid self-loops
                        graph.add_edge(u, v)
            
            elif graph_type == "weighted":
                graph = WeightedGraph(size)
                # Add random weighted edges
                edge_count = min(size * 2, size * (size - 1) // 2)
                for _ in range(edge_count):
                    u = random.randint(0, size - 1)
                    v = random.randint(0, size - 1)
                    if u != v:  # Avoid self-loops
                        weight = random.randint(1, 10)
                        graph.add_edge(u, v, weight=weight)
            
            elif graph_type == "bipartite":
                # Create roughly equal sets
                n1 = size // 2
                n2 = size - n1
                graph = BipartiteGraph(n1, n2)
                
                # Add random edges between sets
                edge_probability = min(0.5, 10 / size)
                for i in range(n1):
                    for j in range(n1, n1 + n2):
                        if random.random() < edge_probability:
                            graph.add_edge(i, j)
            
            elif graph_type == "complete":
                graph = CompleteGraph(size)
            
            elif graph_type == "complete_bipartite":
                # Create roughly equal sets
                n1 = size // 2
                n2 = size - n1
                graph = CompleteBipartiteGraph(n1, n2)
            
            elif graph_type == "cycle":
                graph = CycleGraph(max(3, size))  # Minimum 3 vertices for a cycle
            
            elif graph_type == "tree":
                graph = Tree(size)
            
            elif graph_type == "planar":
                graph = PlanarGraph(size)
            
            elif graph_type == "eulerian":
                graph = EulerianGraph(size)
            
            elif graph_type == "hamiltonian":
                graph = HamiltonianGraph(size)
            
            elif graph_type == "connected":
                graph = ConnectedGraph(size)
            
            elif graph_type == "disconnected":
                # Create 2-3 components
                num_components = min(3, size // 3)
                if num_components < 2:
                    num_components = 2
                graph = DisconnectedGraph(size, num_components)
            
            else:
                raise ValueError(f"Unknown graph type: {graph_type}")
            
            test_graphs[(graph_type, size)] = graph
    
    return test_graphs


def generate_test_cases(graph, num_trials=50):
    """
    Generate test cases for graph algorithms
    
    Parameters:
    -----------
    graph : Graph
        The graph to generate test cases for
    num_trials : int
        Number of test cases to generate
        
    Returns:
    --------
    test_cases : list
        List of (start_vertex, target_vertex) pairs
    """
    test_cases = []
    
    # Cache of reachable vertices from each starting vertex
    reachable_cache = {}
    
    for _ in range(num_trials):
        start = random.randint(0, graph.num_vertices - 1)
        
        # With 50% probability, choose a target that is reachable from start
        if random.random() < 0.5:
            # If we haven't computed reachable vertices from this start yet, do it now
            if start not in reachable_cache:
                # Use DFS to find all reachable vertices
                visited = set()
                stack = [start]
                while stack:
                    vertex = stack.pop()
                    if vertex not in visited:
                        visited.add(vertex)
                        for neighbor in graph.get_neighbors(vertex):
                            if neighbor not in visited:
                                stack.append(neighbor)
                reachable_cache[start] = list(visited)
            
            # Choose a random reachable target
            reachable = reachable_cache[start]
            if reachable:
                target = random.choice(reachable)
            else:
                target = start  # Fallback if no reachable vertices
        else:
            # Choose any random target
            target = random.randint(0, graph.num_vertices - 1)
        
        test_cases.append((start, target))
    
    return test_cases