# ruff: noqa: E501
# fmt: off
from evidently.llm.prompts.content import PromptContent
from evidently.llm.templates import BaseLLMPromptTemplate
from evidently.llm.utils.prompts import PromptBlock
from evidently.llm.utils.prompts import PromptTemplate
from evidently.pydantic_utils import register_type_alias

register_type_alias(PromptBlock, "evidently.llm.utils.prompts.Anchor", "evidently:prompt_block:Anchor")
register_type_alias(PromptBlock, "evidently.llm.utils.prompts.JsonOutputFormatBlock", "evidently:prompt_block:JsonOutputFormatBlock")
register_type_alias(PromptBlock, "evidently.llm.utils.prompts.NoopOutputFormat", "evidently:prompt_block:NoopOutputFormat")
register_type_alias(PromptBlock, "evidently.llm.utils.prompts.SimpleBlock", "evidently:prompt_block:SimpleBlock")
register_type_alias(PromptBlock, "evidently.llm.utils.prompts.StringFormatBlock", "evidently:prompt_block:StringFormatBlock")
register_type_alias(PromptBlock, "evidently.llm.utils.prompts.StringListFormatBlock", "evidently:prompt_block:StringListFormatBlock")
register_type_alias(PromptContent, "evidently.llm.prompts.content.MessagesPromptContent", "evidently:prompt_content:MessagesPromptContent")
register_type_alias(PromptContent, "evidently.llm.prompts.content.TextPromptContent", "evidently:prompt_content:TextPromptContent")
register_type_alias(PromptTemplate, "evidently.llm.utils.prompts.BlockPromptTemplate", "evidently:prompt_template:BlockPromptTemplate")
register_type_alias(PromptTemplate, "evidently.llm.utils.prompts.WithSystemPrompt", "evidently:prompt_template:WithSystemPrompt")
register_type_alias(BaseLLMPromptTemplate, "evidently.llm.templates.BinaryClassificationPromptTemplate", "evidently:prompt_template:BinaryClassificationPromptTemplate")
register_type_alias(BaseLLMPromptTemplate, "evidently.llm.templates.MulticlassClassificationPromptTemplate", "evidently:prompt_template:MulticlassClassificationPromptTemplate")
