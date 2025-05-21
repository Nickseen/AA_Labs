import time
from collections import deque
from functools import lru_cache
import heapq

class DisjointSet:
    """Implementation of disjoint-set data structure for Kruskal's algorithm"""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        """Find the representative of the set containing x (with path compression)"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """Merge the sets containing x and y (union by rank)"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        else:
            self.parent[root_y] = root_x
            if self.rank[root_x] == self.rank[root_y]:
                self.rank[root_x] += 1
        
        return True

class GraphAlgorithms:    
    @staticmethod
    def dfs(graph, start_vertex, target=None):
        start_time = time.time()
        
        visited = set()
        path = []
        found = False
        neighbors_cache = {}
        for v in range(graph.num_vertices):
            neighbors_cache[v] = graph.get_neighbors(v)
        def _dfs_recursive(vertex):
            nonlocal found
            if found:
                return
            visited.add(vertex)
            path.append(vertex)
            if target is not None and vertex == target:
                found = True
                return
            for neighbor in neighbors_cache[vertex]:
                if neighbor not in visited:
                    _dfs_recursive(neighbor)
                    if found:
                        return
        _dfs_recursive(start_vertex)
        execution_time = time.time() - start_time
        return visited, path, execution_time
    
    @staticmethod
    def dfs_iterative(graph, start_vertex, target=None):
        start_time = time.time()
        
        visited = set()
        path = []
        stack = [start_vertex]
        
        # Pre-fetch neighbors for each vertex to avoid repeated calls during iteration
        neighbors_cache = {}
        for v in range(graph.num_vertices):
            neighbors_cache[v] = graph.get_neighbors(v)
        
        while stack and (target is None or target not in visited):
            vertex = stack.pop()
            
            if vertex not in visited:
                visited.add(vertex)
                path.append(vertex)
                
                if target is not None and vertex == target:
                    break
                
                # Add neighbors in reverse order so that the traversal remains the same
                neighbors = neighbors_cache[vertex]
                for neighbor in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        execution_time = time.time() - start_time
        return visited, path, execution_time
    
    @staticmethod
    def bfs(graph, start_vertex, target=None):
        start_time = time.time()
        
        visited = set([start_vertex])
        path = [start_vertex]
        queue = deque([start_vertex])
        
        neighbors_cache = {}
        for v in range(graph.num_vertices):
            neighbors_cache[v] = graph.get_neighbors(v)
        
        while queue and (target is None or target not in visited):
            vertex = queue.popleft()
            
            if target is not None and vertex == target:
                break
                
            for neighbor in neighbors_cache[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    queue.append(neighbor)
        
        execution_time = time.time() - start_time
        return visited, path, execution_time
    
    @staticmethod
    def find_path_dfs(graph, start_vertex, target_vertex):
        if start_vertex == target_vertex:
            return [start_vertex]
            
        # Use dictionary to track visited nodes and their paths
        visited = {}
        path = []
        found = [False]
        
        # Pre-fetch neighbors
        neighbors_cache = {}
        for v in range(graph.num_vertices):
            neighbors_cache[v] = graph.get_neighbors(v)
        
        def _dfs_path_cached(vertex, current_path):
            if found[0]:
                return
                
            visited[vertex] = True
            current_path.append(vertex)
            
            if vertex == target_vertex:
                found[0] = True
                path.extend(current_path)
                return
            
            for neighbor in neighbors_cache[vertex]:
                if neighbor not in visited and not found[0]:
                    _dfs_path_cached(neighbor, current_path)
            
            if not found[0]:
                current_path.pop()
        
        _dfs_path_cached(start_vertex, [])
        return path if found[0] else []
    
    @staticmethod
    def find_path_bfs(graph, start_vertex, target_vertex):
        if start_vertex == target_vertex:
            return [start_vertex]
            
        # Use efficient data structures
        visited = {start_vertex}
        queue = deque([(start_vertex, [start_vertex])])
        
        # Pre-fetch neighbors
        neighbors_cache = {}
        for v in range(graph.num_vertices):
            neighbors_cache[v] = graph.get_neighbors(v)
        
        while queue:
            vertex, path = queue.popleft()
            
            for neighbor in neighbors_cache[vertex]:
                if neighbor == target_vertex:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    # Only store the path we need, not all possible paths
                    queue.append((neighbor, path + [neighbor]))
        
        return []  # No path found
    
    @staticmethod
    @lru_cache(maxsize=128)  # Cache results to avoid repeating computation
    def is_connected(graph):
        if graph.num_vertices == 0:
            return True
            
        visited, _, _ = GraphAlgorithms.dfs(graph, 0)
        return len(visited) == graph.num_vertices
    
    @staticmethod
    def find_connected_components(graph):
        visited = set()
        components = []
        
        # Pre-fetch all nodes to avoid dynamic attribute lookups
        all_vertices = list(range(graph.num_vertices))
        
        for vertex in all_vertices:
            if vertex not in visited:
                component_visited, _, _ = GraphAlgorithms.dfs(graph, vertex)
                components.append(list(component_visited))
                visited.update(component_visited)
        
        return components
    
    @staticmethod
    def dijkstra(graph, start_vertex):
        start_time = time.time()
        
        # Initialize distances and predecessors
        distances = {v: float('inf') for v in range(graph.num_vertices)}
        distances[start_vertex] = 0
        predecessors = {v: None for v in range(graph.num_vertices)}
        
        # Priority queue to store vertices that need to be processed
        # Format: (distance, vertex)
        import heapq
        pq = [(0, start_vertex)]
        
        # Set to keep track of vertices for which we know the shortest path
        processed = set()
        
        while pq:
            # Get vertex with minimum distance
            current_distance, current_vertex = heapq.heappop(pq)
            
            # If we've already processed this vertex, skip it
            if current_vertex in processed:
                continue
            
            # Mark as processed
            processed.add(current_vertex)
            
            # If the current distance is greater than the known distance, skip
            if current_distance > distances[current_vertex]:
                continue
            
            # Process all neighbors
            for neighbor in graph.get_neighbors(current_vertex):
                weight = graph.get_weight(current_vertex, neighbor)
                distance = current_distance + weight
                
                # If we found a shorter path to the neighbor
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(pq, (distance, neighbor))
        
        execution_time = time.time() - start_time
        return distances, predecessors, execution_time

    @staticmethod
    def floyd_warshall(graph):
        start_time = time.time()
        
        n = graph.num_vertices
        
        # Initialize distance and predecessor matrices
        distances = [[float('inf') for _ in range(n)] for _ in range(n)]
        predecessors = [[None for _ in range(n)] for _ in range(n)]
        
        # Initialize diagonal elements to 0 (distance to self)
        for i in range(n):
            distances[i][i] = 0
        
        # Initialize direct edges
        for u in range(n):
            for v in graph.get_neighbors(u):
                weight = graph.get_weight(u, v)
                distances[u][v] = weight
                predecessors[u][v] = u
        
        # Dynamic programming approach
        # For each vertex k, consider it as an intermediate vertex
        for k in range(n):
            # For each pair of vertices (i, j)
            for i in range(n):
                for j in range(n):
                    # If going through k provides a shorter path
                    if distances[i][k] != float('inf') and distances[k][j] != float('inf'):
                        if distances[i][j] > distances[i][k] + distances[k][j]:
                            distances[i][j] = distances[i][k] + distances[k][j]
                            predecessors[i][j] = predecessors[k][j]
        
        execution_time = time.time() - start_time
        return distances, predecessors, execution_time
    
    @staticmethod
    def prim(graph):
        """
        Prim's algorithm for finding Minimum Spanning Tree
        
        Parameters:
        - graph: Weighted graph with get_weight method
        
        Returns:
        - mst: List of (u, v, weight) edges in the MST
        - total_weight: Sum of weights in the MST
        - edges_processed: Number of edges processed during execution
        """
        import heapq
        
        if not hasattr(graph, 'get_weight'):
            raise ValueError("Prim's algorithm requires a weighted graph")
            
        n = graph.num_vertices
        
        # Start from vertex 0
        start_vertex = 0
        
        # Keep track of the MST
        mst = []
        total_weight = 0
        
        # Track visited vertices
        visited = [False] * n
        
        # Priority queue for selecting minimum-weight edges
        # Format: (weight, vertex, from_vertex)
        pq = [(0, start_vertex, -1)]  # Start with vertex 0
        
        edges_processed = 0
        
        while pq and len(mst) < n - 1:
            weight, vertex, from_vertex = heapq.heappop(pq)
            edges_processed += 1
            
            if visited[vertex]:
                continue
            
            visited[vertex] = True
            
            if from_vertex != -1:  # Not the start vertex
                mst.append((from_vertex, vertex, weight))
                total_weight += weight
                
            # Add all unvisited neighbors to the priority queue
            for neighbor in graph.get_neighbors(vertex):
                if not visited[neighbor]:
                    edge_weight = graph.get_weight(vertex, neighbor)
                    heapq.heappush(pq, (edge_weight, neighbor, vertex))
        
        # Check if MST spans the entire graph
        if sum(visited) != n:
            raise ValueError("Graph is not connected, MST doesn't exist")
            
        return mst, total_weight, edges_processed

    @staticmethod
    def kruskal(graph):
        """
        Kruskal's algorithm for finding Minimum Spanning Tree
        
        Parameters:
        - graph: Weighted graph with get_weight method
        
        Returns:
        - mst: List of (u, v, weight) edges in the MST
        - total_weight: Sum of weights in the MST
        - edges_processed: Number of edges processed during execution
        """
        if not hasattr(graph, 'get_weight'):
            raise ValueError("Kruskal's algorithm requires a weighted graph")
            
        n = graph.num_vertices
        
        # Get all edges with weights
        edges = []
        for u in range(n):
            for v in graph.get_neighbors(u):
                if u < v:  # Only consider each edge once
                    weight = graph.get_weight(u, v)
                    edges.append((u, v, weight))
        
        # Sort edges by weight
        edges.sort(key=lambda x: x[2])
        
        # Initialize disjoint-set data structure
        ds = DisjointSet(n)
        
        # Keep track of the MST
        mst = []
        total_weight = 0
        
        edges_processed = 0
        
        for u, v, weight in edges:
            edges_processed += 1
            
            # Check if adding this edge creates a cycle
            if ds.find(u) != ds.find(v):
                # Add edge to MST
                mst.append((u, v, weight))
                total_weight += weight
                
                # Merge components
                ds.union(u, v)
                
                # Check if MST is complete
                if len(mst) == n - 1:
                    break
        
        # Check if MST spans the entire graph
        if len(mst) != n - 1:
            raise ValueError("Graph is not connected, MST doesn't exist")
            
        return mst, total_weight, edges_processed