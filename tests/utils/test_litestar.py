import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def _module(name: str, **attrs):
    module = ModuleType(name)
    module.__dict__.update(attrs)
    return module


def _package(name: str, **attrs):
    module = _module(name, **attrs)
    module.__path__ = []
    return module


def _clear_litestar_modules(monkeypatch):
    for name in list(sys.modules):
        if name == "litestar" or name.startswith("litestar."):
            monkeypatch.delitem(sys.modules, name, raising=False)


def _load_compat_module():
    path = Path(__file__).parents[2] / "src" / "evidently" / "utils" / "litestar.py"
    spec = importlib.util.spec_from_file_location("evidently_litestar_compat_test", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pydantic_schema_plugin_uses_current_litestar_import(monkeypatch):
    plugin = type("CurrentPydanticSchemaPlugin", (), {})

    _clear_litestar_modules(monkeypatch)
    monkeypatch.setitem(sys.modules, "litestar", _package("litestar"))
    monkeypatch.setitem(sys.modules, "litestar.plugins", _package("litestar.plugins"))
    monkeypatch.setitem(
        sys.modules,
        "litestar.plugins.pydantic",
        _module("litestar.plugins.pydantic", PydanticSchemaPlugin=plugin),
    )
    monkeypatch.delitem(sys.modules, "litestar.contrib.pydantic", raising=False)

    module = _load_compat_module()

    assert module.PydanticSchemaPlugin is plugin


def test_pydantic_schema_plugin_falls_back_to_deprecated_import(monkeypatch):
    plugin = type("LegacyPydanticSchemaPlugin", (), {})

    _clear_litestar_modules(monkeypatch)
    monkeypatch.setitem(sys.modules, "litestar", _package("litestar"))
    monkeypatch.setitem(sys.modules, "litestar.plugins", _package("litestar.plugins"))
    monkeypatch.setitem(sys.modules, "litestar.contrib", _package("litestar.contrib"))
    monkeypatch.setitem(
        sys.modules,
        "litestar.contrib.pydantic",
        _module("litestar.contrib.pydantic", PydanticSchemaPlugin=plugin),
    )

    module = _load_compat_module()

    assert module.PydanticSchemaPlugin is plugin
