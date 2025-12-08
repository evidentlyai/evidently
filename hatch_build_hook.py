from hatchling.builders.hooks.plugin.interface import BuildHookInterface


def get_hatch_build_hook():
    return CustomBuildHook


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        import importlib.util
        from pathlib import Path

        version_file = Path(__file__).parent / "src" / "evidently" / "_version.py"
        spec = importlib.util.spec_from_file_location("_version", version_file)
        if spec is None or spec.loader is None:
            raise ValueError(f"Could not load version from {version_file}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        build_data["version"] = module.__version__
