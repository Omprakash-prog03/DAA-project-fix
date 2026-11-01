from flask import Flask, render_template, request, jsonify
from algorithms.kruskal import kruskal_mst
from algorithms.dijkstra import dijkstra
from algorithms.knapsack import knapsack
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load datasets
def load_dataset(name):
    path = os.path.join('datasets', f'{name}.json')
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return None

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "version": "1.0.0", "environment": os.environ.get('FLASK_ENV', 'development')})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/planner')
def planner():
    return render_template('planner.html')

@app.route('/algorithms')
def algorithms():
    return render_template('algorithms.html')

@app.route('/datasets')
def datasets():
    return render_template('datasets.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/dataset/<dataset_name>', methods=['GET'])
def get_dataset(dataset_name):
    data = load_dataset(dataset_name)
    if data:
        return jsonify(data)
    return jsonify({"error": "Dataset not found"}), 404

@app.route('/api/kruskal', methods=['POST'])
def api_kruskal():
    data = request.json
    nodes = data.get('nodes', [])
    edges = data.get('edges', [])
    mst_edges, total_weight, selected, rejected = kruskal_mst(nodes, edges)
    return jsonify({
        "mst_edges": mst_edges,
        "total_weight": total_weight,
        "selected_edges": selected,
        "rejected_edges": rejected
    })

@app.route('/api/knapsack', methods=['POST'])
def api_knapsack():
    data = request.json
    stations = data.get('stations', [])
    budget = data.get('budget', 0)
    selected, rejected, total_cost, total_benefit, remaining, dp = knapsack(stations, budget)
    return jsonify({
        "selected_stations": selected,
        "rejected_stations": rejected,
        "total_cost": total_cost,
        "total_benefit": total_benefit,
        "remaining_budget": remaining
    })

@app.route('/api/dijkstra', methods=['POST'])
def api_dijkstra():
    data = request.json
    graph = data.get('graph', {})
    source = data.get('source')
    destination = data.get('destination')
    try:
        distance, path, predecessors, visited = dijkstra(graph, source, destination)
        return jsonify({
            "distance": distance,
            "path": path,
            "predecessors": predecessors,
            "visited_order": visited
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/optimize', methods=['POST'])
def api_optimize():
    data = request.json
    nodes = data.get('nodes', [])
    edges = data.get('edges', [])
    stations = data.get('stations', [])
    budget = data.get('budget', 0)
    source = data.get('source')
    destination = data.get('destination')
    
    # 1. Kruskal MST
    mst_edges, mst_weight, selected_edges, rejected_edges = kruskal_mst(nodes, edges)
    
    # 2. Knapsack
    sel_stations, rej_stations, total_cost, total_benefit, remaining, dp = knapsack(stations, budget)
    
    # 3. Dijkstra
    # Build adjacency list for Dijkstra
    graph = {node['id']: {} for node in nodes}
    for edge in edges:
        u, v, w = edge['source'], edge['destination'], edge['weight']
        graph[u][v] = w
        graph[v][u] = w  # Assuming undirected
        
    try:
        dist, path, preds, visited = dijkstra(graph, source, destination)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
        
    return jsonify({
        "network": {
            "node_count": len(nodes),
            "edge_count": len(edges)
        },
        "mst": {
            "edges": mst_edges,
            "weight": mst_weight,
            "selected": len(selected_edges),
            "rejected": len(rejected_edges)
        },
        "stations": {
            "selected": sel_stations,
            "rejected": rej_stations,
            "total_cost": total_cost,
            "total_benefit": total_benefit,
            "remaining_budget": remaining
        },
        "route": {
            "distance": dist,
            "path": path,
            "hops": len(path) - 1 if path else 0,
            "predecessors": preds,
            "visited_order": visited
        },
        "recommendation": "Optimization complete based on DAA algorithms."
    })

if __name__ == '__main__':
    # Production configuration: use environment variables, disable debug
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
