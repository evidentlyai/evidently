import subprocess


def get_url_to_service_by_port(*, port: int) -> str:
    return f"http://127.0.0.1:{port}"


def call_service_healt_check(*, port: int):
    import requests

    response = requests.get(f"{get_url_to_service_by_port(port=port)}/api/version")
    if response.status_code == 200:
        if response.headers.get("Content-Type") == "application/json":
            data = response.json()
            return data
    return {}


def is_service_running(*, port: int):
    try:
        data = call_service_healt_check(port=port)

        version = data.get("version")
        application = data.get("application")

        if application == "Evidently UI" and version:
            return True
    except Exception:
        pass

    return False


def terminate_process(process: subprocess.Popen):
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
