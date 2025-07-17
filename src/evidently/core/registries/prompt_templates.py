# ruff: noqa: E501
# fmt: off
from evidently.llm.templates import BaseLLMPromptTemplate
from evidently.llm.utils.templates import PromptTemplate
from evidently.pydantic_utils import register_type_alias

register_type_alias(PromptTemplate, "evidently.llm.datagen.fewshot.FewShotPromptTemplate", "evidently:prompt_template:FewShotPromptTemplate")
register_type_alias(PromptTemplate, "evidently.llm.datagen.rag.RagQueryPromptTemplate", "evidently:prompt_template:RagQueryPromptTemplate")
register_type_alias(PromptTemplate, "evidently.llm.datagen.rag.RagResponsePromptTemplate", "evidently:prompt_template:RagResponsePromptTemplate")
register_type_alias(PromptTemplate, "evidently.llm.utils.templates.BlockPromptTemplate", "evidently:prompt_template:BlockPromptTemplate")
register_type_alias(PromptTemplate, "evidently.llm.utils.templates.StrPromptTemplate", "evidently:prompt_template:StrPromptTemplate")
register_type_alias(PromptTemplate, "evidently.llm.utils.templates.WithSystemPrompt", "evidently:prompt_template:WithSystemPrompt")
register_type_alias(BaseLLMPromptTemplate, "evidently.llm.templates.BinaryClassificationPromptTemplate", "evidently:prompt_template:BinaryClassificationPromptTemplate")
register_type_alias(BaseLLMPromptTemplate, "evidently.llm.templates.MulticlassClassificationPromptTemplate", "evidently:prompt_template:MulticlassClassificationPromptTemplate")
