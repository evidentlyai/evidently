import atexit
import subprocess
import time
from typing import List
from typing import Optional
from typing import Union

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import PrivateAttr
from evidently.ui.service.demo_projects import DemoProjectNamesForCliType
from evidently.ui.utils import get_html_link_to_running_service
from evidently.ui.workspace import RemoteWorkspace


def get_url_to_service(*, port: int) -> str:
    return f"http://127.0.0.1:{port}"


class RunServiceInfoVariants:
    class Success(BaseModel):
        port: int
        process: Optional[subprocess.Popen] = None

        class Config:
            arbitrary_types_allowed = True

        def __str__(self) -> str:
            return f"Running on {get_url_to_service(port=self.port)}"

        def __repr__(self) -> str:
            return f"Running on {get_url_to_service(port=self.port)}"

        def _repr_html_(self):
            return get_html_link_to_running_service(url_to_service=get_url_to_service(port=self.port))

    class Failed(BaseModel):
        error_message: str

        def __str__(self) -> str:
            return self.error_message

        def __repr__(self) -> str:
            return self.error_message

    Success = Success
    Failed = Failed


RunServiceInfo = Union[RunServiceInfoVariants.Success, RunServiceInfoVariants.Failed]


class _EvidentlyUIRunnerImpl(BaseModel):
    @staticmethod
    def __terminate_process(process: subprocess.Popen):
        # Send termination signal
        process.terminate()
        print("Sent termination signal to the running process.")

        # Wait for process to terminate (with timeout)
        try:
            print("Waiting for the process to terminate gracefully...")
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Force kill if it doesn't terminate gracefully
            print("Process did not terminate gracefully. Sending kill signal...")
            process.kill()
            process.wait()

        # Verify process has terminated
        if process.poll() is not None:
            print("Successfully terminated the running process.")
        else:
            print("Warning: Process termination status unclear.")

    # User-configurable service parameters
    port: Optional[int]
    workspace: Optional[str]
    demo_projects: Optional[List[DemoProjectNamesForCliType]]
    # Internal state: caches the service execution result after run() is called
    _run_info: Optional[RunServiceInfo] = PrivateAttr(default=None)

    def run(self, *, force: bool) -> RunServiceInfo:
        if force:
            if isinstance(self._run_info, RunServiceInfoVariants.Success) and self._run_info.process is not None:
                self.__terminate_process(self._run_info.process)
                self._run_info = None

            self._run_info = None

        if self._run_info is not None:
            return self._run_info

        if self.port:
            self._run_info = self.__run_evidently_service_on_port(port=self.port)
            print(self._run_info)
            return self._run_info

        # by default try to run on ports 8000-8005
        self._run_info = self.__run_evidently_service_try_on_ports_range(ports=list(range(8000, 8006)))
        print(self._run_info)
        return self._run_info

    def show_service(self):
        if self._run_info is None:
            print("Service is not running. Please run it first using `run()` method.")
            return

        if isinstance(self._run_info, RunServiceInfoVariants.Failed):
            print("Service failed to run")
            print(self._run_info)
            return

        class _show_html(BaseModel):
            html: str

            def _repr_html_(self):
                return f"""
                {self.html}
                """

        return _show_html(
            html=f"""
                <iframe
                    class="evidently-ui-iframe"
                    frameborder="0"
                    style="width: 100%; height: 1300px; max-height: 80vh"
                    src="{get_url_to_service(port=self._run_info.port)}"
                />
            """
        )

    def terminate(self):
        if self._run_info is None:
            print("Service is not running. Please run it first using `run()` method.")
            return

        if isinstance(self._run_info, RunServiceInfoVariants.Failed):
            print("Service failed to run")
            print(self._run_info)
            return

        if self._run_info.process is None:
            print("We have no control over the running process. Please terminate it manually.")
            return

        self.__terminate_process(self._run_info.process)
        self._run_info = None

    def get_workspace(self) -> RemoteWorkspace:
        if self._run_info is None:
            print("Service is not running. Please run it first using `run()` method.")
            raise ValueError("Service is not running")

        if isinstance(self._run_info, RunServiceInfoVariants.Failed):
            print("Service failed to run")
            print(self._run_info)
            raise ValueError("Service is not running")

        return RemoteWorkspace(base_url=get_url_to_service(port=self._run_info.port))

    def __run_evidently_service_on_port(
        self, *, port: int, max_wait_time_in_seconds: int = 10, time_step: float = 0.5
    ) -> RunServiceInfo:
        if self.__is_service_running(port=port):
            return RunServiceInfoVariants.Success(port=port)

        cmd = self.__get_launch_evidently_ui_cmd(port=port)

        # run service in background
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        atexit.register(lambda: self.__terminate_process(process))

        # wait for service to start
        current_wait_time: float = 0.0
        while process.poll() is None:
            time.sleep(time_step)
            current_wait_time += time_step

            if current_wait_time > max_wait_time_in_seconds:
                break

            if self.__is_service_running(port=port):
                return RunServiceInfoVariants.Success(port=port, process=process)

        assert isinstance(process.returncode, int) and process.returncode > 0
        if process.stderr is None:
            error_message = "Unknown error: stderr is not available"
        else:
            error_message = process.stderr.read().decode("utf-8")

        return RunServiceInfoVariants.Failed(error_message=error_message)

    def __run_evidently_service_try_on_ports_range(self, *, ports: List[int]) -> RunServiceInfo:
        for port in ports:
            result = self.__run_evidently_service_on_port(port=port)

            if isinstance(result, RunServiceInfoVariants.Failed):
                print(result)

            if isinstance(result, RunServiceInfoVariants.Success):
                return result

        return RunServiceInfoVariants.Failed(error_message=f"Failed to run on ports: {ports}")

    def __is_service_running(self, *, port: int):
        import requests

        try:
            data = self.__call_service_healt_check(port=port)

            version = data.get("version")
            application = data.get("application")

            if application == "Evidently UI" and version:
                return True
        except requests.exceptions.RequestException:
            pass

        return False

    def __call_service_healt_check(self, *, port: int):
        import requests

        response = requests.get(f"{get_url_to_service(port=port)}/api/version")
        if response.status_code == 200:
            if response.headers.get("Content-Type") == "application/json":
                data = response.json()
                return data

        return {}

    def __get_launch_evidently_ui_cmd(self, *, port: int) -> list[str]:
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

    def show_service(self):
        """
        Show the Evidently UI service in an iframe. Useful for Jupyter notebooks.
        """
        return self._runner.show_service()

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


# if __name__ == "__main__":
#     impl = EvidentlyUIRunner()
#     impl.run()

#     print("wait 10 seconds")
#     time.sleep(10)
#     print("done")
