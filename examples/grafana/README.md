# Grafana 

This folder contains examples of using Evidently metrics with Grafana dashboards.

These examples show how to export Evidently metrics and visualize them in Grafana using a local setup.

## Available examples

| Example | Description |
|--------|------------|
| [`grafana_data_drift_dashboard`](./grafana_data_drift_dashboard/) | Monitor data drift metrics in a Grafana dashboard |
| [`grafana_llm_evaluation_dashboard`](./grafana_llm_evaluation_dashboard/) | Monitor LLM evaluation metrics in a Grafana dashboard |

Each example includes:
- Docker Compose setup,
- preconfigured Grafana dashboards,
- scripts for computing and exporting Evidently metrics.

## When to use these examples

Use these examples if you want to:

- visualize Evidently metrics in Grafana,
- build custom monitoring dashboards,
- integrate Evidently into an existing observability stack.

For built-in visualization and full local setup, see the [`service`](../service/) example.
