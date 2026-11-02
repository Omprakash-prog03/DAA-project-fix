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


def test_dijkstra_checks_unvisited_edges_and_same_node():
    import pytest
    graph = {'A': {'B': 1}, 'B': {}, 'C': {'B': -1}}
    with pytest.raises(ValueError):
        dijkstra(graph, 'A', 'B')
    assert dijkstra({'A': {}}, 'A', 'A')[:2] == (0, ['A'])
    with pytest.raises(ValueError):
        dijkstra({'A': {'B': 1}}, 'A', 'A')


def test_knapsack_zero_cost_and_nondivisible_budget():
    stations = [{'installation_cost': 0, 'benefit': 2},
                {'installation_cost': 6, 'benefit': 5},
                {'installation_cost': 10, 'benefit': 6}]
    selected, _, cost, benefit, remaining, _ = knapsack(stations, 11)
    assert (cost, benefit, remaining) == (10, 8, 1)
    assert len(selected) == 2


def test_knapsack_matches_exhaustive_search():
    import random
    from itertools import combinations
    rng = random.Random(121)
    for _ in range(100):
        stations = [{'installation_cost': rng.randrange(0, 15), 'benefit': rng.randrange(0, 20)} for _ in range(6)]
        budget = rng.randrange(0, 35)
        *_, benefit, remaining, table = knapsack(stations, budget)
        expected = max(sum(s['benefit'] for s in subset) for n in range(7)
                       for subset in combinations(stations, n)
                       if sum(s['installation_cost'] for s in subset) <= budget)
        assert benefit == expected
        assert remaining >= 0


def test_dijkstra_against_floyd_warshall():
    import random
    rng = random.Random(41)
    nodes = [str(i) for i in range(6)]
    for _ in range(30):
        graph = {a: {b: rng.randrange(0, 20) for b in nodes if a != b and rng.random() < .35} for a in nodes}
        distances = {(a, b): (0 if a == b else graph[a].get(b, float('inf'))) for a in nodes for b in nodes}
        for k in nodes:
            for i in nodes:
                for j in nodes:
                    distances[i, j] = min(distances[i, j], distances[i, k] + distances[k, j])
        for a in nodes:
            for b in nodes:
                distance, path, _, _ = dijkstra(graph, a, b)
                assert distance == distances[a, b]
                if path:
                    assert path[0] == a and path[-1] == b
                    assert sum(graph[x][y] for x, y in zip(path, path[1:])) == distance


def test_kruskal_forest_parallel_edges_and_negative_weights():
    nodes = ['a', 'b', 'c', 'isolated']
    edges = [{'source': 'a', 'destination': 'b', 'weight': 9},
             {'source': 'a', 'destination': 'b', 'weight': -2},
             {'source': 'b', 'destination': 'c', 'weight': 3},
             {'source': 'a', 'destination': 'c', 'weight': 7},
             {'source': 'a', 'destination': 'a', 'weight': -10}]
    mst, weight, chosen, rejected = kruskal_mst(nodes, edges)
    assert weight == 1 and len(mst) == 2 and len(rejected) == 3
