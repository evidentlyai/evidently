try:
    from litestar.plugins.pydantic import PydanticSchemaPlugin
except ImportError:
    from litestar.contrib.pydantic import PydanticSchemaPlugin

__all__ = ["PydanticSchemaPlugin"]
