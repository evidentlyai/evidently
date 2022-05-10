# Real-time ML monitoring with Evidently and Grafana

This example shows how to get real-time Grafana dashboards for monitoring data and model metrics with Evidently. 

## What's inside

We use two toy datasets and treat them as model application logs. Then, we configure Evidently `Monitors` to read the data from the logs at a certain interval (to simulate production service where data appears sequentially). Evidently calculates the metrics for Data Drift, Regression Performance and Classification Performance and sends them to Prometheus. The metrics are displayed on a pre-built Grafana dashboard.

Here is the one for Data Drift. And more inside!

![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/docs/images/evidently_data_drift_grafana_dashboard_top.png)

You can reproduce the example locally following the instructions below and choose one or more dashboards.

You can also adapt this example to your purposes by replacing the data source and the service settings. 

## How to run an example

In this example, we use: 
* `Bike Sharing Demand` (aka `bike`) - data for regression cases
* `kddcup99` - data for classification cases
* `Evidently` - library for the metrics calculations
* `Prometheus` - service to store the metrics
* `Grafana` - service to build the dashboards
* `Docker` - service to rule them all

Follow the instructions below to run the example:

1. **Install Docker** if you haven't used it before. 

2. **Create a new Python virtual environment and activate it**.
For example, for Linux/MacOS:
```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate 
```
3. **Get the `evidently` code example**:
```bash
git clone git@github.com:evidentlyai/evidently.git
```

4. **Install dependencies**.

- Go to the example directory:
```bash
cd evidently/examples/integrations/grafana_monitoring_service/
```
- install dependencies for the example run script
```bash
pip install -r requirements.txt
```

5. **Then run the docker image from the example directory**:
```bash
./run_example.py
```
This will:
- download and prepare the test data - `bike` and `kddcup99` on the first run.
- run Prometheus, Grafana, and Evidently monitoring service in Docker

The services will be available in your system: 
  - **Evidently monitoring service** at port 8085
  - **Prometheus** at port 9090. To access Prometheus web interface, go to your browser and open: http://localhost:9090/
  - **Grafana** at port 3000. To access Grafana web interface, go to your browser and open: http://localhost:3000/

- send the production data from the test datasets to the Evidently monitoring service (row by row)


6. **Explore the dashboard**.
 
Go to the browser and access the Grafana dashboard at http://localhost:3000. At first, you will be asked for login and password. Both are `admin`. 

To see the monitoring dashboard in the Grafana interface, click "General" and navigate to the chosen dashboard (e.g. "Evidently Data Drift").


7. **Stop the example**.

To stop the process of sending data, cancel the execution of the example script (press CTRL-C).

If the Docker containers were not stopped after that, run a command:

```bash
docker compose down
```

## How to customize the Grafana Dashboard view 

We rely on the **existing Grafana functionality** to visualize the metrics. We pre-built several dashboards to organize how metrics are displayed. You can use them as a starting point for Data Drift, Target Drift, Classification Performance or Regression Performance monitoring. 

The Grafana Dashboard view is determined by the JSON config. In our example, each config is stored in the examples/integrations/grafana_monitoring_service folder. For example, here is the one for the Data Drift Dashboard: https://github.com/evidentlyai/evidently/blob/main/examples/integrations/grafana_monitoring_service/dashboards/data_drift.json

If you want to continue using the same source data and metrics, but **change the way the plots are displayed** in the Grafana interface, take the following steps:

1. Run the example using the above instructions
2. Open the Grafana web interface (localhost:3000)
3. Customize the visuals in the Grafana interface. 
4. Apply your changes to the Dashboard and check that you like what you see :)
5. Click the button "save" from the Grafana Top Menu. This will open a dialog window. Select the option "Download JSON" to save the configurations in the JSON file.
6. Replace the initial configuration file (for example, data_drift.JSON) with the newly generated one.

You can refer to the [Grafana documentation](https://grafana.com/docs/grafana/latest/dashboards/) to learn more about UI customization.  

## How to customize which metrics are displayed in the Grafana Dashboard 

To **remove some metrics** from the Dashboard, you can simply do that from the Grafana interface following the steps above. 

To **add, or change** the way metrics are calculated (for example, use a different statistical test), you need to change the code.

We rely on the **core Evidently functionality** to define which metrics are calculated and how. If you want to modify the metrics, there are two components you might need to change: Analyzers and Monitors. 

To calculate the metrics and statistical tests, we use Evidently ```Analyzers```: https://github.com/evidentlyai/evidently/tree/main/src/evidently/analyzers 

For example, we use the ```DataDriftAnalyzer``` to calculate the Data Drift metrics: https://github.com/evidentlyai/evidently/blob/main/src/evidently/analyzers/data_drift_analyzer.py

There are corresponding Analyzers for other report types. Analyzers are shared components used across all Evidently interfaces. Depending on the report type, they might include a larger set of metrics than displayed on a Grafana dashboard. 

To define which exact metrics are computed during Monitoring and logged to Prometheus, we use Evidently ```Monitors```: https://github.com/evidentlyai/evidently/blob/main/src/evidently/model_monitoring/monitors/
 
For example, we use the ```DataDriftMonitor``` to define the Data Drift metrics collected from the live service: 
https://github.com/evidentlyai/evidently/blob/main/src/evidently/model_monitoring/monitors/data_drift.py

If you want to add or customize metrics, you need to check the implementation of the corresponding ```Analyzer``` and ```Monitor```:
- If the statistic you need **is calculated** in the Analyzer, but **not used** in Monitor, you can add it there by updating the Monitor code
- If the statistic you need **is not calculated** in the Analyzer, then you should first add the metric to the Analyzer and then to Monitor

For example, to add something to the Data Drift monitoring dashboard: 
- Check if the metric you need is calculated in the ```DataDriftAnalyzer```: https://github.com/evidentlyai/evidently/blob/main/src/evidently/analyzers/data_drift_analyzer.py
- If the metric is not implemented in ```Analyzer```, update the analyzer code and add this metric to the ```result``` dictionary
- Update the ```metric``` method in ```DataDriftMonitor``` in order to yield the new metric 
- Visit the Grafana web interface and create a visual Dashboard for a new metric

## How to adapt the example to work with your ML service

If you want to adapt this example to use with your ML service, you will need two more things:
- **Change the data source** for your live production data and reference data. For demo purposes, in this example we read the current data from the file. In production use, we suggest to POST the data directly from the ML service to the Evidently service. 
- **Configure Evidently monitoring parameters**. See the instructions below.

To adapt the example for a custom ML service, we recommend to copy the ```grafana_monitoring_service``` folder and rename it. 
Then, take the following steps in the newly created directory:

1. Update ```config.yaml``` to let ```evidently``` know how to parse the data correctly. The config file contains the following parts:
* ```data_format``` - the format of the input data;
* ```column_mapping``` -  the information about the target, prediction names, lists of the numerical and categorical features. The format is similar to the column_mapping we use to calculate ```evidently``` interactive dashboards and profiles;
* ```service```:
  * **reference_path** - path to the reference dataset
  * **use_reference** - define if to use the provided reference dataset ("true") or collect the reference from the production data stream ("false"). Currently, only ```true``` option is available.
  * **min_reference_size** - the minimal number of objects in the reference dataset to start calculating the monitoring metrics. If the reference dataset is provided externally, but has less objects than defined, the required number of objects will be collected from the production data and added to the reference.  
  * **moving_reference** - define if to move the reference in time during metrics calculation. Currently, only ```false``` option is available.
  * **window_size** - the number of the new objects in the current production data stream required to calculate the new monitoring metrics.
  * **calculation_period_sec** - how often the monitoring service will check for the new values of monitoring metrics.
  * **monitors** - the list of monitors to use. Currently, 6 monitors are is available: Data Drift, Categorical Target Drift, Numerical Target Drift, Regression Performance, Classification Performance, Probabilistic Classification Performance https://github.com/evidentlyai/evidently/blob/main/src/evidently/model_monitoring/monitors/

2. Place the ```reference.csv``` inside the project folder (```grafana_monitoring_service``` in the initial example)

3.1 (option 1) If you do not have a live service, you can place the ```production.csv``` file in the project folder exactly as we did in the example. In this scenario, your example will work exactly as the initial one: each **calculation_period_sec** the service will take the next line from the production data to simulate the production service. 

3.2 (option 2) If you do have a live service, then you should update the ```app.py``` script to make it use your service instead of the toy example. Update the ```iterate()``` method from ```@app.route('/iterate', methods=["POST"])``` to send the data from your service to the monitoring.

**Note**: the monitoring functionality is in active development and subject to API change. If you integrate Evidently Monitoring in your production pipeline, we suggest explicitly specifying the Evidently package version. Feel free to ping us on [Discord](https://discord.com/invite/xZjKRaNp8b) if you face any issues, and we'll help to figure them out.
