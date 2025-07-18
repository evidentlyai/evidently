# ruff: noqa: E501
# fmt: off
from evidently.llm.datagen.base import BaseDatasetGenerator
from evidently.pydantic_utils import register_type_alias

register_type_alias(BaseDatasetGenerator, "evidently.llm.datagen.base.BaseLLMDatasetGenerator", "evidently:dataset_generator:BaseLLMDatasetGenerator")
register_type_alias(BaseDatasetGenerator, "evidently.llm.datagen.rag.BaseRagDatasetGenerator", "evidently:dataset_generator:BaseRagDatasetGenerator")
register_type_alias(BaseDatasetGenerator, "evidently.llm.datagen.rag.RagQueryDatasetGenerator", "evidently:dataset_generator:RagQueryDatasetGenerator")
register_type_alias(BaseDatasetGenerator, "evidently.llm.datagen.rag.RagResponseDatasetGenerator", "evidently:dataset_generator:RagResponseDatasetGenerator")
register_type_alias(BaseDatasetGenerator, "evidently.llm.datagen.rag.RagDatasetGenerator", "evidently:dataset_generator:RagDatasetGenerator")
register_type_alias(BaseDatasetGenerator, "evidently.llm.datagen.fewshot.FewShotDatasetGenerator", "evidently:dataset_generator:FewShotDatasetGenerator")
