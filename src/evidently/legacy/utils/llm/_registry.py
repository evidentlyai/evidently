# ruff: noqa: E501
# fmt: off
from evidently.legacy.utils.llm.prompts import PromptBlock
from evidently.legacy.utils.llm.prompts import PromptTemplate
from evidently.pydantic_utils import register_type_alias

register_type_alias(PromptBlock, "evidently.legacy.utils.llm.prompts.Anchor", "evidently:prompt_block:Anchor")
register_type_alias(PromptBlock, "evidently.legacy.utils.llm.prompts.JsonOutputFormatBlock", "evidently:prompt_block:JsonOutputFormatBlock")
register_type_alias(PromptBlock, "evidently.legacy.utils.llm.prompts.NoopOutputFormat", "evidently:prompt_block:NoopOutputFormat")
register_type_alias(PromptBlock, "evidently.legacy.utils.llm.prompts.SimpleBlock", "evidently:prompt_block:SimpleBlock")
register_type_alias(PromptBlock, "evidently.legacy.utils.llm.prompts.StringFormatBlock", "evidently:prompt_block:StringFormatBlock")
register_type_alias(PromptBlock, "evidently.legacy.utils.llm.prompts.StringListFormatBlock", "evidently:prompt_block:StringListFormatBlock")
register_type_alias(PromptTemplate, "evidently.legacy.utils.llm.prompts.BlockPromptTemplate", "evidently:prompt_template:BlockPromptTemplate")
