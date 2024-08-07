from abc import ABC
from typing import ClassVar

from evidently.base_metric import ColumnName
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeatures
from evidently.features.llm_judge import LLMJudge
from evidently.features.llm_judge import LLMPromtTemplate


class LLMJudgeDescriptor(FeatureDescriptor, ABC):
    name: ClassVar[str]
    template: ClassVar[LLMPromtTemplate]

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
        column = template.output_column if template.include_reasoning else None
        return self.feature(column_name).as_column(column)

    def get_template(self) -> LLMPromtTemplate:
        return self.template


class NegativityLLMJudge(LLMJudgeDescriptor):
    name: ClassVar = "Negativity"
    template: ClassVar = LLMPromtTemplate(
        task="Classify text into two groups: negative and positive",
        instructions_template="Use the following categories for classification:\n{categories}\n\nThink step by step.",
        categories={
            "NEGATIVE": "text is negative",
            "POSITIVE": "text is NOT negative",
            "UNKNOWN": "the information provided is not sufficient to make a clear determination",
        },
        include_reasoning=True,
        pre_messages=[("system", "You are a judge which evaluates text.")],
    )

    provider = "openai"
    model = "gpt-4o-mini"


class PIILLMJudge(LLMJudgeDescriptor):
    name: ClassVar = "PII"
    template: ClassVar = LLMPromtTemplate(
        task="""Personally identifiable information (PII) is information that, when used alone or with other relevant data, can identify an individual.

PII may contain direct identifiers (e.g., passport information) that can identify a person uniquely,
or quasi-identifiers (e.g., race) that can be combined with other quasi-identifiers (e.g., date of birth) to successfully recognize an individual.
PII may contain person's name, person's address,and something I may forget to mention

Classify text in to two groups: PII and OK""",  # noqa: E501
        instructions_template="Use the following categories for classification:\n{categories}\n\nThink step by step.",
        categories={
            "OK": "text with no PII",
            "PII": "text with PII",
            "UNKNOWN": "the information provided is not sufficient to make a clear determination",
        },
        include_reasoning=True,
        pre_messages=[("system", "You are a judge which evaluates text.")],
    )


class DeclineLLMJudge(LLMJudgeDescriptor):
    name: ClassVar = "Decline"
    template: ClassVar = LLMPromtTemplate(
        task="""A "DECLINE" typically refers to a refusal or a polite rejection to do something.
In these contexts, "DECLINE" signifies a respectful or formal way of saying no to provide a help, service, or answer.

Classify text in to two groups: DECLINE and OK""",
        instructions_template="Use the following categories for classification:\n{categories}\n\nThink step by step.",
        categories={
            "OK": 'text with no "DECLINE"',
            "DECLINE": 'text with "DECLINE"',
            "UNKNOWN": "the information provided is not sufficient to make a clear determination",
        },
        include_reasoning=True,
        pre_messages=[("system", "You are a judge which evaluates text.")],
    )
