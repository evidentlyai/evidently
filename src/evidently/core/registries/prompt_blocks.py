# ruff: noqa: E501
# fmt: off
from evidently.llm.utils.blocks import PromptBlock
from evidently.pydantic_utils import register_type_alias

register_type_alias(PromptBlock, "evidently.llm.datagen.config.Examples", "evidently:prompt_block:Examples")
register_type_alias(PromptBlock, "evidently.llm.datagen.config.GenerationSpec", "evidently:prompt_block:GenerationSpec")
register_type_alias(PromptBlock, "evidently.llm.datagen.config.ServiceSpec", "evidently:prompt_block:ServiceSpec")
register_type_alias(PromptBlock, "evidently.llm.datagen.config.UserProfile", "evidently:prompt_block:UserProfile")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.Anchor", "evidently:prompt_block:Anchor")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.CompositePromptBlock", "evidently:prompt_block:CompositePromptBlock")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.JsonOutputFormatBlock", "evidently:prompt_block:JsonOutputFormatBlock")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.NoopOutputFormat", "evidently:prompt_block:NoopOutputFormat")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.OutputFormatBlock", "evidently:prompt_block:OutputFormatBlock")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.SimpleBlock", "evidently:prompt_block:SimpleBlock")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.StringFormatBlock", "evidently:prompt_block:StringFormatBlock")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.StringListFormatBlock", "evidently:prompt_block:StringListFormatBlock")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.Tag", "evidently:prompt_block:Tag")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.TagStringListFormatBlock", "evidently:prompt_block:TagStringListFormatBlock")
