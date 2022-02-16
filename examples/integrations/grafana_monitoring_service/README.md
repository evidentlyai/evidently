## Real-time ML monitoring with Evidently and Grafana

This example shows how to get real-time Grafana dashboards for monitoring data metrics with Evidently. 

You can adapt this example to your purposes by replacing the data source and the service settings. 

### How to run an example

In this example, we use: 
* `Bike Sharing Demand` dataset for regression cases
* `kddcup99` dataset for classification cases
* `Evidently` library for the metrics calculations
* `Prometheus` to store the metrics
* `Grafana` to build the Data Drift Dashboard
* `Docker` to rule them all

**Follow the instructions below to run the example**:
1. Create a new python virtual environment and activate it
2. Get the `evidently` code example:
 ```bash
git clone git@github.com:evidentlyai/evidently.git
```
3. Prepare the datasets:
- Go to the example directory:
```bash
cd evidently/examples/integrations/grafana_monitoring_service/
```
- install dependencies for the data preparation script
```bash
pip install -r requirements.txt
```
- Run the data preparation script `prepare_datasets.py` from the example directory 
  - specify a dataset name with `--dataset` or `-d` option  
  - use `bike` if you want to get data for `data_drift` and `regression_performance`
  - use `kddcup99` if you want to get data for `classification_performance`
  - the script will use `bike` as a default
```
prepare_datasets.py --dataset kddcup99
```
- After the script is executed successfully, the three files should appear in the directory: 
  - `config.yaml` - a config for the metrics service
  - `reference.csv` - a file with reference data
  - `production.csv` - a file with current or production data that we will send to the service later
The data is ready.
4. Then run the docker image from the example directory:
```bash
docker compose up -d
```

This will run three services: Prometheus, Grafana, and the monitoring service.

The services will be available in your system: 
  - Evidently monitoring service at port 5000
  - Prometheus at port 9090. To access Prometheus web interface, go to your browser and open: http://localhost:9090/
  - Grafana at port 3000. To access Grafana web interface, go to your browser and open: http://localhost:3000/
 

There will be no data in the database and dashboard until you start to send a production data.

Let's do it is the next step.

5. Run the python script `example_run_request.py` to initiate the process of sending a data to the evidently service:
```bash
python example_run_request.py
```

In this example each row is sent with 10 seconds timeout. This is why at the very beginning no data will show at Grafana dashboard. It will start to appear in less than a minute.

6. Go to the browser and access the Grafana dashboard at http://localhost:3000. At first, you will be asked for login and password. Both are `admin`. 

7. To stop the execution, run ```docker compose down``` command.

### How to customize the Grafana Dashboard view 

The Grafana Dashboard view is determined by the JSON config. In our example, the config for a Data Drift Dashboard is stored in the examples/integrations/grafana_monitoring_service folder: https://github.com/evidentlyai/evidently/blob/main/examples/integrations/grafana_monitoring_service/dashboards/data_drift.json

If you want to continue using the same source data and metrics, but **change the way the plots are displayed** in the Garafana interface, take the following steps:

1. Run the example using the above instructions
2. Open the Grafana web interface (localhost:3000)
3. Customize the visuals in the Grafana interface. 
4. Apply your changes to the Dashboard and check that you like what you see :)
5. Click the button "save" from the Grafana Top Menu. This will open a dialog window. Select the option "Download JSON" to save the configurations in the JSON file.
6. Replace the initial configiration file (data_drift.JSON) with the newly generated one.

You can refer to the Grafana documentation to learn more about UI customization.  

### How to customize metrics displayed in the Grafana Dashboard 

To **remove some metrics** from the Dashboard, you can simply do that from the Grafana interface following the steps above. 

To **add, or change** the way metrics are calculated (for example, use a different statistical test), you need to change the code.

To calculate the metrics we use Evidently ```Analyzers```: https://github.com/evidentlyai/evidently/tree/main/src/evidently/analyzers 

For example, we use the ```DataDriftAnalyzer``` to calculate the Data Drift metrics: https://github.com/evidentlyai/evidently/blob/main/src/evidently/analyzers/data_drift_analyzer.py

If you want to add or customize metrics, you need to check the implemendation of the corresponding ```Analyzer``` and ```Monitor```:
- If the statistic you need **is calculated** in the Analyzer, but **not used** in Monitor, you can add it there by updating the Monitor code
- If the statistic you need **is not calculated** in the Analyzer, than you should first add the metric to the Analyzer and than to Monitor

For example, to add something to the Data Drift Dashboard: 
- Check if the metric you need is calculated in the ```DataDriftAnalyzer```: https://github.com/evidentlyai/evidently/blob/main/src/evidently/analyzers/data_drift_analyzer.py
- If the metric is not implemented in ```Analyzer```, update the analyzer code and add this metric to the ```result``` dictionary
- Update the ```metric``` method in ```DataDriftMonitor``` in order to yield the new metric 
- Visit the Grafana web interface and create a visual Dashboard for a new metric

### How to adapt the example to work with your ML service

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
  * **monitors** - the number of monitors to use. Currently, only the ["data_drift"] option is available.

2. Place the ```reference.csv``` inside the project folder (```grafana_monitoring_service``` in the initial example)

3.1 (option 1) If you do not have a live service, you can place the ```production.csv``` file in the project folder exactly as we did in the example. In this scenario, your example will work exactly as the initial one: each **calculation_period_sec** the service will take the next line from the production data to simulate the production service. 

3.2 (option 2) If you do have a live service, then you should update the ```app.py``` script to make it use your service instead of the toy example. Update the ```iterate()``` method from ```@app.route('/iterate', methods=["POST"])``` to send the data from your service to the monitoring.

