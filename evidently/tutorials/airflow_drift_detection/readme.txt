1. Install Docker [https://docs.docker.com/get-docker/] to your system. You going to use it to install and run the example.
2. Go to the project directory and from the terminal run command: docker-compose up --build (To stop docker later run:  docker-compose down)
3. Open Airflow user interface in your browser. It will be at the localhost:8080 address.
4. Find ‘evidently_drift_dashboard’ DAG. Switch it on!
5. After successful completion of the DAG, Evidently DataDrift Dashboard will be generated and stored locally in your system. 
6. To access the Dashboard go to the project directory and open newly created evidently_reports directory. Here you have your dashboard: boston_data_drift_by_airflow.html

Use this example for the inspiration! You can play around with the input data, scheduling options of Airflow and Evidently Dashboard and Profile parameters as well!

