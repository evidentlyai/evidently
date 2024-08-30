import json
import urllib.parse
import uuid
from typing import Any
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import requests
import uuid6
from litestar.utils import is_class_and_subclass
from msgspec import ValidationError
from uuid6 import UUID

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import parse_obj_as
from evidently.ui.storage.common import SECRET_HEADER_NAME
from evidently.utils import NumpyEncoder

T = TypeVar("T", bound=BaseModel)


class RemoteClientBase:
    def __init__(self, base_url: str, secret: str = None):
        self.base_url = base_url
        self.secret = secret

    def _request(
        self,
        path: str,
        method: str,
        query_params: Optional[dict] = None,
        body: Optional[dict] = None,
        response_model: Optional[Type[T]] = None,
    ) -> Union[T, requests.Response]:
        # todo: better encoding
        headers = {SECRET_HEADER_NAME: self.secret}
        data = None
        if body is not None:
            headers["Content-Type"] = "application/json"

            data = json.dumps(body, allow_nan=True, cls=NumpyEncoder).encode("utf8")

        response = requests.request(
            method, urllib.parse.urljoin(self.base_url, path), params=query_params, data=data, headers=headers
        )
        response.raise_for_status()
        if response_model is not None:
            return parse_obj_as(response_model, response.json())
        return response


def parse_json(body: bytes) -> Any:
    return json.loads(body)


def _dec_uuid6(
    uuid_type: Type[uuid6.UUID],
    value: Any,
) -> uuid6.UUID:
    if isinstance(value, str):
        value = uuid_type(value)

    if isinstance(value, uuid.UUID):
        return uuid6.UUID(hex=value.hex)

    elif hasattr(value, "__buffer__"):
        value = bytes(value)
        try:
            value = uuid_type(value.decode())
        except ValueError:
            # 16 bytes in big-endian order as the bytes argument fail
            # the above check
            value = uuid_type(bytes=value)
    elif isinstance(value, UUID):
        value = uuid_type(str(value))

    if not isinstance(value, uuid_type):
        raise ValidationError(f"Invalid UUID: {value!r}")

    if uuid_type._required_version != value.version:  # type: ignore[attr-defined]
        raise ValidationError(f"Invalid UUID version: {value!r}")

    return value


uuid6_type_decoder = (lambda t: is_class_and_subclass(t, uuid6.UUID), _dec_uuid6)


# class PydanticUUID7Plugin(InitPluginProtocol):
#     def on_app_init(self, app_config: AppConfig) -> AppConfig:
#         app_config.type_decoders = [uuid6_type_decoder, *(app_config.type_decoders or [])]
#         return app_config
