import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import networkx as nx
from statistics import mean, stdev
from graph_structures import (SimpleGraph, DirectedGraph, WeightedGraph, BipartiteGraph,
                             CompleteGraph, CompleteBipartiteGraph, CycleGraph, Tree,
                             PlanarGraph, EulerianGraph, HamiltonianGraph, ConnectedGraph, DisconnectedGraph)
from graph_algorithms import GraphAlgorithms
from data_generation import generate_test_suite, generate_test_cases

def run_algorithm_benchmark(graph, algorithm, num_trials=50):
    execution_times = []
    vertices_visited = []
    
    # Generate test cases
    test_cases = generate_test_cases(graph, num_trials)
    
    for start, target in test_cases:
        visited, path, execution_time = algorithm(graph, start, target)
        execution_times.append(execution_time)
        vertices_visited.append(len(visited))
    
    # Calculate metrics
    results = {
        "mean_time": mean(execution_times),
        "min_time": min(execution_times),
        "max_time": max(execution_times),
        "std_dev_time": stdev(execution_times) if len(execution_times) > 1 else 0,
        "mean_vertices_visited": mean(vertices_visited),
    }
    
    return results


def compare_algorithms(graph_dict):
    algorithms = {
        "DFS": GraphAlgorithms.dfs,
        "BFS": GraphAlgorithms.bfs
    }
    
    results = {}
    
    for (graph_type, size), graph in graph_dict.items():
        print(f"Benchmarking {graph_type} graph with {size} vertices...")
        
        graph_results = {}
        for algo_name, algo_func in algorithms.items():
            print(f"  Running {algo_name}...")
            benchmark_results = run_algorithm_benchmark(graph, algo_func)
            graph_results[algo_name] = benchmark_results
        
        results[(graph_type, size)] = graph_results
    
    return results


def analyze_results(results):
    data = []
    
    for (graph_type, size), algo_results in results.items():
        for algo_name, metrics in algo_results.items():
            entry = {
                "graph_type": graph_type,
                "size": size,
                "algorithm": algo_name,
                "mean_time": metrics["mean_time"],
                "min_time": metrics["min_time"],
                "max_time": metrics["max_time"],
                "std_dev_time": metrics["std_dev_time"]
            }
            
            # Add additional metrics if they exist
            additional_metrics = [
                "mean_vertices_visited", 
                "mean_path_length", 
                "mean_mst_weight", 
                "mean_edges_processed"
            ]
            
            for metric in additional_metrics:
                if metric in metrics:
                    entry[metric] = metrics[metric]
            
            data.append(entry)
    
    df = pd.DataFrame(data)
    return df


def plot_execution_times(df, metric="mean_time"):
    plt.figure(figsize=(14, 8))
    
    graph_types = df["graph_type"].unique()
    num_types = len(graph_types)
    cols = 3
    rows = (num_types + cols - 1) // cols
    
    for i, graph_type in enumerate(graph_types):
        plt.subplot(rows, cols, i+1)
        
        subset = df[df["graph_type"] == graph_type]
        for algo in subset["algorithm"].unique():
            algo_data = subset[subset["algorithm"] == algo]
            plt.plot(algo_data["size"], algo_data[metric], 
                     marker='o', label=algo)
        
        plt.title(f"{graph_type.capitalize()} Graph")
        plt.xlabel("Number of Vertices")
        plt.ylabel(f"{metric.replace('_', ' ').title()} (seconds)")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xscale('log')
        if len(subset) > 0 and subset[metric].max() > 0:
            plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig(f"1/execution_times_{metric}.png")


def plot_vertices_visited(df, metric="mean_vertices_visited"):
    plt.figure(figsize=(14, 8))
    
    # Check if the metric column exists
    if metric not in df.columns:
        print(f"Warning: Column '{metric}' not found in DataFrame.")
        print("Available columns:", df.columns.tolist())
        return
    
    graph_types = df["graph_type"].unique()
    num_types = len(graph_types)
    
    cols = min(3, num_types)  # Ensure we don't try to create more columns than graph types
    rows = (num_types + cols - 1) // cols
    
    for i, graph_type in enumerate(graph_types):
        plt.subplot(rows, cols, i+1)
        
        subset = df[df["graph_type"] == graph_type]
        for algo in subset["algorithm"].unique():
            algo_data = subset[subset["algorithm"] == algo]
            plt.plot(algo_data["size"], algo_data[metric], 
                     marker='o', label=algo)
        
        plt.title(f"{graph_type.capitalize()} Graph")
        plt.xlabel("Number of Vertices")
        plt.ylabel(f"{metric.replace('_', ' ').title()}")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xscale('log')
        plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig(f"1/vertices_visited_{metric}.png")


def plot_algorithm_comparison(df, size=100):
    sizes = sorted(df["size"].unique())
    closest_size = min(sizes, key=lambda x: abs(x - size))
    
    subset = df[df["size"] == closest_size]
    
    plt.figure(figsize=(12, 6))
    
    # Plot mean execution time
    plt.subplot(1, 2, 1)
    sns.barplot(x="graph_type", y="mean_time", hue="algorithm", data=subset)
    plt.title(f"Mean Execution Time for {closest_size} Vertices")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Graph Type")
    plt.ylabel("Mean Time (seconds)")
    plt.yscale('log')
    plt.grid(True, alpha=0.3)
    
    # Plot mean vertices visited
    plt.subplot(1, 2, 2)
    sns.barplot(x="graph_type", y="mean_vertices_visited", hue="algorithm", data=subset)
    plt.title(f"Mean Vertices Visited for {closest_size} Vertices")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Graph Type")
    plt.ylabel("Mean Vertices Visited")
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"1/algorithm_comparison_size_{closest_size}.png")


def plot_time_complexity_comparison(sizes):
    plt.figure(figsize=(10, 6))
    
    # Plot O(V+E) for different graph densities
    x = np.array(sizes)
    
    # Sparse graph: E = V
    plt.plot(x, x, label='O(V+E) for Sparse Graph (E=V)')
    
    # Medium density: E = V*log(V)
    plt.plot(x, x + x*np.log(x), label='O(V+E) for Medium Density (E=V*log(V))')
    
    # Dense graph: E = V²
    plt.plot(x, x + x**2, label='O(V+E) for Dense Graph (E=V²)')
    
    plt.title('Theoretical Time Complexity Comparison')
    plt.xlabel('Number of Vertices (V)')
    plt.ylabel('Operations')
    plt.grid(True)
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig("1/theoretical_complexity.png")


def visualize_graph_examples():
    graph_examples = {
        "Simple Graph": SimpleGraph(8),
        "Directed Graph": DirectedGraph(8),
        "Weighted Graph": WeightedGraph(8),
        "Bipartite Graph": BipartiteGraph(4, 4),
        "Complete Graph": CompleteGraph(8),
        "Complete Bipartite Graph": CompleteBipartiteGraph(4, 4),
        "Cycle Graph": CycleGraph(8),
        "Tree": Tree(8),
        "Planar Graph": PlanarGraph(8),
        "Eulerian Graph": EulerianGraph(8),
        "Hamiltonian Graph": HamiltonianGraph(8),
        "Connected Graph": ConnectedGraph(8),  # Now separate
        "Disconnected Graph": DisconnectedGraph(8, 2)  # Now separate
    }
    
    # Populate the simple graph with some edges
    for i in range(8):
        for j in range(i+1, 8):
            if j == i+1 or j == (i+3) % 8:
                graph_examples["Simple Graph"].add_edge(i, j)
    
    # Add edges to directed graph
    for i in range(8):
        graph_examples["Directed Graph"].add_edge(i, (i+1) % 8)
        graph_examples["Directed Graph"].add_edge(i, (i+2) % 8)
    
    # Add weighted edges
    for i in range(8):
        graph_examples["Weighted Graph"].add_edge(i, (i+1) % 8, weight=i+1)
        graph_examples["Weighted Graph"].add_edge(i, (i+2) % 8, weight=i*2)
    
    # Add edges to bipartite graph
    for i in range(4):
        for j in range(4, 8):
            if j-4 == i or j-4 == (i+1) % 4:
                graph_examples["Bipartite Graph"].add_edge(i, j)
    
    # Create visualization grid
    plt.figure(figsize=(15, 12))  # Increased size to fit more graph types
    
    grid_size = (4, 4)  # Adjusted grid size for more graphs
    for i, (graph_name, graph) in enumerate(graph_examples.items()):
        plt.subplot(grid_size[0], grid_size[1], i+1)
        
        # Use NetworkX for visualization
        G = graph.to_networkx()
        pos = nx.spring_layout(G, seed=42)
        
        # Draw with different settings based on graph type
        if "Directed" in graph_name:
            nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                   node_size=500, font_size=10, font_weight='bold',
                   arrows=True, arrowsize=15)
        elif "Weighted" in graph_name:
            nx.draw(G, pos, with_labels=True, node_color='lightblue',
                   node_size=500, font_size=10, font_weight='bold')
            edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        elif "Bipartite" in graph_name:
            # Color nodes differently for bipartite graphs
            node_colors = ['lightblue' if node < 4 else 'lightgreen' for node in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_color=node_colors,
                   node_size=500, font_size=10, font_weight='bold')
        else:
            nx.draw(G, pos, with_labels=True, node_color='lightblue',
                   node_size=500, font_size=10, font_weight='bold')
        
        plt.title(graph_name)
    
    plt.tight_layout()
    plt.savefig("1/graph_examples.png")

def run_shortest_path_benchmark(graph, algorithm, num_trials=50):
    execution_times = []
    path_lengths = []
    vertices_visited = []
    
    # Generate test cases
    test_cases = generate_test_cases(graph, num_trials)
    
    for start, target in test_cases:
        # Check if it's Floyd-Warshall (takes only graph) or Dijkstra (takes graph and start)
        if algorithm.__name__ == 'floyd_warshall':
            # Floyd-Warshall computes all pairs at once
            distances, paths, execution_time = algorithm(graph)
            # For Floyd-Warshall, distances is a 2D matrix
            if start in distances and target in distances[start]:
                path_lengths.append(distances[start][target])
            else:
                path_lengths.append(float('inf'))
            # Count all vertices for which we computed distances
            vertices_visited.append(graph.num_vertices * graph.num_vertices)
        else:
            # Dijkstra computes single source
            distances, paths, execution_time = algorithm(graph, start)
            if target in distances:
                path_lengths.append(distances[target])
            else:
                path_lengths.append(float('inf'))
            # Count vertices with calculated distances
            vertices_visited.append(len(distances))
        
        execution_times.append(execution_time)
    
    # Calculate metrics
    results = {
        "mean_time": mean(execution_times),
        "min_time": min(execution_times),
        "max_time": max(execution_times),
        "std_dev_time": stdev(execution_times) if len(execution_times) > 1 else 0,
        "mean_vertices_visited": mean(vertices_visited),
        "mean_path_length": mean([x for x in path_lengths if x != float('inf')]) if any(x != float('inf') for x in path_lengths) else float('inf'),
    }
    
    return results

def compare_shortest_path_algorithms(graph_dict):
    algorithms = {
        "Dijkstra": GraphAlgorithms.dijkstra,
        "Floyd-Warshall": GraphAlgorithms.floyd_warshall
    }
    
    results = {}
    
    # Make a copy of the graph_dict for weighted graphs
    weighted_graph_dict = {}
    
    for (graph_type, size), graph in graph_dict.items():
        print(f"Benchmarking {graph_type} graph with {size} vertices...")
        
        # Create a weighted version of the graph if it's not already weighted
        if not hasattr(graph, 'get_weight'):
            print(f"  Converting {graph_type} to weighted graph...")
            weighted_graph = WeightedGraph(graph.num_vertices)
            
            # Copy edges from original graph and add random weights
            for u in range(graph.num_vertices):
                for v in graph.get_neighbors(u):
                    # Only add edge from u to v once since WeightedGraph adds both directions
                    if u < v:  # This ensures each edge is only added once
                        weight = np.random.randint(1, 10)  # Random weight between 1 and 9
                        weighted_graph.add_edge(u, v, weight=weight)
            
            # Store the weighted version
            weighted_graph_dict[(f"weighted_{graph_type}", size)] = weighted_graph
        else:
            # If it's already weighted, use it as is
            weighted_graph_dict[(graph_type, size)] = graph
    
    # Now run algorithms on the weighted graphs
    for (graph_type, size), graph in weighted_graph_dict.items():
        print(f"  Testing on {graph_type} with {size} vertices...")
        
        graph_results = {}
        for algo_name, algo_func in algorithms.items():
            print(f"    Running {algo_name}...")
            benchmark_results = run_shortest_path_benchmark(graph, algo_func)
            graph_results[algo_name] = benchmark_results
        
        results[(graph_type, size)] = graph_results
    
    return results

def plot_shortest_path_execution_times(df, metric="mean_time"):
    plt.figure(figsize=(14, 8))
    
    # Check if df is empty
    if df.empty:
        print("Warning: DataFrame is empty. Cannot plot execution times.")
        return
    
    # Verify that necessary columns exist
    required_cols = ["graph_type", "size", "algorithm", metric]
    for col in required_cols:
        if col not in df.columns:
            print(f"Warning: DataFrame missing required column '{col}'. Available columns: {df.columns.tolist()}")
            return
    
    graph_types = df["graph_type"].unique()
    num_types = len(graph_types)
    
    if num_types == 0:
        print("Warning: No graph types found in DataFrame.")
        return
        
    cols = min(3, num_types)  # Ensure we don't try to create more columns than graph types
    rows = (num_types + cols - 1) // cols
    
    for i, graph_type in enumerate(graph_types):
        plt.subplot(rows, cols, i+1)
        
        subset = df[df["graph_type"] == graph_type]
        for algo in subset["algorithm"].unique():
            algo_data = subset[subset["algorithm"] == algo]
            plt.plot(algo_data["size"], algo_data[metric], 
                     marker='o', label=algo)
        
        plt.title(f"{graph_type.capitalize()} Graph")
        plt.xlabel("Number of Vertices")
        plt.ylabel(f"{metric.replace('_', ' ').title()} (seconds)")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xscale('log')
        if len(subset) > 0 and subset[metric].max() > 0:
            plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig(f"2/shortest_path_{metric}.png")

def plot_path_lengths(df, metric="mean_path_length"):
    plt.figure(figsize=(14, 8))
    
    # Check if df is empty or missing columns
    if df.empty or "graph_type" not in df.columns:
        print("Warning: DataFrame is empty or missing 'graph_type' column.")
        return
    
    graph_types = df["graph_type"].unique()
    num_types = len(graph_types)
    cols = min(3, num_types)  # Ensure we don't try to create more columns than graph types
    rows = (num_types + cols - 1) // cols
    
    for i, graph_type in enumerate(graph_types):
        plt.subplot(rows, cols, i+1)
        
        subset = df[df["graph_type"] == graph_type]
        for algo in subset["algorithm"].unique():
            algo_data = subset[subset["algorithm"] == algo]
            # Filter out infinity values
            finite_data = algo_data[algo_data[metric] != float('inf')]
            if len(finite_data) > 0:
                plt.plot(finite_data["size"], finite_data[metric], 
                         marker='o', label=algo)
        
        plt.title(f"{graph_type.capitalize()} Graph")
        plt.xlabel("Number of Vertices")
        plt.ylabel(f"{metric.replace('_', ' ').title()}")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xscale('log')
        if len(subset) > 0 and any(subset[metric] != float('inf')):
            plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig(f"2/shortest_path_{metric}.png")

def plot_shortest_path_algorithm_comparison(df, size=100):
    # Check if df is empty or missing columns
    if df.empty or "size" not in df.columns:
        print("Warning: DataFrame is empty or missing 'size' column.")
        return
    
    sizes = sorted(df["size"].unique())
    if not sizes:
        print("Warning: No sizes found in DataFrame.")
        return
        
    closest_size = min(sizes, key=lambda x: abs(x - size))
    
    subset = df[df["size"] == closest_size]
    
    if subset.empty:
        print(f"Warning: No data for size {closest_size} in DataFrame.")
        return
    
    plt.figure(figsize=(12, 6))
    
    # Plot mean execution time
    plt.subplot(1, 2, 1)
    sns.barplot(x="graph_type", y="mean_time", hue="algorithm", data=subset)
    plt.title(f"Mean Execution Time for {closest_size} Vertices")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Graph Type")
    plt.ylabel("Mean Time (seconds)")
    plt.yscale('log')
    plt.grid(True, alpha=0.3)
    
    # Plot mean path length
    plt.subplot(1, 2, 2)
    # Filter out infinity values
    finite_subset = subset[subset["mean_path_length"] != float('inf')]
    if len(finite_subset) > 0:
        sns.barplot(x="graph_type", y="mean_path_length", hue="algorithm", data=finite_subset)
        plt.title(f"Mean Path Length for {closest_size} Vertices")
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Graph Type")
        plt.ylabel("Mean Path Length")
        plt.grid(True, alpha=0.3)
    else:
        plt.text(0.5, 0.5, "No finite path lengths to display", 
                 horizontalalignment='center', verticalalignment='center')
    
    plt.tight_layout()
    plt.savefig(f"2/shortest_path_comparison_size_{closest_size}.png")

def plot_complexity_comparison(sizes):
    plt.figure(figsize=(10, 6))
    
    x = np.array(sizes)
    
    # Dijkstra with binary heap: O(E + V log V)
    plt.plot(x, x * np.log(x) + x, label='Dijkstra (Binary Heap): O(E + V log V)')
    
    # Dijkstra with array: O(V²)
    plt.plot(x, x**2, label='Dijkstra (Array): O(V²)')
    
    # Floyd-Warshall: O(V³)
    plt.plot(x, x**3, label='Floyd-Warshall: O(V³)')
    
    plt.title('Theoretical Time Complexity Comparison for Shortest Path Algorithms')
    plt.xlabel('Number of Vertices (V)')
    plt.ylabel('Operations')
    plt.grid(True)
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig("2/shortest_path_theoretical_complexity.png")

def run_mst_benchmark(graph, algorithm, num_trials=10):
    """
    Benchmark a minimum spanning tree algorithm on a graph
    
    Parameters:
    - graph: The graph object
    - algorithm: The MST algorithm to benchmark (prim or kruskal)
    - num_trials: Number of times to run the algorithm for reliable timing
    
    Returns:
    - Dictionary with benchmark metrics
    """
    import time
    from statistics import mean, stdev
    
    execution_times = []
    mst_weights = []
    edges_processed = []
    
    for _ in range(num_trials):
        start_time = time.time()
        mst, total_weight, edges_checked = algorithm(graph)
        end_time = time.time()
        
        execution_time = end_time - start_time
        execution_times.append(execution_time)
        mst_weights.append(total_weight)
        edges_processed.append(edges_checked)
    
    # Calculate metrics
    results = {
        "mean_time": mean(execution_times),
        "min_time": min(execution_times),
        "max_time": max(execution_times),
        "std_dev_time": stdev(execution_times) if len(execution_times) > 1 else 0,
        "mean_mst_weight": mean(mst_weights),
        "mean_edges_processed": mean(edges_processed),
    }
    
    return results


def compare_mst_algorithms(graph_dict):
    """
    Compare Prim's and Kruskal's algorithms across different graph types and sizes
    
    Parameters:
    - graph_dict: Dictionary mapping (graph_type, size) to graph objects
    
    Returns:
    - Dictionary mapping (graph_type, size) to algorithm results
    """
    from graph_algorithms import GraphAlgorithms
    
    algorithms = {
        "Prim": GraphAlgorithms.prim,
        "Kruskal": GraphAlgorithms.kruskal
    }
    
    results = {}
    
    # Make a copy of the graph_dict for weighted graphs
    weighted_graph_dict = {}
    
    for (graph_type, size), graph in graph_dict.items():
        print(f"Benchmarking {graph_type} graph with {size} vertices...")
        
        # Create a weighted version of the graph if it's not already weighted
        if not hasattr(graph, 'get_weight'):
            print(f"  Converting {graph_type} to weighted graph...")
            weighted_graph = WeightedGraph(graph.num_vertices)
            
            # Copy edges from original graph and add random weights
            for u in range(graph.num_vertices):
                for v in graph.get_neighbors(u):
                    # Only add edge from u to v once since WeightedGraph adds both directions
                    if u < v:  # This ensures each edge is only added once
                        weight = np.random.randint(1, 10)  # Random weight between 1 and 9
                        weighted_graph.add_edge(u, v, weight=weight)
            
            # Store the weighted version
            weighted_graph_dict[(f"weighted_{graph_type}", size)] = weighted_graph
        else:
            # If it's already weighted, use it as is
            weighted_graph_dict[(graph_type, size)] = graph
    
    # Now run algorithms on the weighted graphs
    for (graph_type, size), graph in weighted_graph_dict.items():
        print(f"  Testing on {graph_type} with {size} vertices...")
        
        # Skip graphs that are not suitable for MST
        if ("disconnected" in graph_type or 
            not nx.is_connected(graph.to_networkx())):
            print(f"  Skipping {graph_type} - requires a connected graph")
            continue
            
        graph_results = {}
        for algo_name, algo_func in algorithms.items():
            try:
                print(f"    Running {algo_name}...")
                benchmark_results = run_mst_benchmark(graph, algo_func)
                graph_results[algo_name] = benchmark_results
            except ValueError as e:
                print(f"    Skipping {algo_name}: {str(e)}")
        
        if graph_results:  # Only add results if at least one algorithm succeeded
            results[(graph_type, size)] = graph_results
    
    return results


def plot_mst_execution_times(df, metric="mean_time"):
    """
    Plot execution time comparisons for MST algorithms
    
    Parameters:
    - df: DataFrame with benchmark results
    - metric: The metric to plot (mean_time, min_time, etc.)
    """
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(14, 8))
    
    # Check if df is empty
    if df.empty:
        print("Warning: DataFrame is empty. Cannot plot execution times.")
        return
    
    graph_types = df["graph_type"].unique()
    num_types = len(graph_types)
    
    if num_types == 0:
        print("Warning: No graph types found in DataFrame.")
        return
        
    cols = min(3, num_types)  # Ensure we don't try to create more columns than graph types
    rows = (num_types + cols - 1) // cols
    
    for i, graph_type in enumerate(graph_types):
        plt.subplot(rows, cols, i+1)
        
        subset = df[df["graph_type"] == graph_type]
        for algo in subset["algorithm"].unique():
            algo_data = subset[subset["algorithm"] == algo]
            plt.plot(algo_data["size"], algo_data[metric], 
                     marker='o', label=algo)
        
        plt.title(f"{graph_type.capitalize()} Graph")
        plt.xlabel("Number of Vertices")
        plt.ylabel(f"{metric.replace('_', ' ').title()} (seconds)")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xscale('log')
        if len(subset) > 0 and subset[metric].max() > 0:
            plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig(f"3/mst_{metric}.png")


def plot_mst_edges_processed(df, metric="mean_edges_processed"):
    """
    Plot number of edges processed by MST algorithms
    
    Parameters:
    - df: DataFrame with benchmark results
    - metric: The metric to plot (mean_edges_processed)
    """
    import matplotlib.pyplot as plt
    
    # Check if the metric column exists
    if metric not in df.columns:
        print(f"Warning: Column '{metric}' not found in DataFrame.")
        print("Available columns:", df.columns.tolist())
        return
    
    plt.figure(figsize=(14, 8))
    
    # Check if df is empty
    if df.empty:
        print("Warning: DataFrame is empty. Cannot plot edges processed.")
        return
    
    graph_types = df["graph_type"].unique()
    num_types = len(graph_types)
    
    if num_types == 0:
        print("Warning: No graph types found in DataFrame.")
        return
        
    cols = min(3, num_types)  # Ensure we don't try to create more columns than graph types
    rows = (num_types + cols - 1) // cols
    
    for i, graph_type in enumerate(graph_types):
        plt.subplot(rows, cols, i+1)
        
        subset = df[df["graph_type"] == graph_type]
        for algo in subset["algorithm"].unique():
            algo_data = subset[subset["algorithm"] == algo]
            plt.plot(algo_data["size"], algo_data[metric], 
                     marker='o', label=algo)
        
        plt.title(f"{graph_type.capitalize()} Graph")
        plt.xlabel("Number of Vertices")
        plt.ylabel(f"{metric.replace('_', ' ').title()}")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xscale('log')
        plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig(f"3/mst_{metric}.png")


def plot_mst_algorithm_comparison(df, size=100):
    """
    Plot side-by-side comparison of MST algorithms for a specific graph size
    
    Parameters:
    - df: DataFrame with benchmark results
    - size: The graph size to compare
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Check if df is empty or missing columns
    if df.empty or "size" not in df.columns:
        print("Warning: DataFrame is empty or missing 'size' column.")
        return
    
    sizes = sorted(df["size"].unique())
    if not sizes:
        print("Warning: No sizes found in DataFrame.")
        return
        
    closest_size = min(sizes, key=lambda x: abs(x - size))
    
    subset = df[df["size"] == closest_size]
    
    if subset.empty:
        print(f"Warning: No data for size {closest_size} in DataFrame.")
        return
    
    plt.figure(figsize=(12, 6))
    
    # Plot mean execution time
    plt.subplot(1, 2, 1)
    sns.barplot(x="graph_type", y="mean_time", hue="algorithm", data=subset)
    plt.title(f"Mean Execution Time for {closest_size} Vertices")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Graph Type")
    plt.ylabel("Mean Time (seconds)")
    plt.yscale('log')
    plt.grid(True, alpha=0.3)
    
    # Plot mean edges processed
    plt.subplot(1, 2, 2)
    sns.barplot(x="graph_type", y="mean_edges_processed", hue="algorithm", data=subset)
    plt.title(f"Mean Edges Processed for {closest_size} Vertices")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Graph Type")
    plt.ylabel("Mean Edges Processed")
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"3/mst_comparison_size_{closest_size}.png")


def plot_mst_complexity_comparison(sizes):
    """
    Plot theoretical time complexity for MST algorithms
    
    Parameters:
    - sizes: List of graph sizes to plot
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    plt.figure(figsize=(10, 6))
    
    x = np.array(sizes)
    
    # Prim's with binary heap: O(E log V)
    # For sparse graphs E ~ V, for dense graphs E ~ V²
    plt.plot(x * np.log(x), label="Prim's (Binary Heap) - Sparse: O(V log V)")
    plt.plot(x**2 * np.log(x), label="Prim's (Binary Heap) - Dense: O(V² log V)")
    
    # Kruskal's: O(E log E) ~ O(E log V)
    # For sparse graphs E ~ V, for dense graphs E ~ V²
    plt.plot(x * np.log(x), label="Kruskal's - Sparse: O(V log V)")
    plt.plot(x**2 * np.log(x), label="Kruskal's - Dense: O(V² log V)")
    
    plt.title('Theoretical Time Complexity for MST Algorithms')
    plt.xlabel('Number of Vertices (V)')
    plt.ylabel('Operations')
    plt.grid(True)
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig("3/mst_theoretical_complexity.png")


def algorithm_analysis():
    """Main function to run the empirical analysis"""
    print("Starting graph algorithm analysis...")
    
    # Generate test graphs
    print("Generating test graphs...")
    sizes = [10, 20, 50, 100, 200, 500]
    graph_types = [
        "simple", "directed", "weighted", "bipartite",
        "complete", "complete_bipartite", "cycle", "tree",
        "planar", "eulerian", "hamiltonian", "connected", "disconnected"
    ]
    
    test_graphs = generate_test_suite(sizes, graph_types)
    
    # Run algorithm comparison
    print("Running algorithm comparison...")
    results = compare_algorithms(test_graphs)
    
    # Analyze results
    print("Analyzing results...")
    df = analyze_results(results)
    
    # Generate visualizations
    print("Generating visualizations...")
    plot_execution_times(df, "mean_time")
    plot_vertices_visited(df, "mean_vertices_visited")
    plot_algorithm_comparison(df, 100)
    
    # Generate theoretical complexity plot
    plot_time_complexity_comparison(sizes + [500, 1000, 2000])
    
    # Create graph examples visualization
    visualize_graph_examples()
    
    print("Analysis complete! Results saved to files.")

def shortest_path_algorithm_analysis():
    """Main function to run the empirical analysis for shortest path algorithms"""
    print("Starting shortest path algorithm analysis...")
    
    # Make directories for output
    import os
    os.makedirs("2", exist_ok=True)
    
    # Generate test graphs (focus on weighted graphs)
    print("Generating test graphs...")
    sizes = [10, 20, 50, 100]  # Reduced max size for faster execution with Floyd-Warshall
    graph_types = [
        "simple", "directed", "weighted", "bipartite",
        "complete", "complete_bipartite", "cycle", "tree",
        "planar", "eulerian", "hamiltonian", "connected", "disconnected"
    ]
    
    test_graphs = generate_test_suite(sizes, graph_types)
    
    # Run algorithm comparison
    print("Running algorithm comparison...")
    results = compare_shortest_path_algorithms(test_graphs)
    
    # Analyze results
    print("Analyzing results...")
    if not results:
        print("Error: No results were generated. Check the implementation of shortest path algorithms.")
        return
        
    df = analyze_results(results)
    
    if df.empty:
        print("Error: DataFrame is empty. Check the analysis function.")
        return
    
    print("Generated DataFrame with columns:", df.columns.tolist())
    print("Generated DataFrame with graph types:", df["graph_type"].unique().tolist() if "graph_type" in df.columns else "No graph_type column")
    
    # Generate visualizations
    print("Generating visualizations...")
    plot_shortest_path_execution_times(df, "mean_time")
    plot_path_lengths(df, "mean_path_length")
    plot_shortest_path_algorithm_comparison(df, 100)
    
    # Generate theoretical complexity plot
    plot_complexity_comparison(sizes + [500, 1000, 2000])
    
    print("Analysis complete! Results saved to files.")

def mst_algorithm_analysis():
    """Main function to run the empirical analysis for MST algorithms"""
    print("Starting MST algorithm analysis...")
    
    # Generate test graphs (focus on weighted graphs)
    print("Generating test graphs...")
    sizes = [10, 20, 50, 100, 200, 500]
    graph_types = [
        "simple", "directed", "weighted", "bipartite",
        "complete", "complete_bipartite", "cycle", "tree",
        "planar", "eulerian", "hamiltonian", "connected", "disconnected"
    ]
    
    test_graphs = generate_test_suite(sizes, graph_types)
    
    # Run algorithm comparison
    print("Running algorithm comparison...")
    results = compare_mst_algorithms(test_graphs)
    
    # Analyze results
    print("Analyzing results...")
    if not results:
        print("Error: No results were generated. Check the implementation of MST algorithms.")
        return
        
    df = analyze_results(results)
    
    if df.empty:
        print("Error: DataFrame is empty. Check the analysis function.")
        return
    
    print("Generated DataFrame with columns:", df.columns.tolist())
    
    # Generate visualizations
    print("Generating visualizations...")
    plot_mst_execution_times(df, "mean_time")
    plot_mst_edges_processed(df, "mean_edges_processed")
    plot_mst_algorithm_comparison(df, 100)
    
    # Generate theoretical complexity plot
    plot_mst_complexity_comparison(sizes + [1000, 2000, 5000])
    
    print("Analysis complete! Results saved to files.")


if __name__ == "__main__":
    algorithm_analysis()
    shortest_path_algorithm_analysis()
    mst_algorithm_analysis()
