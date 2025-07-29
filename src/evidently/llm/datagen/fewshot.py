from typing import Any
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Set
from typing import Union

import pandas as pd

from evidently.legacy.options.base import AnyOptions
from evidently.legacy.options.base import Options
from evidently.llm.datagen.base import BaseLLMDatasetGenerator
from evidently.llm.datagen.base import DatasetGeneratorResult
from evidently.llm.datagen.config import Examples
from evidently.llm.datagen.config import GenerationSpec
from evidently.llm.datagen.config import ServiceSpec
from evidently.llm.datagen.config import UserProfile
from evidently.llm.utils.blocks import PromptBlock
from evidently.llm.utils.prompt_render import PreparedTemplate
from evidently.llm.utils.templates import StrPromptTemplate
from evidently.llm.utils.templates import prompt_contract


class FewShotPromptTemplate(StrPromptTemplate):
    sample_spec: ClassVar[GenerationSpec]
    additional_prompt_blocks: ClassVar[List[PromptBlock]]

    @prompt_contract
    def generate(self, count: int) -> List[str]:
        """
        {sample_spec}
        {additional_prompt_blocks}

        {% datagen_instruction('{count}') %}

        {% output_string_list(sample_spec.kind, tagged=True) %}
        """
        return []


class FewShotDatasetGenerator(BaseLLMDatasetGenerator):
    template: FewShotPromptTemplate
    sample_spec: GenerationSpec = GenerationSpec(kind="texts")
    additional_prompt_blocks: List[PromptBlock] = []
    count: int = 10

    def __init__(
        self,
        template: Union[str, FewShotPromptTemplate, None] = None,
        examples: Optional[List[str]] = None,
        example: Optional[str] = None,
        count: int = 10,
        kind: Optional[str] = None,
        complexity: Optional[str] = None,
        user: Optional[UserProfile] = None,
        sample_spec: Optional[GenerationSpec] = None,
        service: Union[str, ServiceSpec, None] = None,
        additional_prompt_blocks: Optional[List[PromptBlock]] = None,
        model="gpt-4o-mini",
        provider="openai",
        options: AnyOptions = None,
        **data: Any,
    ):
        if sample_spec is None:
            if examples is None and example is None:
                raise ValueError("Either `sample_spec` or `examples` or `example` must be provided")
            sample_spec = GenerationSpec(
                kind=kind or "texts",
                complexity=complexity or "medium",
                examples=Examples(examples=examples or [example or ""]),
            )

        self.sample_spec = sample_spec

        additional: List[PromptBlock] = additional_prompt_blocks or []
        if user is not None:
            additional.append(user if isinstance(user, UserProfile) else UserProfile(role=user))
        if service is not None:
            additional.append(
                service if isinstance(service, ServiceSpec) else ServiceSpec(kind="RAG", description=service)
            )
        self.additional_prompt_blocks = additional

        self.count = count
        self.provider = provider
        self.options = Options.from_any_options(options)
        self.model = model
        if isinstance(template, str):
            self.template = FewShotPromptTemplate(prompt_template=template)
        else:
            self.template = template or FewShotPromptTemplate()

        super().__init__(**data)
        if not self.sample_spec.has_examples:
            raise ValueError("At least one example must be provided")

    async def agenerate(self) -> DatasetGeneratorResult:
        max_attempt_count = 3
        attempt_count = 0
        inputs_set: Set[str] = set()
        num_questions = self.count
        assert self.sample_spec.examples is not None  # guaranteed by __init__
        while len(inputs_set) < num_questions and attempt_count < max_attempt_count:
            attempt_count += 1
            num_questions = (num_questions - len(inputs_set)) * attempt_count
            with self.template.with_context(
                sample_spec=self.sample_spec, additional_prompt_blocks=self.additional_prompt_blocks
            ):
                requests = self.template.generate(count=self.count)
            response = await self.wrapper.run(requests)
            inputs_set = inputs_set | set(response)

        return pd.DataFrame({"texts": list(inputs_set)[:num_questions]})

    @property
    def prepared_sample_template(self) -> PreparedTemplate:
        return self.template.prepare(
            sample_spec=self.sample_spec, additional_prompt_blocks=self.additional_prompt_blocks
        )
