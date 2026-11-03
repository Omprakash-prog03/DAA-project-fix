from pathlib import Path
import json
import math
import os
from flask import Flask, jsonify, render_template, request
from algorithms.kruskal import kruskal_mst
from algorithms.dijkstra import dijkstra
from algorithms.knapsack import knapsack

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
DATASET = Path(__file__).resolve().parent / 'datasets' / 'small_network.json'

@app.get('/health')
def health():
    return jsonify(status='healthy')

@app.get('/')
@app.get('/planner')
def index():
    return render_template('index.html')

@app.get('/api/dataset/<name>')
def dataset(name):
    if name != 'small_network':
        return jsonify(error='Dataset not found'), 404
    with DATASET.open(encoding='utf-8') as f:
        return jsonify(json.load(f))

def payload():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError('A JSON object is required')
    return data

def finite_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False

def graph_data(data):
    nodes, edges = data.get('nodes'), data.get('edges')
    if not isinstance(nodes, list) or not nodes or not isinstance(edges, list):
        raise ValueError('Provide a non-empty nodes list and an edges list')
    ids = [n.get('id') if isinstance(n, dict) else n for n in nodes]
    if any(not isinstance(n, str) or not n for n in ids) or len(set(ids)) != len(ids):
        raise ValueError('Node IDs must be unique non-empty strings')
    graph = {n: {} for n in ids}
    for e in edges:
        if (not isinstance(e, dict) or not isinstance(e.get('source'), str)
                or not isinstance(e.get('destination'), str)
                or e['source'] not in graph or e['destination'] not in graph):
            raise ValueError('Edges must reference existing nodes')
        w = e.get('weight')
        if not finite_number(w) or w < 0:
            raise ValueError('Edge weights must be finite non-negative numbers')
        u, v = e['source'], e['destination']
        graph[u][v] = min(graph[u].get(v, w), w)
        graph[v][u] = min(graph[v].get(u, w), w)
    try:
        if not math.isfinite(math.fsum(e['weight'] for e in edges)):
            raise ValueError('Total edge weight is too large')
    except OverflowError:
        raise ValueError('Total edge weight is too large')
    return ids, edges, graph

@app.errorhandler(ValueError)
def invalid(error):
    return jsonify(error=str(error)), 400

@app.post('/api/optimize')
def optimize():
    data = payload()
    ids, edges, graph = graph_data(data)
    source, destination = data.get('source'), data.get('destination')
    if not isinstance(source, str) or not isinstance(destination, str) or source not in graph or destination not in graph:
        raise ValueError('Choose a valid start and destination')
    stations = data.get('stations')
    if not isinstance(stations, list) or any(not isinstance(s, dict) for s in stations):
        raise ValueError('Stations must be a list of objects')
    if any(not isinstance(s.get('node_id'), str) or s['node_id'] not in graph for s in stations):
        raise ValueError('Each station must reference an existing node')
    mst, weight, selected_edges, rejected_edges = kruskal_mst(ids, edges)
    selected, rejected, cost, benefit, remaining, _ = knapsack(stations, data.get('budget'))
    distance, path, predecessors, visited = dijkstra(graph, source, destination)
    return jsonify(network={'node_count': len(ids), 'edge_count': len(edges)},
        mst={'edges': mst, 'weight': weight, 'selected': len(selected_edges), 'rejected': len(rejected_edges), 'connected': len(mst) == len(ids) - 1, 'components': len(ids) - len(mst)},
        stations={'selected': selected, 'rejected': rejected, 'total_cost': cost, 'total_benefit': benefit, 'remaining_budget': remaining},
        route={'distance': distance if math.isfinite(distance) else None, 'path': path, 'predecessors': predecessors, 'visited_order': visited})

@app.post('/api/kruskal')
def api_kruskal():
    ids, edges, _ = graph_data(payload())
    mst, total, selected, rejected = kruskal_mst(ids, edges)
    return jsonify(mst_edges=mst, total_weight=total, selected_edges=selected, rejected_edges=rejected, connected=len(mst) == len(ids) - 1, components=len(ids) - len(mst))

@app.post('/api/knapsack')
def api_knapsack():
    data = payload()
    stations = data.get('stations')
    if not isinstance(stations, list) or any(not isinstance(s, dict) for s in stations):
        raise ValueError('Stations must be a list of objects')
    selected, rejected, cost, benefit, remaining, _ = knapsack(stations, data.get('budget'))
    return jsonify(selected_stations=selected, rejected_stations=rejected, total_cost=cost, total_benefit=benefit, remaining_budget=remaining)

@app.post('/api/dijkstra')
def api_dijkstra():
    data = payload()
    graph = data.get('graph')
    if (not isinstance(graph, dict) or not isinstance(data.get('source'), str)
            or not isinstance(data.get('destination'), str) or data['source'] not in graph
            or data['destination'] not in graph):
        raise ValueError('Provide a graph and valid source and destination')
    edges = []
    for u, neighbors in graph.items():
        if not isinstance(neighbors, dict):
            raise ValueError('Graph neighbors must be objects')
        for v, w in neighbors.items():
            edges.append({'source': u, 'destination': v, 'weight': w})
    # Validate without changing directed graph semantics.
    graph_data({'nodes': list(graph), 'edges': edges})
    distance, path, predecessors, visited = dijkstra(graph, data['source'], data['destination'])
    return jsonify(distance=distance if math.isfinite(distance) else None, path=path, predecessors=predecessors, visited_order=visited)

# Teaching endpoints use one fixed dataset, so students can trace each result by hand.
def teaching_data():
    path = Path(__file__).resolve().parent / 'datasets' / 'teaching_graph.json'
    with path.open(encoding='utf-8') as file:
        return json.load(file)

@app.get('/api/demo')
def demo_data():
    return jsonify(teaching_data())

@app.post('/api/demo/dijkstra')
def demo_dijkstra():
    data = payload()
    demo = teaching_data()
    _, _, graph = graph_data(demo)
    trace = []
    distance, path, _, visited = dijkstra(graph, data.get('source'), data.get('destination'), trace)
    return jsonify(path=path, distance=distance if math.isfinite(distance) else None,
                   visited=visited, steps=trace)

@app.post('/api/demo/kruskal')
def demo_kruskal():
    demo = teaching_data()
    nodes, edges, _ = graph_data(demo)
    trace = []
    selected, total, _, _ = kruskal_mst(nodes, edges, trace)
    return jsonify(edges=selected, total=total, steps=trace)

@app.post('/api/demo/knapsack')
def demo_knapsack():
    from functools import reduce
    from math import gcd
    data = payload()
    candidates = teaching_data()['stations']
    chosen_ids = data.get('station_ids', [s['station_id'] for s in candidates])
    if not isinstance(chosen_ids, list) or any(not isinstance(i, str) for i in chosen_ids):
        raise ValueError('Station IDs must be a list of strings')
    if len(set(chosen_ids)) != len(chosen_ids) or any(i not in {s['station_id'] for s in candidates} for i in chosen_ids):
        raise ValueError('Station IDs must be unique and present in the demo')
    stations = [s for s in candidates if s['station_id'] in chosen_ids]
    budget = data.get('budget')
    selected, _, cost, benefit, remaining, table = knapsack(stations, budget)
    # Each DP column represents one greatest-common-divisor unit of rupees.
    unit = reduce(gcd, (station['installation_cost'] for station in stations), 0) or 1
    return jsonify(selected=selected, cost=cost, benefit=benefit, remaining=remaining,
                   unit=unit, table=table, candidates=[s['station_id'] for s in stations])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
