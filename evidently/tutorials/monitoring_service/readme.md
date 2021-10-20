## Real-time ML monitoring with Evidently and Grafana

This example shows how to run a real-time Grafana dashboard to monitor Data Drift. You can adapt this example to your production use case by replacing the data source for your production service data. 

### How to run an example

In this example we use: 
* Bike Sharing Demand dataset to build a regression model
* Evidently to calculate the Data Drift metrics 
* Prometheus to store the metrics
* Grafana to build the Data Drift Dashboard

**Follow the instructions below to run the example**:

1. Clone the evidently repo using ```git clone git@github.com:evidentlyai/evidently.git``` command. 

*Make sure you have evidently version v0.1.27.dev0 or above.*

2. Download the data folder Bike-Sharing-Dataset.zip from the UCI repo: https://archive.ics.uci.edu/ml/machine-learning-databases/00275/ 

7. Unzip and place the data in the example directory in your file system: evidently/evidently/tutorials/monitoring_service 
8. Prepare the datasets:
- Go the example directory. In terminal, run the command ```cd evidently/tutorials/monitoring_service/``` 
- Run the python script ```prepare_datasets.py``` from the example directory (evidently/evidently/tutorials/monitoring_service) to prepare the datasets: ```python prepare_datasets.py``` 
- After the script is executed successfully, the two files should appear at the example directory: ```reference.csv``` and ```example.csv```.

*If you work in an empty environment, make sure you have the following Python packages installed: Sklearn, Numpy, Pandas, Requests.
You can install these packages using command ```pip install sklearn, numpy, pandas, requests```.*

5. Run the docker image from the example directory (evidently/evidently/tutorials/monitoring_service):```docker compose up``` . 

This will install Evidently package, Prometheus and Grafana. The three services will be running at your system: Evidently service at port 5000, Prometheus at port 9090, Grafana at port 3000.

- To access Prometheus web interface, go to your browser and open: localhost:9090
- To access Grafana web interface, go to your browser and open: localhost:3000 

There will be no data in the database and dashboard until you run the service, which is the next step.

6. Run the python script ```example_run_request.py``` to initiate the process of sending data to the evidently service: ```python example_run_request.py```

In this example each prediction is made with 10 seconds timeout. This is why at the very beginning no data will show at Grafana dashboard. It will start to appear in less than a minute.

7. Go to the browser and access the Grafana dashboard at localhost:3000. At first, you will be asked for login and password. Both are “admin”. 

8. To stop the execution, run ```docker compose down``` command.

### How to customize the Dashboard view (using the same source data)
The Dashboard view is determined by the json config. 
In our example the config for Data Drift Dashboard is stored in the monitoring_service/dashboards folder: https://github.com/evidentlyai/evidently/blob/main/evidently/tutorials/monitoring_service/dashboards/data_drift.json

To customize the Dashboard visual representation (but keeping the same metrics) you should:
1. Run the example, using the instrcutions from the above
2. Visit Grafana web interface (localhost:3000)
3. Customize the visuals in the Grafane interface
4. Apply your changes to the Dashboard and make sure you like it :)
5. Click the button "save" from the Grafana Top Menu. This will lead to the dialog window opennig. Select the option "Download Json" to save configurations in the json file.
6. Replace the initial configirations with the new one, meaning replce the old data_drift.json with the newly generated one.

### How to customize metrics to show in the Dashboard 

To calculate metrics for Dashboard we use ```Analyzers``` from Evidently:https://github.com/evidentlyai/evidently/blob/main/evidently/analyzers/. Particularly to calculate Data Drift metrics we use ```DataDriftAnalyzer```: https://github.com/evidentlyai/evidently/blob/main/evidently/analyzers/data_drift_analyzer.py

Depending on the changes you want to make there are several ways how you can customize metrics:
1. If you want to remove some metrics from the Dashboard, you can simply remove them by removing the corresponding visuals/metrics from Grafana interface
2. If you want to add or customize some metrics, you need to check the implemendation of the corresponding ```Analyzer``` and ```Monitor```:
- If the statistic you are interested in is calculated in the Analyzer, but not used in Monitor, you can add it there by updating the Monitor code
- If the statistic you are interested in is not calculated in the Analyzer, than you should start from adding the metric to Analyzed and than to Monitor

For example, to add something to DataDrift Dashbord: 
- check if the metric you are interested in is calculated in the ```DataDriftAnalyzer```: https://github.com/evidentlyai/evidently/blob/main/evidently/analyzers/data_drift_analyzer.py 
- if the metric is not implemented in ```Analyzer```, update the analyzer and add this metric to the ```result``` dictionary
- update ```metric``` method in ```DataDriftMonitor``` in order to yield new metric as wll
- visit Grafana web interface and create a visual Dashboard for new metric

### How to adopt the example to the custom ML service
To adopt the example for the custom service we recommend to copy the ```monitoring_service``` folder and rename in. Then you need to make the following steps in the new creadted directory:
1. Update ```config.yaml``` to let ```evidently``` know how to parse the data correctly. The config file contains the following parts:
- ```data_format``` - the format of the input data;
- ```column_mapping``` -  the information about the target, prediction names, lists of the numeric and categorical features. The format if similar to the column_mapping we use to calculate ```evidently``` interactive dashboards and profiles;
- ```service```:
  **reference_path** - path to the reference data
  **min_reference_size** - the minimal amount of objects in the reference dataset to start monitoring metrics calculation
  **use_reference** - should the service use the provided reference data or collect the reference from the data, that comes to the service (currently only ```true``` option is avaliable)
  **moving_reference** - should we move the reference in time during metrics calculation (currently only ```false``` option is avaliable)
  **window_size** - how much new objects should be collected in order to calculate new vaue for metrics
  **calculation_period_sec** - how often the monitoring service will check for new values of monitoring metrics
  **monitors** - the amould of monitors to use (currently only the ["data_drift"] option is avaliable)

2. Place the ```reference.csv``` inside the project folder (```monitoring_service``` in the initial example)

3.1 (option 1) If you do not have the running service, you can place the ```production.csv``` servcie in the project folder exactly as we did in the example. In this scenario your example will work exactly as the initial one: each **calculation_period_sec** service will take the next line from the production data to simu;ate the procuction service. 

3.2 (option 2) If you do have the running service, then you should update the ```app.py``` script to make the script use your service instead of the toy example. Update the ```iterate()``` method from ```@app.route('/iterate', methods=["POST"])``` to send the data from your service to the monitoring.

