# ruff: noqa: E501
# fmt: off
from evidently.llm.datagen.base import BaseDatasetGenerator
from evidently.llm.rag.index import DataCollectionProvider
from evidently.llm.rag.splitter import Splitter
from evidently.pydantic_utils import register_type_alias

register_type_alias(DataCollectionProvider, "evidently.llm.rag.index.ChunksDataCollectionProvider", "evidently:data_collection_provider:ChunksDataCollectionProvider")
register_type_alias(DataCollectionProvider, "evidently.llm.rag.index.FileDataCollectionProvider", "evidently:data_collection_provider:FileDataCollectionProvider")
register_type_alias(Splitter, "evidently.llm.rag.splitter.LlamaIndexSplitter", "evidently:splitter:LlamaIndexSplitter")
register_type_alias(Splitter, "evidently.llm.rag.splitter.SimpleSplitter", "evidently:splitter:SimpleSplitter")

register_type_alias(BaseDatasetGenerator, "evidently.llm.datagen.base.BaseLLMDatasetGenerator", "evidently:dataset_generator:BaseLLMDatasetGenerator")
register_type_alias(BaseDatasetGenerator, "evidently.llm.datagen.rag.InputSeedDatasetGenerator", "evidently:dataset_generator:InputSeedDatasetGenerator")
register_type_alias(BaseDatasetGenerator, "evidently.llm.datagen.rag.RagDatasetGenerator", "evidently:dataset_generator:RagDatasetGenerator")
