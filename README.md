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

## Deploy to Google Cloud Run

The included Dockerfile starts Gunicorn on the port supplied by Cloud Run. Deployment requires a Google Cloud project with billing enabled, the Google Cloud CLI, and permissions to build and deploy. Charges may apply.

From a checkout containing the Dockerfile, authenticate using `gcloud auth login`, select your project with `gcloud config set project PROJECT_ID`, and enable the required services:

```sh
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
gcloud run deploy ev-grid-optimizer --source . --region asia-south1 --allow-unauthenticated
```

The last command creates a publicly accessible service and builds the Dockerfile using Cloud Build. Follow any CLI prompts, then open the service URL printed by the command and check `/health`. Do not commit credentials or secrets. Consult the Cloud Run logs if the build or health check fails.

No live Cloud Run deployment has been verified by this repository configuration alone. The homepage currently contains placeholder metrics and map; routes for pages without corresponding templates, such as `/planner`, are not ready. External API integrations are not implemented in the current backend.

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
