from typing import Annotated, List

import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi_utils.tasks import repeat_every

from config import CollectorConfig, CollectorServiceConfig, CONFIG_PATH
from evidently import ColumnMapping
from evidently.report import Report
from storage import LogEvent

app = FastAPI()
conf = CollectorServiceConfig.load_or_default(CONFIG_PATH)
storage = conf.storage
storage.init_all(conf)


@app.post("/{id}")
async def create_collector(id: Annotated[str, "Collector id"], data: CollectorConfig) -> CollectorConfig:
    data.id = id
    conf.collectors[id] = data
    storage.init(id)
    conf.save(CONFIG_PATH)
    return data


@app.get("/{id}")
async def get_collector(id: Annotated[str, "Collector id"]) -> CollectorConfig:
    if id not in conf.collectors:
        raise HTTPException(status_code=404, detail=f"Collector config with id '{id}' not found")
    return conf.collectors[id]


@app.post("/{id}/reference")
async def reference(id: Annotated[str, "Collector id"], request: Request):
    if id not in conf.collectors:
        raise HTTPException(status_code=404, detail=f"Collector config with id '{id}' not found")
    collector = conf.collectors[id]
    data = pd.DataFrame.from_dict(await request.json())
    path = collector.reference_path or f"{id}_reference.parquet"
    data.to_parquet(path)
    collector.reference_path = path
    conf.save(CONFIG_PATH)
    return {}


@app.post("/{id}/data")
async def data(id: Annotated[str, "Collector id"], request: Request):
    if id not in conf.collectors:
        raise HTTPException(status_code=404, detail=f"Collector config with id '{id}' not found")
    async with storage.lock(id):
        storage.append(id, await request.json())
    return {}


@app.get("/{id}/logs")
async def get_logs(id: Annotated[str, "Collector id"]) -> List[LogEvent]:
    if id not in conf.collectors:
        raise HTTPException(status_code=404, detail=f"Collector config with id '{id}' not found")
    return storage.get_logs(id)


@app.on_event("startup")
@repeat_every(seconds=conf.check_interval)
async def check_snapshots():
    for _, collector in conf.collectors.items():
        if not collector.trigger.is_ready(collector, storage):
            continue
        await create_snapshot(collector)


async def create_snapshot(collector: CollectorConfig):
    async with storage.lock(collector.id):
        current = storage.get_and_flush(collector.id)
        if current is None:
            return
        current.index = current.index.astype(int)
        report_conf = collector.report_config
        report = Report(metrics=report_conf.metrics, options=report_conf.options, metadata=report_conf.metadata, tags=report_conf.tags)
        try:
            report.run(reference_data=collector.reference, current_data=current, column_mapping=ColumnMapping())
            report._inner_suite.raise_for_error()
        except Exception as e:
            storage.log(collector.id, LogEvent(ok=False, error=f"Error running report: {e.__class__.__name__}: {e.args}"))
            return
        try:
            collector.workspace.add_report(collector.project_id, report)
        except Exception as e:
            storage.log(collector.id, LogEvent(ok=False, error=f"Error saving snapshot: {e.__class__.__name__}: {e.args}"))
            return
        storage.log(collector.id, LogEvent(ok=True))


def main():
    uvicorn.run(app, port=8081)


if __name__ == '__main__':
    main()
