import ast
import glob
import os.path
from _ast import Import
from _ast import ImportFrom
from typing import Any

import pytest

import evidently

IMPORT_EXCEPTIONS = ["evidently.ui.config"]
IMPORT_EXCEPTIONS = [os.path.join(*i.split(".")) + ".py" for i in IMPORT_EXCEPTIONS]


@pytest.mark.parametrize(
    "sourcefile",
    glob.glob(
        os.path.join(os.path.dirname(os.path.dirname(evidently.__file__)), "**", "*.py"),
        recursive=True,
    ),
)
def test_all_imports_from_compat(sourcefile):
    if sourcefile.endswith("_pydantic_compat.py"):
        return
    with open(sourcefile, encoding="utf8") as f:
        tree = ast.parse(f.read(), filename=sourcefile)

    class Visitor(ast.NodeVisitor):
        def visit_ImportFrom(self, node: ImportFrom) -> Any:
            if node.module is not None and node.module.startswith("pydantic"):
                raise Exception(f"{sourcefile}:{node.lineno}")

        def visit_Import(self, node: Import) -> Any:
            if any(sourcefile.endswith(p) for p in IMPORT_EXCEPTIONS):
                return
            if any("pydantic" == name.name for name in node.names):
                raise Exception(f"{sourcefile}:{node.lineno}")

    Visitor().visit(tree)
