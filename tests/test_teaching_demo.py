from app import app


def test_fixed_graph_and_shortest_path():
    with app.test_client() as client:
        demo = client.get('/api/demo').get_json()
        assert [node['id'] for node in demo['nodes']] == list('ABCDE')
        response = client.post('/api/demo/dijkstra', json={'source': 'A', 'destination': 'E'})
        assert response.status_code == 200
        result = response.get_json()
        assert result['path'] == ['A', 'C', 'E']
        assert result['distance'] == 10
        assert result['visited'] == ['A', 'C', 'B', 'D', 'E']
        assert any('Relax' in step for step in result['steps'])
        same = client.post('/api/demo/dijkstra', json={'source': 'A', 'destination': 'A'}).get_json()
        assert (same['path'], same['distance']) == (['A'], 0)
        assert client.post('/api/demo/dijkstra', json={'source': 'X', 'destination': 'E'}).status_code == 400


def test_fixed_graph_mst():
    with app.test_client() as client:
        result = client.post('/api/demo/kruskal', json={}).get_json()
        assert [(e['source'], e['destination'], e['weight']) for e in result['edges']] == [
            ('B', 'C', 1), ('A', 'C', 2), ('D', 'E', 3), ('B', 'D', 5)]
        assert result['total'] == 11
        assert len(result['steps']) == 6
        assert any('cycle' in step and 'Skip' in step for step in result['steps'])


def test_budget_station_candidates_and_dp_table():
    with app.test_client() as client:
        response = client.post('/api/demo/knapsack', json={'budget': 100000})
        assert response.status_code == 200
        result = response.get_json()
        assert result['cost'] <= 100000
        assert (result['cost'], result['benefit'], result['remaining']) == (100000, 200, 0)
        assert len({s['station_id'] for s in result['selected']}) == len(result['selected'])
        assert result['unit'] == 10000
        assert result['table'][-1][-1] == result['benefit']
        subset = client.post('/api/demo/knapsack', json={'budget': 40000, 'station_ids': ['B', 'D']}).get_json()
        assert subset['cost'] == 30000 and subset['benefit'] == 60
        empty = client.post('/api/demo/knapsack', json={'budget': 0, 'station_ids': []}).get_json()
        assert empty['selected'] == [] and empty['table'] == [[0]]
        assert client.post('/api/demo/knapsack', json={'budget': -1}).status_code == 400
        assert client.post('/api/demo/knapsack', json={'budget': 1, 'station_ids': ['A', 'A']}).status_code == 400
