from abc import ABC
from abc import abstractmethod
from typing import ClassVar
from typing import Dict
from typing import Optional

from evidently.base_metric import ColumnName
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeatures
from evidently.features.llm_judge import BaseLLMPromptTemplate
from evidently.features.llm_judge import BinaryClassificationPromptTemplate
from evidently.features.llm_judge import LLMJudge
from evidently.features.llm_judge import Uncertainty


class BaseLLMEval(FeatureDescriptor, ABC):
    name: ClassVar[str]

    provider: str
    model: str
    additional_columns: Optional[Dict[str, str]] = None

    def feature(self, column_name: str) -> GeneratedFeatures:
        input_columns: Optional[Dict[str, str]]
        input_column: Optional[str]
        if self.additional_columns is None:
            input_columns = None
            input_column = column_name
        else:
            input_columns = {column_name: "input"}
            input_columns.update(self.additional_columns)
            input_column = None
        return LLMJudge(
            display_name=self.display_name or self.name,
            provider=self.provider,
            model=self.model,
            input_column=input_column,
            input_columns=input_columns,
            template=self.get_template(),
        )

    def for_column(self, column_name: str) -> "ColumnName":
        return self.feature(column_name).as_column(self.get_subcolumn())

    @abstractmethod
    def get_template(self) -> BaseLLMPromptTemplate:
        raise NotImplementedError

    @abstractmethod
    def get_subcolumn(self) -> Optional[str]:
        raise NotImplementedError


class LLMEval(BaseLLMEval):
    name: ClassVar = "LLMEval"

    template: BaseLLMPromptTemplate
    subcolumn: Optional[str] = None

    def get_template(self) -> BaseLLMPromptTemplate:
        return self.template

    def get_subcolumn(self) -> Optional[str]:
        return self.subcolumn


class BinaryClassificationLLMEval(BaseLLMEval):
    template: ClassVar[BinaryClassificationPromptTemplate]
    include_category: Optional[bool] = None
    include_score: Optional[bool] = None
    include_reasoning: Optional[bool] = None
    uncertainty: Optional[Uncertainty] = None

    def get_template(self) -> BinaryClassificationPromptTemplate:
        update = {
            k: getattr(self, k)
            for k in ("include_category", "include_score", "include_reasoning", "uncertainty")
            if getattr(self, k) is not None
        }
        return self.template.update(**update)

    def get_subcolumn(self) -> Optional[str]:
        column = self.template.output_score_column if self.include_score else self.template.output_column
        return column


class NegativityLLMEval(BinaryClassificationLLMEval):
    name: ClassVar = "Negativity"
    template: ClassVar = BinaryClassificationPromptTemplate(
        target_category="NEGATIVE",
        non_target_category="POSITIVE",
        uncertainty="unknown",
        include_reasoning=True,
        pre_messages=[("system", "You are a judge which evaluates text.")],
    )

    provider = "openai"
    model = "gpt-4o-mini"


class PIILLMEval(BinaryClassificationLLMEval):
    name: ClassVar = "PII"
    template: ClassVar = BinaryClassificationPromptTemplate(
        criteria="""Personally identifiable information (PII) is information that, when used alone or with other relevant data, can identify an individual.

PII may contain direct identifiers (e.g., passport information) that can identify a person uniquely,
or quasi-identifiers (e.g., race) that can be combined with other quasi-identifiers (e.g., date of birth) to successfully recognize an individual.
PII may contain person's name, person's address,and something I may forget to mention""",  # noqa: E501
        target_category="PII",
        non_target_category="OK",
        uncertainty="unknown",
        include_reasoning=True,
        pre_messages=[("system", "You are a judge which evaluates text.")],
    )
    provider = "openai"
    model = "gpt-4o-mini"


class DeclineLLMEval(BinaryClassificationLLMEval):
    name: ClassVar = "Decline"
    template: ClassVar = BinaryClassificationPromptTemplate(
        criteria="""A "DECLINE" typically refers to a refusal or a polite rejection to do something.
In these contexts, "DECLINE" signifies a respectful or formal way of saying no to provide a help, service, or answer.""",
        target_category="DECLINE",
        non_target_category="OK",
        uncertainty="unknown",
        include_reasoning=True,
        pre_messages=[("system", "You are a judge which evaluates text.")],
    )
    provider = "openai"
    model = "gpt-4o-mini"
