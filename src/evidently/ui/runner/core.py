import atexit
import logging
import subprocess
import time
from typing import Callable
from typing import List
from typing import Literal
from typing import Optional
from typing import Union

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import PrivateAttr
from evidently.ui.runner.utils import get_url_to_service_by_port
from evidently.ui.runner.utils import is_service_running
from evidently.ui.runner.utils import terminate_process
from evidently.ui.service.demo_projects import DemoProjectNamesForCliType
from evidently.ui.utils import get_html_link_to_running_service
from evidently.ui.workspace import RemoteWorkspace

logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class ServicePage:
    service_page_path: str

    def __init__(
        self,
        *,
        project_id: Optional[str] = None,
        project_list: Optional[
            Union[Literal["reports"], Literal["datasets"], Literal["traces"], Literal["prompts"]]
        ] = None,
        report_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
        export_id: Optional[str] = None,
        trace_view_mode: Optional[Union[Literal["trace"], Literal["dataset"], Literal["dialog"]]] = None,
        trace_id: Optional[str] = None,
        prompt_id: Optional[str] = None,
    ):
        """
        Initialize the ServicePage to construct a URL path for navigating to specific pages in the Evidently UI service.

        Args:
        - `project_id`: Optional project identifier.
        - `project_list`: Optional list view type ("reports", "datasets", "traces", or "prompts").
          If provided, navigates to a list page.
        - `report_id`: Optional report identifier.
        - `dataset_id`: Optional dataset identifier.
        - `export_id`: Optional trace identifier.
        - `trace_view_mode`: Optional trace view mode ("trace", "dataset", or "dialog").
        - `trace_id`: Optional trace identifier.
        - `prompt_id`: Optional prompt identifier.
        """
        self.service_page_path = ""

        if project_id:
            self.service_page_path += f"projects/{project_id}"
            if project_list:
                self.service_page_path += f"/{project_list}"
                return
            if report_id:
                self.service_page_path += f"/reports/{report_id}"
            if dataset_id:
                self.service_page_path += f"/datasets/{dataset_id}"
                return
            if export_id:
                self.service_page_path += f"/traces/{export_id}"
                if trace_view_mode:
                    self.service_page_path += f"/{trace_view_mode}"
                    return
                if trace_id:
                    self.service_page_path += f"?trace-id={trace_id}"
                return
            if prompt_id:
                self.service_page_path += f"/prompts/{prompt_id}"
                return


class RunServiceInfo(BaseModel):
    """Base class for service run status information.

    Returned by `EvidentlyUIRunner.run()` to indicate the status of the UI service.
    Use `raise_on_error()` to raise an exception if the service failed to start.
    """

    def raise_on_error(self):
        """Raise an exception if the service failed to start.

        Raises:
        * `ServiceRunnerError`: If the service is not running or failed to start.
        """
        pass


class ServiceRunnerError(Exception):
    """
    Runner failed to start or terminate service.
    """

    def __init__(self, message: str):
        super().__init__(message)


class RunServiceInfoVariants:
    """Variants of `RunServiceInfo` representing different service states."""

    class Success(RunServiceInfo):
        """Service is running successfully."""

        port: int
        """Port number the service is running on."""
        process: subprocess.Popen
        """Subprocess handle for the running service."""

        class Config:
            """@private"""

            arbitrary_types_allowed = True

        def __str__(self) -> str:
            return f"Running on {get_url_to_service_by_port(port=self.port)}"

        def __repr__(self) -> str:
            return f"Running on {get_url_to_service_by_port(port=self.port)}"

        def _repr_html_(self):
            """Get HTML representation with link to the service.

            Returns:
            * HTML string with link to the running service.
            """
            return get_html_link_to_running_service(url_to_service=get_url_to_service_by_port(port=self.port))

    class NotRunning(RunServiceInfo):
        """Service is not running."""

        def raise_on_error(self):
            raise ServiceRunnerError("Service is not running. Please run it first using `run()` method.")

    class Failed(RunServiceInfo):
        """Service failed to start."""

        error_message: str
        """Error message describing why the service failed."""

        def __str__(self) -> str:
            return self.error_message

        def __repr__(self) -> str:
            return self.error_message

        def raise_on_error(self):
            raise ServiceRunnerError(message=self.error_message)


class _ServiceIframeHandler:
    service_url: str

    def __init__(self, url: str):
        self.service_url = url

    def _repr_html_(self):
        link_html = get_html_link_to_running_service(
            url_to_service=self.service_url, title="Go to page", service_label="Page"
        )

        return f"""
                {link_html}
                <iframe
                    class="evidently-ui-iframe"
                    frameborder="0"
                    style="width: 100%; height: 1300px; max-height: 80vh"
                    allow="clipboard-write"
                    src="{self.service_url}"
                />
            """


class _EvidentlyUIRunnerImpl(BaseModel):
    # User-configurable service parameters
    port: Optional[int]
    workspace: Optional[str]
    demo_projects: Optional[List[DemoProjectNamesForCliType]]
    # Internal state: caches the service execution result after run() is called
    _run_info: RunServiceInfo = PrivateAttr(default_factory=lambda: RunServiceInfoVariants.NotRunning())
    _atexit_handler: Optional[Callable[[], object]] = PrivateAttr(default=None)

    def run(self, *, force: bool) -> RunServiceInfo:
        if force:
            self._stop_service()

        if isinstance(self._run_info, RunServiceInfoVariants.Success):
            return self._run_info

        if self.port:
            self._run_info = self._run_evidently_service_on_port(port=self.port)
            logger.info(self._run_info)
            return self._run_info

        # by default try to run on ports 8000-8005
        self._run_info = self._run_evidently_service_try_on_ports_range(ports=list(range(8000, 8006)))
        logger.info(self._run_info)
        return self._run_info

    def show_service(self, *, page: ServicePage = None):
        if not isinstance(self._run_info, RunServiceInfoVariants.Success):
            self._run_info.raise_on_error()
            raise ServiceRunnerError(f"Unexpected status: {self._run_info}")

        port = self._run_info.port
        service_url = get_url_to_service_by_port(port=port)

        page = page or ServicePage()
        service_url = f"{service_url}/{page.service_page_path}"

        return _ServiceIframeHandler(service_url)

    def get_service_url(self) -> str:
        if not isinstance(self._run_info, RunServiceInfoVariants.Success):
            self._run_info.raise_on_error()
            raise ServiceRunnerError(f"Unexpected status: {self._run_info}")

        return get_url_to_service_by_port(port=self._run_info.port)

    def terminate(self):
        self._run_info.raise_on_error()
        self._stop_service()

    def _stop_service(self):
        if isinstance(self._run_info, RunServiceInfoVariants.Success):
            terminate_process(self._run_info.process)

        self._run_info = RunServiceInfoVariants.NotRunning()

        if self._atexit_handler:
            atexit.unregister(self._atexit_handler)
            self._atexit_handler = None

    def get_workspace(self) -> RemoteWorkspace:
        if not isinstance(self._run_info, RunServiceInfoVariants.Success):
            self._run_info.raise_on_error()
            raise ServiceRunnerError(f"Unexpected status: {self._run_info}")

        return RemoteWorkspace(base_url=get_url_to_service_by_port(port=self._run_info.port))

    def _run_evidently_service_on_port(
        self, *, port: int, max_wait_time_in_seconds: int = 10, time_step: float = 0.5
    ) -> RunServiceInfo:
        if is_service_running(port=port):
            error_message = f"Service is already running on port {port}"
            return RunServiceInfoVariants.Failed(error_message=error_message)

        cmd = self._get_launch_evidently_ui_cmd(port=port)

        # run service in background
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        def _terminate_process():
            terminate_process(process)
            self._run_info = RunServiceInfoVariants.NotRunning()

        self._atexit_handler = _terminate_process
        atexit.register(_terminate_process)

        # wait for service to start
        current_wait_time: float = 0.0
        while process.poll() is None:
            time.sleep(time_step)
            current_wait_time += time_step

            if current_wait_time > max_wait_time_in_seconds:
                break

            if is_service_running(port=port):
                return RunServiceInfoVariants.Success(port=port, process=process)

        assert isinstance(process.returncode, int) and process.returncode > 0
        if process.stderr is None:
            error_message = "Unknown error: stderr is not available"
        else:
            error_message = process.stderr.read().decode("utf-8")

        return RunServiceInfoVariants.Failed(error_message=error_message)

    def _run_evidently_service_try_on_ports_range(self, *, ports: List[int]) -> RunServiceInfo:
        for port in ports:
            result = self._run_evidently_service_on_port(port=port)

            if isinstance(result, RunServiceInfoVariants.Failed):
                logger.warning(f"Failed to run service on port {port}: {result}")

            if isinstance(result, RunServiceInfoVariants.Success):
                return result

        return RunServiceInfoVariants.Failed(error_message=f"Failed to run on ports: {ports}")

    def _get_launch_evidently_ui_cmd(self, *, port: int) -> list[str]:
        cmd = ["evidently", "ui", "--port", str(port)]

        if self.demo_projects:
            cmd.append("--demo-projects")
            if "all" in self.demo_projects:
                cmd.append("all")
            else:
                cmd.append(",".join(self.demo_projects))

        if self.workspace:
            cmd.append("--workspace")
            cmd.append(self.workspace)

        return cmd


class EvidentlyUIRunner:
    """
    Run `evidently ui` command in the background and provide a client to interact with the running service.
    """

    def __init__(
        self,
        *,
        port: int = None,
        workspace: str = None,
        demo_projects: Union[DemoProjectNamesForCliType, List[DemoProjectNamesForCliType]] = None,
    ):
        """
        Initialize the Evidently UI runner.

        Args:
        * `port`: Port to run the service on. If not provided, will try ports `8000-8005`.
        * `workspace`: Path to the workspace directory. Default is `workspace`.
        * `demo_projects`: List of demo projects to generate. Options: `bikes`, `reviews`, `all`. You can also pass a single string value.
        """
        if isinstance(demo_projects, str):
            demo_projects = [demo_projects]

        self._runner = _EvidentlyUIRunnerImpl(port=port, workspace=workspace, demo_projects=demo_projects)

    def run(self, *, force: bool = False) -> RunServiceInfo:
        """
        Run the Evidently UI service.

        Args:
        * `force`: If `True`, terminates any previously running service started by this runner instance
          and forces a fresh start, ignoring cached runs.

        Returns:
        * `RunServiceInfo`: Information about the running service.
        """
        return self._runner.run(force=force)

    def show_service(self, page: ServicePage = None):
        """
        Show the Evidently UI service in an iframe. Useful for Jupyter notebooks.

        Args:
        * `page`: Service page. See `ServicePage` for available options.
        """
        return self._runner.show_service(page=page)

    def get_service_url(self) -> str:
        """
        Get the URL of the running service.
        """
        return self._runner.get_service_url()

    def get_workspace(self) -> RemoteWorkspace:
        """
        Get a client to interact with the running service.

        Returns:
        * `RemoteWorkspace`: A client to interact with the running remote workspace.

        Raises:
        * `ValueError`: If the service is not running.
        """
        return self._runner.get_workspace()

    def terminate(self):
        """
        Terminate the Evidently UI service.
        """
        self._runner.terminate()
