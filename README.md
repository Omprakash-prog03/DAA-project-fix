# EV Charging Station Placement and Route Planning System

## Project Overview
A Design and Analysis of Algorithms (DAA) academic project for 3rd Semester B.Tech CSE (Data Science) at NIST University.

## Students
- **Om Prakash Sahu** (Roll No: 202556339)
- **Prasant Nayak** (Roll No: 202556393)

## Institution
- **NIST University**, Berhampur, Odisha
- **Department**: Computer Science and Engineering
- **Programme**: B.Tech in Computer Science & Engineering (Data Science)
- **Academic Session**: 2026–27
- **Semester**: 3rd

## Faculty Guide
**Prof. __________________________**

## Core Algorithms
1. **Kruskal's Minimum Spanning Tree** (Manual implementation)
2. **0/1 Knapsack Dynamic Programming** (Manual implementation)
3. **Dijkstra's Shortest Path Algorithm** (Manual implementation)

## Architecture
- **Backend**: Python Flask
- **Frontend**: HTML/CSS/JavaScript (Professional Product-Grade UI/UX)
- **Visualization**: Leaflet/MapLibre (Interactive Map) + SVG/Canvas
- **Deployment**: Python web service using Gunicorn

## Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Run locally: `python app.py`

## Deploy to Railway

The repository includes `railway.json` with the build command, Gunicorn start command and `/health` health check. To deploy:

1. Push the branch containing `railway.json` to GitHub (or merge it into the branch you want to deploy).
2. In the Railway dashboard, create a project and choose **Deploy from GitHub repo**. Connect and select `Omprakash-prog03/DAA-project-fix`, then select the branch containing the configuration.
3. Deploy the service. Railway supplies `PORT`; do not set it manually. Generate a public domain under the service's networking settings.
4. Check the build and deployment logs, then visit the generated domain and its `/health` endpoint.

Railway account access and any applicable payment or plan setup are required. No live Railway deployment has been verified by this repository configuration alone. The homepage currently contains placeholder metrics and map; routes for pages without corresponding templates, such as `/planner`, are not ready. External API integrations are not implemented in the current backend.

## Datasets
- `datasets/small_network.json`
- `datasets/medium_network.json`
- `datasets/large_network.json`
- `datasets/india_demo.json`
- `datasets/bhubaneswar_demo.json`

## Report
The complete academic report (`EV_Charging_Station_Placement_and_Route_Planning_Report.pdf`) documents the implementation, algorithms, architecture, testing, and results following the NIST University reference design.

## License
Academic Project - NIST University
