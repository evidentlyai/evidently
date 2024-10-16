from typing import Optional

from evidently._pydantic_compat import PrivateAttr
from evidently.experimental.dataset_generators.base import BaseDatasetGenerator
from evidently.options.base import Options
from evidently.utils.llm.wrapper import LLMWrapper
from evidently.utils.llm.wrapper import get_llm_wrapper


class BaseLLMDatasetGenerator(BaseDatasetGenerator):
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
