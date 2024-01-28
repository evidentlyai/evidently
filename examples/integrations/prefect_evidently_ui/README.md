# Evidently UI + Prefect

![Evidently () + Prefect](static/preview.png "Dashboard preview")

This example shows steps to integrate Evidently into your production pipeline using Prefect and Evidently UI server.

- Run production ML pipelines for inference and monitoring with [Prefect](https://www.prefect.io/). 
- Generate data quality and model monitoring reports with Evidenlty UI


--------
Project Organization
------------

    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── features       <- Features for model training and inference.
    │   ├── predictions    <- Generated predictions.
    │   ├── raw            <- The original, immutable data dump.
    │   └── reference      <- Reference datasets for monitoring.
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    ├── prefect            <- Prefect artifacts and DB
    ├── src                <- Source code for use in this project.
    │   ├── pipelines      <- Source code for all pipelines
    │   ├── scripts        <- Helper scripts
    │   └── utils          <- Utility functions and classes 
    └── static             <- Assets for docs 


## :woman_technologist: Installation

### 1 - Fork / Clone this repository

Get the tutorial example code:

```bash
git clone git@github.com:evidentlyai/evidently.git
cd evidently/examples/integrations/prefect_evidently_ui
```

### 2 - Build Docker image with Prefect

```bash
export USER_ID=$(id -u)
docker compose build
```

<details>
<summary>DEV environment</summary>

Create virtual environment named `.venv` and install python libraries

```bash
python3 -m venv .venv
echo "export PYTHONPATH=$PWD" >> .venv/bin/activate
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
``` 
</details>

## :rocket: Launch Monitoring Cluster

### 1 - Launch Prefect app

```bash
docker compose up prefect -d
```

Open Prefect UI: [http://localhost:4200](http://localhost:4200)


### 2 - Enter working Docker container

```bash
docker exec -ti prefect /bin/bash
```

**Note**: further commands will be run inside the `Docker` container.


### 3 - Prepare data and model

```bash 
python src/scripts/load_data.py               # Download data for NYC Taxi to 'data/raw'
python src/scripts/process_data.py            # Process & save to 'data/features/'
python src/scripts/train.py                   # Save trained model to 'models/' 
python src/scripts/prepare_reference_data.py  # Save to 'data/reference'
```

### 4 - Run scoring & monitoring pipelines

Run all pipelines at once:

```bash 
python src/pipelines/scheduler.py
```

Or, run each pipeline (flow) separately:

```bash
python src/pipelines/predict.py --ts '2021-02-01 01:00:00' --interval 60
python src/pipelines/monitor_data.py --ts '2021-02-01 01:00:00' --interval 60
python src/pipelines/monitor_model.py --ts '2021-02-01 02:00:00' --interval 60

```

<details>
<summary>Notes</summary>

-  It's expected to run the `predict` pipeline before monitoring pipelines for each timestamp `--ts` 
- `monitor_model` pipeline requires ground truth data to test the quality of predictions. We assume that these labels are available for the previous period. The earliest date to run `monitor_model` is '2021-02-01 02:00:00'
- When you design a new project (dashboard) or add panels to existing one, you need to update Evidently UI.
    ```bash
    python src/scripts/update_dashboards.py
    ```

</details>

### 6 - Launch Evidently Monitoring UI

```bash
docker compose up evidently-ui -d
```

Open Evidently UI: [http://localhost:8001](http://localhost:8001)

<details>
<summary>Restart Evidently UI to show up new dashboards</summary>

- In case you add a new project (dashboard) and can't see it in the UI:

    ```bash
    docker compose restart evidently-ui
    ```
</details>



## :checkered_flag: Stop cluster

```bash
docker compose down
```
