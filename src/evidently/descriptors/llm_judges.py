from abc import ABC
from typing import ClassVar

from evidently.base_metric import ColumnName
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeatures
from evidently.features.llm_judge import BinaryClassificationPromptTemplate
from evidently.features.llm_judge import LLMJudge


class LLMJudgeDescriptor(FeatureDescriptor, ABC):
    name: ClassVar[str]
    template: ClassVar[BinaryClassificationPromptTemplate]

    provider: str
    model: str

    def feature(self, column_name: str) -> GeneratedFeatures:
        return LLMJudge(
            display_name=self.display_name or self.name,
            provider=self.provider,
            model=self.model,
            input_column=column_name,
            template=self.get_template(),
        )

    def for_column(self, column_name: str) -> "ColumnName":
        template = self.get_template()
        column = template.output_column if template.include_category else template.output_score_column
        return self.feature(column_name).as_column(column)

    def get_template(self) -> BinaryClassificationPromptTemplate:
        return self.template


class NegativityLLMJudge(LLMJudgeDescriptor):
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


class PIILLMJudge(LLMJudgeDescriptor):
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


class DeclineLLMJudge(LLMJudgeDescriptor):
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
