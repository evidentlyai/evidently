from abc import ABC
from abc import abstractmethod
from typing import Optional
from typing import Tuple

import pandas as pd
from typing_extensions import TypeAlias

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import PrivateAttr
from evidently.legacy.options.base import Options
from evidently.legacy.utils.sync import async_to_sync
from evidently.llm.utils.wrapper import LLMWrapper
from evidently.llm.utils.wrapper import get_llm_wrapper

DatasetGeneratorResult: TypeAlias = Tuple[str, pd.DataFrame]


class BaseDatasetGenerator(BaseModel, ABC):
    class Config:
        is_base_type = True

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
