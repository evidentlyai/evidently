from evidently.ui.demo_project import DEMO_PROJECT_NAME, create_demo_project
from evidently.ui.remote import RemoteWorkspace


def main():
    workspace = "http://localhost:8000"
    ws = RemoteWorkspace(workspace)
    has_demo_project = any(p.name == DEMO_PROJECT_NAME for p in ws.list_projects())
    if not has_demo_project:
        print("Generating demo project...")
        create_demo_project(ws)

    demo_project = ws.search_project(DEMO_PROJECT_NAME)[0]
    print(demo_project.id)


if __name__ == '__main__':
    main()