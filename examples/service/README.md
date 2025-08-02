# Evidently UI Demo: Remote Project Example

This example demonstrates how to run an **Evidently UI service** and connect to it remotely to upload and monitor a demo project using Evidently's Python API.

---

## 📦 Contents

- `run_service.sh` — Script to start the Evidently UI service in Docker.
- `remote_demo_project.py` — Python script that uploads a demo bike rentals monitoring project to the running Evidently service.
- `workspace_tutorial.ipynb` — Jupyter notebook with Evidently UI API tutorial.
- `docker_s3_tutorial.ipynb` — A complete tutorial on how to use the Evidently UI official docker image with S3 and GCS.
- `README.md` — (this file) instructions on how to set up and run the example.

---

## 🚀 How to Run the Evidently UI Service

You have two options for running the Evidently UI service:

### 🔸 Option 1: Using Docker (recommended)

1. Make sure you have [Docker](https://www.docker.com/get-started) installed.
2. Run the service using the provided script:

```bash
bash run_service.sh
```

This will start the Evidently UI at:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 🔸 Option 2: Run Locally without Docker

Alternatively, you can start the Evidently UI service directly in your terminal (if Evidently is installed in your Python environment):

```bash
evidently ui
```

The service will be available at:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📊 Upload the Demo Project

Once the UI service is running, you can upload a demo project by running:

```bash
python remote_demo_project.py
```

This script will:

- Connect to the Evidently service at `http://127.0.0.1:8000`
- Create a sample project for bike rental monitoring
- Upload a few simulated data runs
- Add a dashboard panel to visualize metrics

You can then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to explore the project and its reports.

---

## 📚 More Information

For detailed documentation and configuration options, visit:  
[Evidently AI Documentation](https://docs.evidentlyai.com)

---

## ✅ Requirements

- Python 3.8+
- `evidently` Python package  
  Install it via:

```bash
pip install evidently
```

- (Optional) Docker, if using the Docker-based option.

---

Enjoy exploring your
