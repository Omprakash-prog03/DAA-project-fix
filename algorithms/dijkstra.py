import heapq

def dijkstra(graph, source, destination):
    """
    Manual Dijkstra implementation
    Returns: distance, path, predecessors, visited_order
    """
    # graph: {node: {neighbor: weight, ...}, ...}
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    predecessors = {node: None for node in graph}
    visited_order = []
    
    # Priority queue: (distance, node)
    pq = [(0, source)]
    visited = set()
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_node in visited:
            continue
            
        visited.add(current_node)
        visited_order.append(current_node)
        
        if current_node == destination:
            break
            
        for neighbor, weight in graph.get(current_node, {}).items():
            if weight < 0:
                raise ValueError("Negative edge weights not supported in Dijkstra")
                
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
                
    # Reconstruct path
    path = []
    curr = destination
    if distances[destination] != float('inf'):
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]
        path.reverse()
    else:
        distance = float('inf')
        
    return distances[destination], path, predecessors, visited_order
