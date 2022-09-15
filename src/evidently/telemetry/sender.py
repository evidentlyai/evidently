import logging
import os
import platform

import requests

import evidently


class TelemetrySender:
    def __init__(self, address):
        self.address = address
        self.env = _collect_environment()
        self.evi = _collect_package()

    def send(self, usage):
        collected = dict(
            environment=self.env,
            evidently=self.evi,
            usage=usage,
        )
        try:
            requests.post(self.address, json=collected, timeout=3)
        except Exception as error:  # pylint: disable=broad-except
            logging.warning(f"failed to send telemetry: {error}")


def _collect_environment():
    return dict(
        python=dict(
            version=platform.python_version(),
            interpreter=platform.python_implementation(),
            conda="CONDA_DEFAULT_ENV" in os.environ,
            venv="VIRTUAL_ENV" in os.environ,
        ),
        os=platform.platform(),
    )


def _collect_package():
    return dict(version=evidently.__version__)
