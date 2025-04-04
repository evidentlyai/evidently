import time
from typing import Union
from unittest.mock import Mock

import pytest

from evidently._pydantic_compat import ValidationError
from evidently.legacy.collector.config import IntervalTrigger
from evidently.legacy.collector.config import RowsCountOrIntervalTrigger
from evidently.legacy.collector.config import RowsCountTrigger
from evidently.legacy.collector.storage import CollectorStorage


def test_interval_trigger_work():
    ready_arg = Mock()
    trigger = IntervalTrigger(interval=0.01)
    # First check always ready
    assert trigger.is_ready(ready_arg, ready_arg)
    assert trigger.is_ready(ready_arg, ready_arg) is False
    time.sleep(0.01)
    assert trigger.is_ready(ready_arg, ready_arg)


@pytest.mark.parametrize("interval", [0.0, -1.0])
def test_interval_trigger_invalid_interval(interval: float):
    with pytest.raises(ValidationError):
        IntervalTrigger(interval=interval)


def test_row_count_trigger_work():
    storage = Mock(spec=CollectorStorage)
    storage.get_buffer_size = Mock(side_effect=[0, 1, 0])
    config = Mock()
    trigger = RowsCountTrigger(rows_count=1)

    assert trigger.is_ready(config, storage) is False
    assert trigger.is_ready(config, storage) is True
    assert trigger.is_ready(config, storage) is False


@pytest.mark.parametrize("rows_count", [0.0, -1.0, 0.7])
def test_rows_count_trigger_invalid_rows_count(rows_count: Union[int, float]):
    with pytest.raises(ValidationError):
        RowsCountTrigger(rows_count=rows_count)


def test_rows_count_or_interval_trigger_work():
    storage = Mock(spec=CollectorStorage)
    storage.get_buffer_size = Mock(side_effect=[1])
    config = Mock()
    trigger = RowsCountOrIntervalTrigger(
        rows_count_trigger=RowsCountTrigger(rows_count=1), interval_trigger=IntervalTrigger(interval=0.1)
    )
    # Interval trigger
    assert trigger.is_ready(config, storage)
    # Rows count trigger
    assert trigger.is_ready(config, storage)
