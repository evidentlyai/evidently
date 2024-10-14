from evidently.experimental.dataset_generators.base import BaseDatasetGenerator
from evidently.experimental.dataset_generators.llm.index import DataCollectionProvider
from evidently.experimental.dataset_generators.llm.splitter import Splitter
from evidently.pydantic_utils import register_type_alias
from evidently.utils.llm.prompts import PromptTemplate

register_type_alias(
    BaseDatasetGenerator,
    "evidently.experimental.dataset_generators.llm.questions.QADatasetFromSeedGenerator",
    "evidently:dataset_generator:QADatasetFromSeedGenerator",
)
register_type_alias(
    BaseDatasetGenerator,
    "evidently.experimental.dataset_generators.llm.questions.QADatasetGenerator",
    "evidently:dataset_generator:QADatasetGenerator",
)
register_type_alias(
    DataCollectionProvider,
    "evidently.experimental.dataset_generators.llm.index.ChunksDataCollectionProvider",
    "evidently:data_collecton_provider:ChunksDataCollectionProvider",
)
register_type_alias(
    DataCollectionProvider,
    "evidently.experimental.dataset_generators.llm.index.FileDataCollectionProvider",
    "evidently:data_collecton_provider:FileDataCollectionProvider",
)

register_type_alias(
    PromptTemplate,
    "evidently.experimental.dataset_generators.llm.prompts.BaselineAnswerPromptTemplate",
    "evidently:prompt_template:BaselineAnswerPromptTemplate",
)
register_type_alias(
    PromptTemplate,
    "evidently.experimental.dataset_generators.llm.prompts.NaiveQuestionsFromContextPromptTemplate",
    "evidently:prompt_template:NaiveQuestionsFromContextPromptTemplate",
)
register_type_alias(
    PromptTemplate,
    "evidently.experimental.dataset_generators.llm.prompts.QuestionsFromContextPromptTemplate",
    "evidently:prompt_template:QuestionsFromContextPromptTemplate",
)
register_type_alias(
    PromptTemplate,
    "evidently.experimental.dataset_generators.llm.prompts.QuestionsFromSeedPromptTemplate",
    "evidently:prompt_template:QuestionsFromSeedPromptTemplate",
)
register_type_alias(
    PromptTemplate,
    "evidently.experimental.dataset_generators.llm.prompts.ReformulateQuestionPromptTemplate",
    "evidently:prompt_template:ReformulateQuestionPromptTemplate",
)
register_type_alias(
    PromptTemplate,
    "evidently.experimental.dataset_generators.llm.prompts.SimpleQuestionPromptTemplate",
    "evidently:prompt_template:SimpleQuestionPromptTemplate",
)
register_type_alias(
    Splitter,
    "evidently.experimental.dataset_generators.llm.splitter.LlamaIndexSplitter",
    "evidently:splitter:LlamaIndexSplitter",
)
register_type_alias(
    Splitter,
    "evidently.experimental.dataset_generators.llm.splitter.SimpleSplitter",
    "evidently:splitter:SimpleSplitter",
)
