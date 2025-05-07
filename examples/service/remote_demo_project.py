from evidently.ui.workspace import RemoteWorkspace
from evidently.ui.service.demo_projects import DEMO_PROJECTS
DEMO_PROJECT_NAME = "bikes"

def main():
    workspace = "http://localhost:8000"
    ws = RemoteWorkspace(workspace)
    demo_project = DEMO_PROJECTS[DEMO_PROJECT_NAME]
    has_demo_project = any(p.name == demo_project.name for p in ws.list_projects())
    if not has_demo_project:
        print("Generating demo project...")
        demo_project.create(ws)

    demo_project = ws.search_project(demo_project.name)[0]
    print(demo_project.id)


if __name__ == '__main__':
    main()