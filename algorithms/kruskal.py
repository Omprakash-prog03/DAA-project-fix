import math

class UnionFind:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])  # Path compression
        return self.parent[node]

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            # Union by rank
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1
            return True
        return False  # Cycle detected


def kruskal_mst(nodes, edges, trace=None):
    """
    Manual Kruskal implementation
    Returns: mst_edges, total_weight, selected_edges, rejected_edges
    """
    if not isinstance(nodes, list) or any(not isinstance(n, str) or not n for n in nodes) or len(set(nodes)) != len(nodes):
        raise ValueError('Nodes must be unique non-empty strings')
    if not isinstance(edges, list):
        raise ValueError('Edges must be a list')
    known = set(nodes)
    weights = []
    for edge in edges:
        if (not isinstance(edge, dict) or not isinstance(edge.get('source'), str)
                or not isinstance(edge.get('destination'), str)
                or edge['source'] not in known or edge['destination'] not in known):
            raise ValueError('Edges must reference existing nodes')
        weight = edge.get('weight')
        try:
            valid = not isinstance(weight, bool) and isinstance(weight, (int, float)) and math.isfinite(weight)
        except OverflowError:
            valid = False
        if not valid:
            raise ValueError('Edge weights must be finite numbers')
        weights.append(abs(weight))
    try:
        if not math.isfinite(math.fsum(weights)):
            raise ValueError('Total edge weight is too large')
    except OverflowError:
        raise ValueError('Total edge weight is too large')
    # A disconnected input produces a minimum spanning forest.
    # Sort edges by weight
    sorted_edges = sorted(edges, key=lambda x: x['weight'])
    
    uf = UnionFind(nodes)
    mst_edges = []
    selected_edges = []
    rejected_edges = []
    total_weight = 0
    
    for edge in sorted_edges:
        u, v, w = edge['source'], edge['destination'], edge['weight']
        if uf.union(u, v):
            if trace is not None:
                trace.append(f'Add {u} — {v} ({w}): no cycle.')
            mst_edges.append(edge)
            selected_edges.append(edge)
            total_weight += w
        else:
            if trace is not None:
                trace.append(f'Skip {u} — {v} ({w}): creates a cycle.')
            rejected_edges.append(edge)
            
    return mst_edges, total_weight, selected_edges, rejected_edges
