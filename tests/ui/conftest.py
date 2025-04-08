import json
import os
from typing import Optional

import pytest
from litestar import Litestar
from litestar import get
from litestar.datastructures import State
from litestar.testing import TestClient

from evidently._pydantic_compat import BaseModel
from evidently.legacy.ui.app import create_app
from evidently.legacy.ui.base import Project
from evidently.legacy.ui.components.base import Component
from evidently.legacy.ui.components.base import ComponentContext
from evidently.legacy.ui.components.storage import LocalStorageComponent
from evidently.legacy.ui.local_service import LocalConfig
from evidently.legacy.ui.local_service import LocalServiceComponent
from evidently.legacy.ui.managers.projects import ProjectManager
from evidently.legacy.ui.security.service import SecurityService
from evidently.legacy.utils import NumpyEncoder

HEADERS = {"Content-Type": "application/json"}

os.environ["DO_NOT_TRACK"] = "1"


class TestsSetupComponent(Component):
    class Config:
        arbitrary_types_allowed = True

    app: Optional[Litestar] = None

    def get_route_handlers(self, ctx: ComponentContext):
        @get("/tests_setup")
        async def tests_setup(project_manager: ProjectManager, security: SecurityService) -> None:
            self.app.state["pm"] = project_manager
            self.app.state["security"] = security

        return [tests_setup]

    def finalize(self, ctx: ComponentContext, app: Litestar):
        self.app = app
        client = TestClient(app)
        client.get("/tests_setup")


def _get_app(app) -> Litestar:
    if isinstance(app, Litestar):
        return app
    return _get_app(app.__closure__[0].cell_contents.app)


def _get_app_state(client: TestClient) -> State:
    try:
        return _get_app(client.app).state
    except (AttributeError, IndexError) as e:
        raise ValueError("Cannot find app state") from e


def get_pm(client: TestClient) -> ProjectManager:
    try:
        return _get_app_state(client)["pm"]
    except KeyError as e:
        raise ValueError("Cannot find pm in client") from e


def get_security(client: TestClient) -> SecurityService:
    try:
        return _get_app_state(client)["security"]
    except KeyError as e:
        raise ValueError("Cannot find security in client") from e


def _dumps(obj: BaseModel):
    return json.dumps(obj.dict(), allow_nan=True, cls=NumpyEncoder)


@pytest.fixture
def test_client(tmp_path):
    config = LocalConfig(
        storage=LocalStorageComponent(path=str(tmp_path)),
        service=LocalServiceComponent(debug=True),
        additional_components={"_setup_tests": TestsSetupComponent()},
    )
    return TestClient(create_app(config=config))


@pytest.fixture
def project_manager(test_client) -> ProjectManager:
    return get_pm(test_client)


@pytest.fixture
def mock_project():
    return Project(name="mock", team_id=None)


@pytest.fixture
def project_factory():
    def inner(name: str) -> Project:
        return Project(name=name, team_id=None)

    return inner
