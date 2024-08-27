import json
import urllib.parse
from typing import Any
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import requests
from litestar.config.app import AppConfig
from litestar.plugins import InitPluginProtocol
from litestar.utils import is_class_and_subclass
from typing_extensions import Buffer
from uuid6 import UUID

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import ValidationError
from evidently._pydantic_compat import parse_obj_as
from evidently.pydantic_utils import UUID7
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


def _dec_uuid7(
    uuid_type: Type[UUID7],
    value: Any,
) -> UUID7:
    if isinstance(value, str):
        value = uuid_type(value)

    elif isinstance(value, Buffer):
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

    if value._required_version != value.version:
        raise ValidationError(f"Invalid UUID version: {value!r}")

    return value


uuid7_type_decoder = (lambda t: is_class_and_subclass(t, UUID7), _dec_uuid7)


class PydanticUUID7Plugin(InitPluginProtocol):
    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        app_config.type_decoders = [uuid7_type_decoder, *(app_config.type_decoders or [])]
        return app_config
