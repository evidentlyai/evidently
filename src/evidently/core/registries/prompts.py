# ruff: noqa: E501
# fmt: off
from evidently.llm.prompts.content import PromptContent
from evidently.pydantic_utils import register_type_alias

register_type_alias(PromptContent, "evidently.llm.prompts.content.MessagesPromptContent", "evidently:prompt_content:MessagesPromptContent")
register_type_alias(PromptContent, "evidently.llm.prompts.content.TextPromptContent", "evidently:prompt_content:TextPromptContent")
