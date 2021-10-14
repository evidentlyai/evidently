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
