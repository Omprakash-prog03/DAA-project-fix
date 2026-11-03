# EV Charging Station Placement and Route Planning using DAA

An educational Flask application for understanding how three algorithms relate to an EV infrastructure planning problem. It uses a small, fixed, fictional graph and does not need maps, API keys, a database or an internet connection after installation.

## Run locally

Install Python 3.9 or newer, then open a terminal in this project folder:

```sh
python -m venv .venv
```

Activate the environment:

- **Windows PowerShell:** `.venv\Scripts\Activate.ps1`
- **Windows Command Prompt:** `.venv\Scripts\activate.bat`
- **macOS / Linux:** `source .venv/bin/activate`

On macOS/Linux, use `python3` if `python` is unavailable. Then install and run:

```sh
python -m pip install -r requirements.txt
python app.py
```

Open **http://localhost:5000**. Press Ctrl+C in the terminal to stop. If port 5000 is occupied, stop the other app or choose a different port with the `PORT` environment variable.

If you cloned the repository, check out the branch containing these changes before running it; they may not yet be on `main`.

## The demonstration

1. **Graph:** Five locations A–E and six weighted, undirected roads, in `datasets/teaching_graph.json`.
2. **Dijkstra:** Select a start and destination. For A to E, the path is A → C → E with distance **10**. The min-heap chooses the next closest unvisited location and the app shows actual relaxation steps. Code: `algorithms/dijkstra.py`.
3. **Kruskal:** Sort roads by weight, using Union-Find to skip cycles. The fixed graph's MST has total cost **11**. Code: `algorithms/kruskal.py`.
4. **0/1 knapsack:** Check the station candidates and enter a budget. For ₹100,000 with all candidates, the maximum benefit is **200**, at a cost of ₹100,000. Multiple optimal combinations are possible. The DP table and selected combination are displayed. Code: `algorithms/knapsack.py`.

The graph provides context for all three calculations, but they are **independent demonstrations**: Dijkstra uses the original roads, not only the MST; station selection maximizes the provided benefit values and does not guarantee route coverage or charging feasibility. Values are illustrative, not real-world recommendations.

Knapsack costs are divided by their greatest common divisor before building the DP table. This preserves exact results while keeping the table small. A budget not divisible by that unit is rounded down only for the table capacity; costs and the remaining budget are still reported in rupees.

## Tests

With the virtual environment activated, run:

```sh
python -m pytest -q
```

The academic report predates this simplified version; check it against the current implementation before submission. Deployment configuration and the previous dataset are retained but are not needed for this demonstration.
