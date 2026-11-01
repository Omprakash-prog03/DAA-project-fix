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


def kruskal_mst(nodes, edges):
    """
    Manual Kruskal implementation
    Returns: mst_edges, total_weight, selected_edges, rejected_edges
    """
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
            mst_edges.append(edge)
            selected_edges.append(edge)
            total_weight += w
        else:
            rejected_edges.append(edge)
            
    return mst_edges, total_weight, selected_edges, rejected_edges
