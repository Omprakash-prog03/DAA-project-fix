import unittest
from algorithms.kruskal import kruskal_mst
from algorithms.dijkstra import dijkstra
from algorithms.knapsack import knapsack

class TestDAAAlgorithms(unittest.TestCase):
    
    def test_kruskal_simple(self):
        nodes = ['A', 'B', 'C']
        edges = [
            {'source': 'A', 'destination': 'B', 'weight': 2},
            {'source': 'B', 'destination': 'C', 'weight': 3},
            {'source': 'A', 'destination': 'C', 'weight': 5}
        ]
        mst, weight, selected, rejected = kruskal_mst(nodes, edges)
        self.assertEqual(weight, 5)
        self.assertEqual(len(selected), 2)
        self.assertEqual(len(rejected), 1)

    def test_dijkstra_simple(self):
        graph = {
            'A': {'B': 4, 'C': 6},
            'B': {'A': 4, 'C': 2, 'D': 5},
            'C': {'A': 6, 'B': 2, 'D': 3},
            'D': {'B': 5, 'C': 3}
        }
        dist, path, preds, visited = dijkstra(graph, 'A', 'D')
        # Path A -> B -> D is 4 + 5 = 9
        # Path A -> B -> C -> D is 4 + 2 + 3 = 9
        # Both are valid shortest paths. Dijkstra returns the first one found.
        self.assertEqual(dist, 9)
        self.assertIn(path, [['A', 'B', 'D'], ['A', 'B', 'C', 'D']])

    def test_knapsack_simple(self):
        stations = [
            {'station_id': 'S1', 'installation_cost': 20, 'benefit': 80},
            {'station_id': 'S2', 'installation_cost': 15, 'benefit': 60},
            {'station_id': 'S3', 'installation_cost': 25, 'benefit': 100}
        ]
        budget = 40
        selected, rejected, cost, benefit, remaining, dp = knapsack(stations, budget)
        # S2 (15, 60) + S3 (25, 100) = 40 cost, 160 benefit
        self.assertEqual(cost, 40)
        self.assertEqual(benefit, 160)
        self.assertEqual(remaining, 0)

if __name__ == '__main__':
    unittest.main()
