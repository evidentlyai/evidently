from evidently.ui.demo_project import create_demo_project


def test_create_demo_proejct(tmp_path):
    create_demo_project(str(tmp_path))
