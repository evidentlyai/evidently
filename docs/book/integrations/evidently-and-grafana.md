---
description: Create live dashboards for real-time ML monitoring.
---

# Evidently + Grafana

Grafana is an open-source [data visualization platform](https://github.com/grafana/grafana). It is frequently used with the Prometheus [time series database](https://github.com/prometheus/prometheus) to monitor software system performance.

You can use this same stack for ML monitoring. In this case, Evidently provides a metrics calculation layer that can be easily configured for your use case.&#x20;

**An integration example is available as a Docker container:**
{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/integrations/grafana_monitoring_service" %}

Follow the readme to install and modify the example.&#x20;

It contains pre-built dashboards to display Evidently reports in the Grafana interface.

### 1. Data Drift Dashboard

![](../.gitbook/assets/grafana\_dashboard.jpg)

We plan to add more pre-built dashboards in the future.
