import json
from abc import abstractmethod
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List

from jsonschema import ValidationError
from jsonschema import validate

from evidently.legacy.utils.llm.errors import LLMResponseParseError
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel


class LLMResponseSchema(AutoAliasMixin, EvidentlyBaseModel):
    __alias_type__: ClassVar[str] = "llm_output_schema"

    class Config:
        is_base_type = True

    @abstractmethod
    def parse_llm_response(self, response: str) -> Any:  # todo: generic
        raise NotImplementedError


class JsonLLMResponseSchema(LLMResponseSchema):
    json_schema: Dict[str, Any]

    def parse_llm_response(self, response: str) -> Any:
        try:
            response_data = json.loads(response)
            validate(instance=response_data, schema=self.json_schema)
        except (json.JSONDecodeError, ValidationError) as e:
            raise LLMResponseParseError("Failed to parse response as json with schema", response) from e

        return response_data


class PlainLLMResponseSchema(LLMResponseSchema):
    def parse_llm_response(self, response: str) -> str:
        return response


class LinesLLMResponseSchema(LLMResponseSchema):
    def parse_llm_response(self, response: str) -> List[str]:
        return [line.strip() for line in response.split("\n") if line.strip()]
