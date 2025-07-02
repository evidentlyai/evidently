import re
from abc import ABC
from abc import abstractmethod
from typing import ClassVar
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from evidently import Dataset
from evidently.core.datasets import LLMClassification
from evidently.legacy.features.llm_judge import BinaryClassificationPromptTemplate
from evidently.legacy.features.llm_judge import LLMJudge
from evidently.legacy.options.base import AnyOptions
from evidently.legacy.options.base import Options
from evidently.legacy.utils.llm.base import LLMMessage
from evidently.legacy.utils.sync import async_to_sync
from evidently.llm.optimization.optimizer import BaseOptimizer
from evidently.llm.optimization.optimizer import Inputs
from evidently.llm.optimization.optimizer import OptimizerConfig
from evidently.llm.optimization.optimizer import OptimizerContext
from evidently.llm.optimization.optimizer import OptimizerLog
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel


class PromptOptimizationLog(OptimizerLog):
    input_prompt: str
    optimizer_prompt: str
    new_prompt: str
    input_tokens: int
    output_tokens: str


class PromptOptimizerStrategy(AutoAliasMixin, EvidentlyBaseModel, ABC):
    __alias_type__: ClassVar = "prompt_optimizer_strategy"

    @abstractmethod
    async def run(self, prompt: str, state: OptimizerContext) -> PromptOptimizationLog:
        raise NotImplementedError()


class PromptOptimizerConfig(OptimizerConfig):
    strategy: PromptOptimizerStrategy


class PromptEvaluationLog(OptimizerLog):
    prompt: str
    data: Dict[Inputs, Optional[pd.Series]]


class PromptEvaluator(AutoAliasMixin, EvidentlyBaseModel, ABC):
    __alias_type__: ClassVar = "prompt_evaluator"

    @abstractmethod
    def evaluate(self, prompt: str, dataset: Dataset, options: Options) -> PromptEvaluationLog:
        raise NotImplementedError()

    @abstractmethod
    def get_base_prompt(self) -> str:
        raise NotImplementedError()


class BinaryLLMJudgePromptEvaluator(PromptEvaluator):
    judge: LLMJudge

    def evaluate(self, prompt: str, dataset: Dataset, options: Options) -> PromptEvaluationLog:
        template = self.template
        judge = self.judge.update(template=template.update(criteria=prompt))
        generated = judge.generate_features_renamed(
            dataset.as_dataframe(), data_definition=dataset.data_definition, options=options
        )
        cols = judge.list_columns()
        category = generated[[c.name for c in cols if "category" in c.name][0]] if template.include_category else None
        score = generated[[c.name for c in cols if "score" in c.name][0]] if template.include_score else None
        reasoning = (
            generated[[c.name for c in cols if "reasoning" in c.name][0]] if template.include_reasoning else None
        )
        return PromptEvaluationLog(
            prompt=prompt,
            data={
                Inputs.Pred: category,
                Inputs.PredReasoning: reasoning,
                Inputs.PredScores: score,
            },
        )

    @property
    def template(self) -> BinaryClassificationPromptTemplate:
        t = self.judge.template
        assert isinstance(t, BinaryClassificationPromptTemplate)
        return t

    def get_base_prompt(self) -> str:
        return self.template.criteria


AnyPromptEvaluator = Union[PromptEvaluator, LLMJudge]


def get_prompt_evaluator(value: AnyPromptEvaluator) -> PromptEvaluator:
    if isinstance(value, PromptEvaluator):
        return value
    if isinstance(value, LLMJudge) and isinstance(value.template, BinaryClassificationPromptTemplate):
        return BinaryLLMJudgePromptEvaluator(judge=value)
    raise NotImplementedError(f"Not implemented for {value.__class__.__name__}")


class PromptScoringLog(OptimizerLog):
    scores: Dict[str, float]


class OptimizationScorer(AutoAliasMixin, EvidentlyBaseModel, ABC):
    __alias_type__: ClassVar = "optimizer_scorer"

    @abstractmethod
    def score(self, context: OptimizerContext, evaluation: PromptEvaluationLog) -> Optional[float]:
        raise NotImplementedError()


class AccuracyScorer(OptimizationScorer):
    def score(self, context: OptimizerContext, evaluation: PromptEvaluationLog) -> Optional[float]:
        if Inputs.Target not in context.inputs or Inputs.Pred not in evaluation.data:
            # todo: error?
            return None
        target = context.inputs[Inputs.Target]
        result = evaluation.data[Inputs.Pred]
        return (result == target).mean()


class PromptOptimizer(BaseOptimizer[PromptOptimizerConfig]):
    def __init__(self, name: str, strategy: PromptOptimizerStrategy, checkpoint_path: Optional[str] = None):
        super().__init__(name, PromptOptimizerConfig(strategy=strategy), checkpoint_path=checkpoint_path)

    def run_sync(
        self,
        dataset: Dataset,
        evaluator: AnyPromptEvaluator,
        scorer: Optional[OptimizationScorer],
        options: AnyOptions = None,
    ) -> Optional[PromptOptimizationLog]:
        return async_to_sync(self.run(dataset, evaluator, scorer, options))

    async def run(
        self,
        dataset: Dataset,
        evaluator: AnyPromptEvaluator,
        scorer: Optional[OptimizationScorer],
        options: AnyOptions = None,
    ) -> Optional[PromptOptimizationLog]:
        self.set_input_dataset(dataset)
        evaluator = get_prompt_evaluator(evaluator)
        self.set_input(Inputs.Evaluator, evaluator)
        self.set_input(Inputs.Options, Options.from_any_options(options))
        if scorer is None:
            scorer = AccuracyScorer()
        self.set_input(Inputs.Scorer, scorer)

        await self.resume()

    async def resume(self):
        evaluator = self.get_input(Inputs.Evaluator, PromptEvaluator)
        scorer = self.get_input(Inputs.Scorer, OptimizationScorer)
        prompt = evaluator.get_base_prompt()

        self._eval_score(prompt, evaluator, scorer)
        opt_log = await self.config.strategy.run(prompt, self.context)
        self.context.add_log(opt_log)
        prompt = opt_log.new_prompt
        self._eval_score(prompt, evaluator, scorer)

    def _eval_score(self, prompt: str, evaluator: PromptEvaluator, scorer: OptimizationScorer):
        eval_log = evaluator.evaluate(prompt, self.dataset, self.context.options)
        self.context.add_log(eval_log)
        score = scorer.score(self.context, eval_log)
        score_log = PromptScoringLog(scores={scorer.__class__.__name__: score})
        self.context.add_log(score_log)

    @property
    def config(self) -> PromptOptimizerConfig:
        return self.context.config

    @property
    def dataset(self) -> Dataset:
        clf = self.get_input(Inputs.LLMClassification, LLMClassification)
        return Dataset.from_pandas(
            pd.DataFrame(
                {
                    clf.values: list(self.get_input(Inputs.Values, pd.Series)),
                    clf.target: list(self.get_input(Inputs.Target, pd.Series)),
                }
            )
        )

    def set_input_dataset(self, dataset: Dataset):
        dd = dataset.data_definition
        clf = dd.llm
        assert isinstance(clf, LLMClassification)
        self.set_input(Inputs.Values, dataset.column(clf.values).data)
        self.set_input(Inputs.Target, dataset.column(clf.target).data)
        self.set_input(Inputs.LLMClassification, clf)
        if clf.reasoning is not None:
            self.set_input(Inputs.Reasoning, dataset.column(clf.reasoning).data)
        if clf.predictions is not None:
            self.set_input(Inputs.Pred, dataset.column(clf.predictions).data)
        if clf.prediction_reasoning is not None:
            self.set_input(Inputs.PredReasoning, dataset.column(clf.prediction_reasoning).data)


def get_tag(value, tag_name):
    match = re.search(rf"<{tag_name}>(.*?)</{tag_name}>", value, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


class SimplePromptOptimizer(PromptOptimizerStrategy):
    optimizer_prompt: str = (
        "I'm using llm to classify texts. Here is my prompt <prompt>{prompt}</prompt>. "
        "Please make it better so I can have better classification quality. "
        "Do not add new classes. "
        "Return new version inside <new_prompt> tag"
    )
    return_tag: str = "new_prompt"

    async def run(self, prompt: str, state: OptimizerContext) -> PromptOptimizationLog:
        response = await state.llm_wrapper.complete([LLMMessage.user(self.optimizer_prompt.format(prompt=prompt))])
        new_prompt = get_tag(response.result, self.return_tag)
        return PromptOptimizationLog(
            input_prompt=prompt,
            optimizer_prompt=self.optimizer_prompt,
            new_prompt=new_prompt,
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
        )


class FeedbackStrategy(PromptOptimizerStrategy):
    add_feedback_prompt = (
        "I ran LLM judge for some inputs and it made some mistakes. "
        "Here is my original prompt <prompt>{prompt}</prompt>. "
        "And here are rows where LLM made mistakes: <rows>{rows}</rows>. "
        "Please update my prompt to improve LLM judge quality. "
        "Generalize examples to not overfit on them. "
        "Return new prompt inside <new_prompt> tag"
    )
    row_template = """<input>{input}</input>
    <true_label>{true_label}</true_label>
    <llm_judge_label>{llm_judge_label}</llm_judge_label>
    <human_reasoning>{human_reasoning}</human_reasoning>
    <llm_judge_reasoning>{llm_judge_reasoning}</llm_judge_reasoning>
    """

    async def run(self, prompt: str, state: OptimizerContext) -> PromptOptimizationLog:
        mistakes = state.mistakes
        rows = "\n".join(
            self.row_template.format(
                input=val,
                true_label=gt,
                llm_judge_label=pred,
                human_reasoning=gt_reason,
                llm_judge_reasoning=pred_reason,
            )
            for val, gt, pred, gt_reason, pred_reason in zip(
                mistakes.values, mistakes.target, mistakes.preds, mistakes.reasoning, mistakes.preds_reasoning
            )
        )
        return await SimplePromptOptimizer(
            optimizer_prompt=self.add_feedback_prompt.format(prompt="{prompt}", rows=rows)
        ).run(prompt, state)
