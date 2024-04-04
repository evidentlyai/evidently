from functools import partial
from typing import Any
from typing import ClassVar
from typing import Dict

from iterative_telemetry import IterativeTelemetryLogger
from litestar.di import Provide

import evidently
from evidently.telemetry import DO_NOT_TRACK
from evidently.ui.components.base import Component


async def get_event_logger(telemetry_config: Any):
    _event_logger = IterativeTelemetryLogger(
        telemetry_config.tool_name,
        evidently.__version__,
        url=telemetry_config.url,
        token=telemetry_config.token,
        enabled=telemetry_config.enabled and DO_NOT_TRACK is None,
    )
    yield partial(_event_logger.send_event, telemetry_config.service_name)


class TelemetryComponent(Component):
    __section__: ClassVar = "telemetry"

    url: str = "http://35.232.253.5:8000/api/v1/s2s/event?ip_policy=strict"
    tool_name: str = "evidently"
    service_name: str = "service"
    token: str = "s2s.5xmxpip2ax4ut5rrihfjhb.uqcoh71nviknmzp77ev6rd"
    enabled: bool = True

    def get_dependencies(self) -> Dict[str, Provide]:
        return {
            "telemetry_config": Provide(lambda: self, sync_to_thread=True),
            "log_event": Provide(get_event_logger),
        }
