import json
from pathlib import Path
from app import app


def test_demo_optimization():
    data = json.loads((Path(__file__).resolve().parents[1] / 'datasets/small_network.json').read_text())
    data.update(source='A', destination='D', budget=350000)
    with app.test_client() as client:
        assert client.get('/').status_code == 200
        assert client.get('/planner').status_code == 200
        assert client.get('/api/dataset/small_network').status_code == 200
        result = client.post('/api/optimize', json=data)
        assert result.status_code == 200
        body = result.get_json()
        assert body['route']['path'] == ['A', 'E', 'D']
        assert abs(body['route']['distance'] - 6.5) < 0.001
        assert body['stations']['total_cost'] <= data['budget']
        assert body['stations']['total_benefit'] == 155
        assert len(body['mst']['edges']) == 4


def test_invalid_inputs_and_unreachable_route():
    with app.test_client() as client:
        assert client.post('/api/optimize', json={}).status_code == 400
        assert client.post('/api/knapsack', json={'stations': [], 'budget': -1}).status_code == 400
        response = client.post('/api/dijkstra', json={'graph': {'a': {}, 'b': {}}, 'source': 'a', 'destination': 'b'})
        assert response.status_code == 200
        assert response.get_json()['distance'] is None
        assert client.get('/api/dataset/not_found').status_code == 404
