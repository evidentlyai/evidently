---
description: Overview of the available Evidently integrations.
---

Evidently is a Python library, and can be easily integrated with other tools to fit into the existing workflows.

Below are a few specific examples of how to integrate Evidently with other tools in the ML lifecycle. You can adapt them for other workflow management, visualization, tracking and other tools.

| Tool | Description | Guide or example |
|---|---|---|
| Notebook environments (Jupyter, Colab, etc.) | Render visual Evidently Reports and Test Suites. | [Docs](notebook-environments.md)<br>[Code examples](../examples/examples.md) |
| Streamlit | Create a web app with Evidently Reports.  | [Tutorial](https://www.evidentlyai.com/blog/ml-model-monitoring-dashboard-tutorial)<br> [Code example](https://github.com/evidentlyai/evidently/tree/main/examples/integrations/streamlit_dashboard)|
| MLflow | Log metrics calculated by Evidently to MLflow. | [Docs](evidently-and-mlflow.md)<br>[Code example](https://github.com/evidentlyai/evidently/blob/main/examples/integrations/mlflow_logging/mlflow_integration.ipynb) |
| Airflow | Run data and ML model checks as part of an Airflow DAG. | [Docs](evidently-and-airflow.md)<br>[Code example](https://github.com/evidentlyai/evidently/tree/main/examples/integrations/airflow_drift_detection) |
| Metaflow | Run data and ML model checks as part of a Metaflow Flow. | [Docs](evidently-and-metaflow.md) |
| FastAPI + PostgreSQL| Generate on-demand Reports for models deployed with FastAPI.  | [Tutorial](https://www.evidentlyai.com/blog/fastapi-tutorial)<br>[Code example](https://github.com/evidentlyai/evidently/tree/main/examples/integrations/fastapi_monitoring) |
| Grafana + PostgreSQL + Prefect | Run ML monitoring jobs with Prefect and visualize metrics in Grafana.  | [Tutorial](https://www.evidentlyai.com/blog/batch-ml-monitoring-architecture)<br>[Code example](https://github.com/evidentlyai/evidently/tree/main/examples/integrations/postgres_grafana_batch_monitoring/) |
| AWS SES | Send email alerts with attached Evidently Reports (Community contribution). | [Tutorial](https://www.evidentlyai.com/blog/ml-monitoring-with-email-alerts-tutorial)<br>[Code example](https://github.com/evidentlyai/aws_alerting)
| Grafana | Real-time ML monitoring with Grafana. (Old API, not currently supported). | [Code example](https://github.com/evidentlyai/evidently/tree/main/examples/integrations/grafana_monitoring_service) |
