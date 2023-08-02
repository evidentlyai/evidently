import os.path
import re

from watchdog.events import EVENT_TYPE_DELETED
from watchdog.events import EVENT_TYPE_MODIFIED
from watchdog.events import EVENT_TYPE_MOVED
from watchdog.events import FileSystemEvent
from watchdog.events import FileSystemEventHandler

from evidently.ui.workspace import METADATA_PATH
from evidently.ui.workspace import SNAPSHOTS
from evidently.ui.workspace import Workspace

uuid4hex = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"


class WorkspaceDirHandler(FileSystemEventHandler):
    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.path = os.path.abspath(self.workspace.path)

    def dispatch(self, event):
        if self.is_project_event(event):
            self.on_project_event(event)
            return
        if self.is_snapshot_event(event):
            self.on_snapshot_event(event)

    def is_project_event(self, event: FileSystemEvent):
        return re.fullmatch(os.path.join(self.path, uuid4hex, METADATA_PATH), event.src_path, re.I)

    def is_snapshot_event(self, event: FileSystemEvent):
        return re.fullmatch(os.path.join(self.path, uuid4hex, SNAPSHOTS, uuid4hex + r"\.json"), event.src_path, re.I)

    def parse_project_id(self, path):
        m = re.match(os.path.join(self.path, f"({uuid4hex})"), path)
        if m:
            return m.group(1)
        return None

    def parse_project_and_snapshot_id(self, path):
        m = re.match(os.path.join(self.path, f"({uuid4hex})", SNAPSHOTS, f"({uuid4hex})"), path)
        if m:
            return m.group(1), m.group(2)
        return None, None

    def on_project_event(self, event: FileSystemEvent):
        project_id = self.parse_project_id(event.src_path)
        if project_id is None:
            return
        if event.event_type == EVENT_TYPE_MODIFIED:
            self.workspace.reload_project(project_id)
        if event.event_type == EVENT_TYPE_DELETED:
            self.workspace.delete_project(project_id)

    def on_snapshot_event(self, event):
        project_id, snapshot_id = self.parse_project_and_snapshot_id(event.src_path)
        if project_id is None or snapshot_id is None:
            return
        project = self.workspace.get_project(project_id)
        if project is None:
            return
        if (event.event_type == EVENT_TYPE_MODIFIED or event.event_type == EVENT_TYPE_MOVED) and os.path.exists(
            event.src_path
        ):
            project.reload_snapshot(snapshot_id)
        if (
            event.event_type == EVENT_TYPE_DELETED
            or event.event_type == EVENT_TYPE_MOVED
            and not os.path.exists(event.src_path)
        ):
            project.delete_snapshot(snapshot_id)
