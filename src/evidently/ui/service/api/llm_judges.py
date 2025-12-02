from typing import List

from litestar import Router
from litestar import get
from litestar import post

from evidently._pydantic_compat import BaseModel
from evidently.legacy.descriptors import BiasLLMEval
from evidently.legacy.descriptors import CompletenessLLMEval
from evidently.legacy.descriptors import ContextQualityLLMEval
from evidently.legacy.descriptors import CorrectnessLLMEval
from evidently.legacy.descriptors import DeclineLLMEval
from evidently.legacy.descriptors import FaithfulnessLLMEval
from evidently.legacy.descriptors import NegativityLLMEval
from evidently.legacy.descriptors import PIILLMEval
from evidently.legacy.descriptors import ToxicityLLMEval
from evidently.legacy.features.llm_judge import BaseLLMPromptTemplate
from evidently.legacy.features.llm_judge import BinaryClassificationPromptTemplate


class LLMPromptTemplateModel(BaseModel):
    name: str
    template: BinaryClassificationPromptTemplate
    prompt: str
    output_format: str

    @classmethod
    def from_llm_template(cls, name: str, template: BinaryClassificationPromptTemplate):
        output_format = template.get_output_format().render()
        prompt = template.prepare().template.split(output_format)[0]
        return LLMPromptTemplateModel(name=name, template=template, prompt=prompt, output_format=output_format)


@get("/templates")
async def get_llm_judges_templates() -> List[LLMPromptTemplateModel]:
    return [
        LLMPromptTemplateModel.from_llm_template(NegativityLLMEval.name, NegativityLLMEval.template),
        LLMPromptTemplateModel.from_llm_template(PIILLMEval.name, PIILLMEval.template),
        LLMPromptTemplateModel.from_llm_template(DeclineLLMEval.name, DeclineLLMEval.template),
        LLMPromptTemplateModel.from_llm_template(ToxicityLLMEval.name, ToxicityLLMEval.template),
        LLMPromptTemplateModel.from_llm_template(BiasLLMEval.name, BiasLLMEval.template),
        LLMPromptTemplateModel.from_llm_template(ContextQualityLLMEval.name, ContextQualityLLMEval.template),
        LLMPromptTemplateModel.from_llm_template(CorrectnessLLMEval.name, CorrectnessLLMEval.template),
        LLMPromptTemplateModel.from_llm_template(CompletenessLLMEval.name, CompletenessLLMEval.template),
        LLMPromptTemplateModel.from_llm_template(FaithfulnessLLMEval.name, FaithfulnessLLMEval.template),
    ]


class PromptTemplateRequest(BaseModel):
    template: BaseLLMPromptTemplate


@post("/prompt_template")
async def get_prompt_template(data: PromptTemplateRequest) -> str:
    return data.template.prepare().template


def llm_judges_router() -> Router:
    return Router(
        path="/llm_judges",
        route_handlers=[
            get_llm_judges_templates,
            get_prompt_template,
        ],
    )
