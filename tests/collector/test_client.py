import socket
import time
from multiprocessing import Process
from typing import Optional

import pandas as pd
import pytest

from evidently.legacy.collector.app import run
from evidently.legacy.collector.client import CollectorClient
from evidently.legacy.collector.config import CollectorConfig
from evidently.legacy.collector.config import IntervalTrigger
from evidently.legacy.collector.config import ReportConfig
from evidently.legacy.test_suite import TestSuite
from evidently.legacy.tests import TestNumberOfOutRangeValues

COLLECTOR_ID = "1"
PROJECT_ID = "2"

HOST = "localhost"
PORT = 8080
BASE_URL = f"http://{HOST}:{PORT}"


def create_test_data() -> pd.DataFrame:
    return pd.DataFrame([{"values1": 5.0, "values2": 0.0}])


def create_test_suite() -> TestSuite:
    return TestSuite(tests=[TestNumberOfOutRangeValues("values1", left=5)], tags=["quality"])


def create_report_config(
    current_data: pd.DataFrame,
    test_suite: TestSuite,
    references: Optional[pd.DataFrame] = None,
):
    test_suite.run(reference_data=references, current_data=current_data)
    return ReportConfig.from_test_suite(test_suite)


def create_collector_config(data: pd.DataFrame, test_suite: TestSuite) -> CollectorConfig:
    return CollectorConfig(
        trigger=IntervalTrigger(interval=1),
        report_config=create_report_config(current_data=data, test_suite=test_suite),
        project_id=PROJECT_ID,
    )


def create_collector_client(base_url: str = BASE_URL) -> CollectorClient:
    return CollectorClient(base_url=base_url)


def wait_server_start(host: str = HOST, port: int = PORT, timeout: float = 10.0, check_interval: float = 0.01) -> None:
    start_time = time.time()
    while time.time() - start_time < timeout:
        time.sleep(check_interval)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((host, port))
            except ConnectionRefusedError:
                continue
            return
    raise TimeoutError()


@pytest.fixture
def server() -> None:
    proc = Process(target=run, args=(HOST, PORT))
    proc.start()
    wait_server_start()
    try:
        yield
    finally:
        proc.kill()


@pytest.mark.skip
def test_create_collector_handler_work_with_collector_client(server: None):
    collector_config = create_collector_config(create_test_data(), create_test_suite())
    client = create_collector_client()
    resp = client.create_collector(COLLECTOR_ID, collector_config)
    assert resp["id"] == COLLECTOR_ID
    assert resp["project_id"] == PROJECT_ID


@pytest.mark.skip
def test_data_handler_work_with_collector_client(server: None):
    collector_config = create_collector_config(create_test_data(), create_test_suite())
    client = create_collector_client()
    client.create_collector(COLLECTOR_ID, collector_config)
    client.send_data(COLLECTOR_ID, create_test_data())


@pytest.mark.skip
def test_references_handler_work_with_collector_client(server: None):
    collector_config = create_collector_config(create_test_data(), create_test_suite())
    client = create_collector_client()
    client.create_collector(COLLECTOR_ID, collector_config)
    client.set_reference(COLLECTOR_ID, create_test_data())
