# ruff: noqa: E501
# fmt: off
from evidently.llm.prompts.content import PromptContent
from evidently.llm.templates import BaseLLMPromptTemplate
from evidently.llm.utils.blocks import PromptBlock
from evidently.llm.utils.templates import PromptTemplate
from evidently.pydantic_utils import register_type_alias

register_type_alias(BaseLLMPromptTemplate, "evidently.llm.templates.BinaryClassificationPromptTemplate", "evidently:prompt_template:BinaryClassificationPromptTemplate")
register_type_alias(BaseLLMPromptTemplate, "evidently.llm.templates.MulticlassClassificationPromptTemplate", "evidently:prompt_template:MulticlassClassificationPromptTemplate")
register_type_alias(PromptBlock, "evidently.llm.datagen.rag.RagConfig", "evidently:prompt_block:RagConfig")
register_type_alias(PromptBlock, "evidently.llm.datagen.rag.RagInputs", "evidently:prompt_block:RagInputs")
register_type_alias(PromptBlock, "evidently.llm.datagen.rag.RagOutputs", "evidently:prompt_block:RagOutputs")
register_type_alias(PromptBlock, "evidently.llm.datagen.rag.RagService", "evidently:prompt_block:RagService")
register_type_alias(PromptBlock, "evidently.llm.datagen.rag.SeedConfig", "evidently:prompt_block:SeedConfig")
register_type_alias(PromptBlock, "evidently.llm.datagen.rag.UserProfile", "evidently:prompt_block:UserProfile")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.Anchor", "evidently:prompt_block:Anchor")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.CompositePromptBlock", "evidently:prompt_block:CompositePromptBlock")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.JsonOutputFormatBlock", "evidently:prompt_block:JsonOutputFormatBlock")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.NoopOutputFormat", "evidently:prompt_block:NoopOutputFormat")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.OutputFormatBlock", "evidently:prompt_block:OutputFormatBlock")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.SimpleBlock", "evidently:prompt_block:SimpleBlock")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.StringFormatBlock", "evidently:prompt_block:StringFormatBlock")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.StringListFormatBlock", "evidently:prompt_block:StringListFormatBlock")
register_type_alias(PromptBlock, "evidently.llm.utils.blocks.Tag", "evidently:prompt_block:Tag")
register_type_alias(PromptContent, "evidently.llm.prompts.content.MessagesPromptContent", "evidently:prompt_content:MessagesPromptContent")
register_type_alias(PromptContent, "evidently.llm.prompts.content.TextPromptContent", "evidently:prompt_content:TextPromptContent")
register_type_alias(PromptTemplate, "evidently.llm.datagen.rag.InputSeedPromptTemplate", "evidently:prompt_template:InputSeedPromptTemplate")
register_type_alias(PromptTemplate, "evidently.llm.datagen.rag.RagInputsPromptTemplate", "evidently:prompt_template:RagInputsPromptTemplate")
register_type_alias(PromptTemplate, "evidently.llm.datagen.rag.RagOutputsPromptTemplate", "evidently:prompt_template:RagOutputsPromptTemplate")
register_type_alias(PromptTemplate, "evidently.llm.utils.templates.BlockPromptTemplate", "evidently:prompt_template:BlockPromptTemplate")
register_type_alias(PromptTemplate, "evidently.llm.utils.templates.StrPromptTemplate", "evidently:prompt_template:StrPromptTemplate")
register_type_alias(PromptTemplate, "evidently.llm.utils.templates.WithSystemPrompt", "evidently:prompt_template:WithSystemPrompt")
