"""Dijkstra's algorithm for directed, non-negative weighted graphs."""
import heapq
import math
from itertools import count


def dijkstra(graph, source, destination, trace=None):
    if not isinstance(graph, dict) or not isinstance(source, str) or not isinstance(destination, str):
        raise ValueError('Provide a graph and valid source and destination')
    if source not in graph or destination not in graph:
        raise ValueError('Source and destination must be present in the graph')
    # Validate the entire graph, including unreachable edges and paths beyond the destination.
    for node, neighbors in graph.items():
        if not isinstance(node, str) or not node or not isinstance(neighbors, dict):
            raise ValueError('Graph nodes must be non-empty strings with neighbor objects')
        for neighbor, weight in neighbors.items():
            if neighbor not in graph:
                raise ValueError('Every neighbor must be present in the graph')
            if isinstance(weight, bool) or not isinstance(weight, (int, float)) or weight < 0:
                raise ValueError('Edge weights must be finite non-negative numbers')
            try:
                finite = math.isfinite(weight)
            except OverflowError:
                finite = False
            if not finite:
                raise ValueError('Edge weights must be finite non-negative numbers')
    try:
        if not math.isfinite(math.fsum(weight for neighbors in graph.values() for weight in neighbors.values())):
            raise ValueError('Total edge weight is too large')
    except OverflowError:
        raise ValueError('Total edge weight is too large')
    # Start every location at infinity except the chosen source.
    distances = {node: float('inf') for node in graph}
    predecessors = {node: None for node in graph}
    distances[source] = 0
    sequence = count()
    queue = [(0, next(sequence), source)]
    visited = set()
    visited_order = []
    while queue:
        # Take the closest unvisited location from the min-heap.
        distance, _, node = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        visited_order.append(node)
        if trace is not None:
            trace.append(f'Select {node} with shortest known distance {distance}.')
        if node == destination:
            break
        for neighbor, weight in graph[node].items():
            # Relax this road when it improves the known distance.
            candidate = distance + weight
            if candidate < distances[neighbor]:
                if trace is not None:
                    trace.append(f'Relax {node} → {neighbor}: update distance to {candidate}.')
                distances[neighbor] = candidate
                predecessors[neighbor] = node
                heapq.heappush(queue, (candidate, next(sequence), neighbor))
    # Follow predecessors backwards to reconstruct the path.
    path = []
    if distances[destination] != float('inf'):
        current = destination
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()
    return distances[destination], path, predecessors, visited_order
