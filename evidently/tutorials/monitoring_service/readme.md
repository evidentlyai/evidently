This is the instruction to run an example of Data Drift Monitoring for Bikes Demand Precision. 
In this example we use: 
- Bike Sharing Demand dataset to build a regression model
- Evidently to calculate Data Drift Metrics 
- Prometheus to store the metrics
- Grafana to build Data Drift Dashboard

Follow the instructions below to run the example:

1. Clone the evidently repo using ```git clone git@github.com:evidentlyai/evidently.git``` command. Make sure you have evidently version not earlier than v0.1.27.dev0
2. Download the data folder Bike-Sharing-Dataset.zip from the USI repo: https://archive.ics.uci.edu/ml/machine-learning-databases/00275/ 
3. Unzip data folder and place in inside the example directory in your filesystem:  evidently/evidently/tutorials/monitoring_service 
4. Go the example directory (in terminal run the command ```cd evidently/tutorials/monitoring_service/```). Run python script ```prepare_datasets.py``` from example directory (evidently/evidently/tutorials/monitoring_service) to prepare datasets: ```python prepare_datasets.py``` After successful script execution 2 files should appear at the example directory: ```reference.csv``` and ```example.csv```.

*If you are working in an empty environment make sure you have the following python packages installed:
- Sklearn
- Numpy
- Pandas
- Requests
You can install these packages using command ```pip install sklearn, numpy, pandas, requests```

5. Run docker image from the example directory evidently/evidently/tutorials/monitoring_service:```docker compose up``` . This will lead to the installation of evidently package, Prometheus and Grafana. Three services will be running at your system:
- Evidently service at port 5000
- Prometheus at port 9090
- Grafana at port 3000
To access Prometheus  web interface go to your browser and open: localhost:9090
To access Grafana web interface go to your browser and open: localhost:3000 
There will be no data in the database and dashboard until you run the service, with is the next step.
6. Run python script ```example_run_request.py``` to initiate the process of data sending to the evidently service: ```python example_run_request.py```
Note, that we implemented an example in a way, that each prediction is made with 10 seconds timeout. This is why at the very beginning there will be no data at Grafana dashboard. But after less that a minute you will see some data in the dashboard.
7. Go to the browser and access the Grafana dashboard: localhost:3000  At the first time you will be asked for login and password. Both are “admin”. 
8. To stop the execution run ```docker compose down``` command.
