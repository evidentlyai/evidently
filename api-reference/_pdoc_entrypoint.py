#!/usr/bin/env python
"""
Fake pdoc CLI entrypoint that monkey-patches __all__ before running pdoc.
"""

import importlib
import re
import sys

from pdoc.__main__ import cli

# Configuration: dict mapping module names to their __pdoc__ settings
# For now, we'll auto-populate with False for all private vars
PDOC_CONFIG = {"evidently": {}}


def setup_module_pdoc(module_name: str) -> None:
    """Monkey-patch __pdoc__ for a module to exclude private members."""
    try:
        module = importlib.import_module(module_name)
        if not hasattr(module, "__all__"):
            module.__all__ = []

        # Add False for all private members (starting with _)
        for name in dir(module):
            if name.startswith("_") and not name.startswith("__"):
                if name in module.__all__:
                    module.__all__.remove(name)

        # # Recursively handle submodules
        # if hasattr(module, "__path__"):
        #     import pkgutil
        #     for importer, modname, ispkg in pkgutil.walk_packages(
        #         path=module.__path__,
        #         prefix=module.__name__ + "."
        #     ):
        #         setup_module_pdoc(modname)
    except Exception:
        # If module can't be imported, skip it
        pass


if __name__ == "__main__":
    for mod in PDOC_CONFIG:
        setup_module_pdoc(mod)
    sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    sys.exit(cli())
