1. Install Docker [https://docs.docker.com/get-docker/] to your system. You are going to use it to install and run the example.
2. Go to the project directory and run the following command from the terminal: docker-compose up --build 
Note:
* to stop the docker later, run:  docker-compose down; 
* to rebuild docker image (for example, to get the latest version of the libraries) run:  docker compose build --no-cache)
3. Open the Airflow user interface in your browser. It will be at the localhost:8080 address.
4. Find ‘evidently_drift_dashboard’ DAG. Switch it on!
5. After the successful completion of the DAG, Evidently DataDrift HTML Report will be generated and stored locally in your system. 
6. To access the HTML Report, go to the project directory and open the newly created evidently_reports directory. Here you will see the report: boston_data_drift_by_airflow.html

Use this example as an inspiration! You can play around with the input data, scheduling options of Airflow, and Evidently Dashboard and Profile parameters as well!
