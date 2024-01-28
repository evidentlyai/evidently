import os.path
import re
import uuid

from watchdog.events import EVENT_TYPE_DELETED
from watchdog.events import EVENT_TYPE_MODIFIED
from watchdog.events import EVENT_TYPE_MOVED
from watchdog.events import FileSystemEvent
from watchdog.events import FileSystemEventHandler

from evidently.ui.storage.common import NO_USER
from evidently.ui.storage.local.base import METADATA_PATH
from evidently.ui.storage.local.base import SNAPSHOTS
from evidently.ui.storage.local.base import LocalState
from evidently.ui.storage.local.base import load_project

uuid4hex = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"


class WorkspaceDirHandler(FileSystemEventHandler):
    def __init__(self, state: LocalState):
        self.state = state
        self.path = state.location.path

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
            project = load_project(self.state.location, project_id)
            if project is None:
                return
            self.state.projects[project.id] = project.bind(self.state.project_manager, NO_USER.id)
        if event.event_type == EVENT_TYPE_DELETED:
            pid = uuid.UUID(project_id)
            del self.state.projects[pid]
            del self.state.snapshots[pid]
            del self.state.snapshot_data[pid]

    def on_snapshot_event(self, event):
        project_id, snapshot_id = self.parse_project_and_snapshot_id(event.src_path)
        if project_id is None or snapshot_id is None:
            return
        pid = uuid.UUID(project_id)
        sid = uuid.UUID(snapshot_id)
        project = self.state.projects.get(pid)
        if project is None:
            return
        if (event.event_type == EVENT_TYPE_MODIFIED or event.event_type == EVENT_TYPE_MOVED) and os.path.exists(
            event.src_path
        ):
            self.state.reload_snapshot(project, sid)
        if (
            event.event_type == EVENT_TYPE_DELETED
            or event.event_type == EVENT_TYPE_MOVED
            and not os.path.exists(event.src_path)
        ):
            del self.state.snapshots[pid][sid]
            del self.state.snapshot_data[pid][sid]
