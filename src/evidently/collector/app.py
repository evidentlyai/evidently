from asyncio import ensure_future
from contextlib import asynccontextmanager
from typing import List

import pandas as pd
import uvicorn
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi_restful.tasks import repeat_every
from typing_extensions import Annotated

from evidently import ColumnMapping
from evidently.collector.config import CONFIG_PATH
from evidently.collector.config import CollectorConfig
from evidently.collector.config import CollectorServiceConfig
from evidently.collector.storage import LogEvent
from evidently.telemetry import DO_NOT_TRACK_ENV
from evidently.telemetry import event_logger
from evidently.ui.api.security import setup_security
from evidently.ui.api.utils import authorized
from evidently.ui.config import NoSecurityConfig
from evidently.ui.errors import EvidentlyServiceError
from evidently.ui.storage.common import SecretHeaderSecurity
from evidently.ui.utils import NumpyJsonResponse

COLLECTOR_INTERFACE = "collector"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run at startup
    Initialise the Client and add it to app.state
    """
    app.state.conf = CollectorServiceConfig.load_or_default(app.state.config_path)
    app.state.storage = app.state.conf.storage
    app.state.storage.init_all(app.state.conf)

    if event_logger.is_enabled():
        print(f"Anonimous usage reporting is enabled. To disable it, set env variable {DO_NOT_TRACK_ENV} to any value")
    else:
        print("Anonimous usage reporting is disabled")
    event_logger.send_event(COLLECTOR_INTERFACE, "startup")

    ensure_future(repeat_every(seconds=app.state.conf.check_interval, raise_exceptions=True)(check_snapshots)())
    yield
    """ Run on shutdown
        Close the connection
        Clear variables and release the resources
    """


app = FastAPI(lifespan=lifespan)


@app.exception_handler(EvidentlyServiceError)
async def entity_not_found_exception_handler(request: Request, exc: EvidentlyServiceError):
    return exc.to_response()


collector_write_router = APIRouter(dependencies=[Depends(authorized)], default_response_class=NumpyJsonResponse)


@collector_write_router.post("/{id}")
async def create_collector(id: Annotated[str, "Collector id"], data: CollectorConfig) -> CollectorConfig:
    data.id = id
    app.state.conf.collectors[id] = data
    app.state.storage.init(id)
    app.state.conf.save(CONFIG_PATH)
    return data


@collector_write_router.get("/{id}")
async def get_collector(id: Annotated[str, "Collector id"]) -> CollectorConfig:
    if id not in app.state.conf.collectors:
        raise HTTPException(status_code=404, detail=f"Collector config with id '{id}' not found")
    return app.state.conf.collectors[id]


@collector_write_router.post("/{id}/reference")
async def reference(id: Annotated[str, "Collector id"], request: Request):
    if id not in app.state.conf.collectors:
        raise HTTPException(status_code=404, detail=f"Collector config with id '{id}' not found")
    collector = app.state.conf.collectors[id]
    data = pd.DataFrame.from_dict(await request.json())
    path = collector.reference_path or f"{id}_reference.parquet"
    data.to_parquet(path)
    collector.reference_path = path
    app.state.conf.save(CONFIG_PATH)
    return {}


@collector_write_router.post("/{id}/data")
async def data(id: Annotated[str, "Collector id"], request: Request):
    if id not in app.state.conf.collectors:
        raise HTTPException(status_code=404, detail=f"Collector config with id '{id}' not found")
    async with app.state.storage.lock(id):
        app.state.storage.append(id, await request.json())
    return {}


@collector_write_router.get("/{id}/logs")
async def get_logs(id: Annotated[str, "Collector id"]) -> List[LogEvent]:
    if id not in app.state.conf.collectors:
        raise HTTPException(status_code=404, detail=f"Collector config with id '{id}' not found")
    return app.state.storage.get_logs(id)


async def check_snapshots():
    for _, collector in app.state.conf.collectors.items():
        if not collector.trigger.is_ready(collector, app.state.storage):
            continue
        # todo: call async
        await create_snapshot(collector)


async def create_snapshot(collector: CollectorConfig):
    async with app.state.storage.lock(collector.id):
        current = app.state.storage.get_and_flush(collector.id)
        if current is None:
            return
        current.index = current.index.astype(int)
        report_conf = collector.report_config
        report = report_conf.to_report_base()
        try:
            report.run(reference_data=collector.reference, current_data=current, column_mapping=ColumnMapping())
            report._inner_suite.raise_for_error()
        except Exception as e:
            app.state.storage.log(
                collector.id, LogEvent(ok=False, error=f"Error running report: {e.__class__.__name__}: {e.args}")
            )
            return
        try:
            collector.workspace.add_snapshot(collector.project_id, report.to_snapshot())
        except Exception as e:
            app.state.storage.log(
                collector.id, LogEvent(ok=False, error=f"Error saving snapshot: {e.__class__.__name__}: {e.args}")
            )
            return
        app.state.storage.log(collector.id, LogEvent(ok=True))


app.include_router(collector_write_router)


def run(host: str = "0.0.0.0", port: int = 8001, config_path: str = CONFIG_PATH, secret: str = None):
    setup_security(app, NoSecurityConfig() if secret is None else SecretHeaderSecurity(secret=secret))
    app.state.config_path = config_path
    uvicorn.run(app, host=host, port=port)


def main():
    run()


if __name__ == "__main__":
    main()
