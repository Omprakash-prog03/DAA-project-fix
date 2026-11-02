# EV Grid — Charging Station and Route Planner

A Flask demo for NIST University students Om Prakash Sahu and Prasant Nayak. It uses a small fictional Bhubaneswar dataset to demonstrate manual Kruskal, Dijkstra, and 0/1 knapsack algorithms. The network diagram is schematic, not a live map; external data APIs are not currently integrated and the results are not real-world recommendations.

## Run locally

Install Python 3.9 or newer and Git. In a terminal:

```sh
git clone https://github.com/Omprakash-prog03/DAA-project-fix.git
cd DAA-project-fix
python -m venv .venv
```

On macOS/Linux, use `python3` instead of `python` if necessary. Activate the environment:

- Windows PowerShell: `.venv\Scripts\Activate.ps1` (if blocked, use Command Prompt instead).
- Windows Command Prompt: `.venv\Scripts\activate.bat`
- macOS/Linux: `source .venv/bin/activate`

Then run:

```sh
python -m pip install -r requirements.txt
python app.py
```

Open **http://localhost:5000** in your browser. Choose locations and a budget, then click **Run optimization**. Press Ctrl+C to stop the server. If port 5000 is already occupied, stop the other application or set the `PORT` environment variable before running the app. Always run commands from the project directory.

If you cloned an older version of the repository, fetch the latest changes or check out the branch containing these fixes. For example: `git fetch origin` followed by `git checkout arena/fb2b6ade-daa-project-fix` once that branch has been pushed.

## Tests

With the virtual environment activated, run `python -m pytest -q`.

## Implementation

- `app.py`: Flask routes and input validation.
- `algorithms/`: manual Union-Find Kruskal, heap-based Dijkstra and exact 0/1 knapsack dynamic programming.
- `datasets/small_network.json`: bundled demo network and candidate stations.
- `templates/` and `static/`: interactive offline planner.
- `tests/`: algorithm and application smoke tests.

The academic report in the repository predates these fixes and should be checked against the current implementation before submission.
