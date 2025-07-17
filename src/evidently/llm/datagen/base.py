from abc import ABC
from abc import abstractmethod
from typing import ClassVar
from typing import Optional

import pandas as pd
from typing_extensions import TypeAlias

from evidently._pydantic_compat import PrivateAttr
from evidently.legacy.options.base import Options
from evidently.legacy.utils.sync import async_to_sync
from evidently.llm.utils.blocks import SimpleBlock
from evidently.llm.utils.prompt_render import prompt_command
from evidently.llm.utils.wrapper import LLMWrapper
from evidently.llm.utils.wrapper import get_llm_wrapper
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel

DatasetGeneratorResult: TypeAlias = pd.DataFrame


class BaseDatasetGenerator(AutoAliasMixin, EvidentlyBaseModel, ABC):
    __alias_type__: ClassVar = "dataset_generator"

    class Config:
        is_base_type = True
        extra = "forbid"

    options: Options

    @abstractmethod
    async def agenerate(self) -> DatasetGeneratorResult:
        raise NotImplementedError

    def generate(self) -> DatasetGeneratorResult:
        return async_to_sync(self.agenerate())


class BaseLLMDatasetGenerator(BaseDatasetGenerator, ABC):
    provider: str
    model: str
    _llm_wrapper: Optional[LLMWrapper] = PrivateAttr(None)

    def get_llm_wrapper(self, options: Options) -> LLMWrapper:
        if self._llm_wrapper is None:
            self._llm_wrapper = get_llm_wrapper(self.provider, self.model, options)
        return self._llm_wrapper

    @property
    def wrapper(self):
        return self.get_llm_wrapper(self.options)


@prompt_command("datagen_instruction")
def datagen_instruction_block(number):
    instruction = f"""Instructions:
•	Make sure the sentence are not exactly repeats of each other.
•	Remain faithful to the above context.
•	Make sure you do not start sentence with hyphen sign.
•	Make sure you do not end sentence with a newline.
•	Avoid providing any preamble.
•	Avoid providing any closing statement.
•	Ensure the number of generated texts is exactly {number}"""
    return SimpleBlock(value=instruction)
