from asyncio import Lock

import pandas as pd
import uvicorn
from fastapi import Body, FastAPI
from fastapi import Response, Request
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every

from config import CollectorConfig
from evidently import ColumnMapping
from evidently.report import Report
from  example_report import get_data

app = FastAPI()
conf = CollectorConfig.load("config.json")

lock = Lock()
buffer = []

_, reference = get_data()

@app.post("/data")
async def data(request: Request):
    async with lock:
        buffer.append(await request.json())
    print("Buffer size", len(buffer))
    return {}

@app.on_event("startup")
@repeat_every(seconds=conf.snapshot_interval)
async def create_snapshot():
    print("Creating snapshot")
    async with lock:
        if len(buffer) == 0:
            return
        current = pd.concat([
            pd.DataFrame.from_dict(o) for o in buffer
        ])
        current.index = current.index.astype(int)
        report_conf = conf.report_config()
        report = Report(metrics=report_conf.metrics, options=report_conf.options, metadata=report_conf.metadata, tags=report_conf.tags)
        report.run(reference_data=reference, current_data=current, column_mapping=ColumnMapping(numerical_features=["values1"]))
        report._inner_suite.raise_for_error()
        report.upload(conf.api_url, conf.project_id)
        buffer.clear()

def main():
    uvicorn.run(app, port=8001)


if __name__ == '__main__':
    main()
