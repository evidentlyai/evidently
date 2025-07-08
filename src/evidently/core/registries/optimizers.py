# ruff: noqa: E501
# fmt: off
from evidently.llm.optimization.optimizer import OptimizerConfig
from evidently.llm.optimization.optimizer import OptimizerLog
from evidently.llm.optimization.prompts import OptimizationScorer
from evidently.llm.optimization.prompts import PromptExecutor
from evidently.llm.optimization.prompts import PromptOptimizerStrategy
from evidently.pydantic_utils import register_type_alias

register_type_alias(OptimizerConfig, "evidently.llm.optimization.prompts.PromptOptimizerConfig", "evidently:optimizer_config:PromptOptimizerConfig")
register_type_alias(OptimizerLog, "evidently.llm.optimization.prompts.PromptExecutionLog", "evidently:optimizer_log:PromptExecutionLog")
register_type_alias(OptimizerLog, "evidently.llm.optimization.prompts.PromptOptimizationLog", "evidently:optimizer_log:PromptOptimizationLog")
register_type_alias(OptimizerLog, "evidently.llm.optimization.prompts.PromptScoringLog", "evidently:optimizer_log:PromptScoringLog")
register_type_alias(OptimizationScorer, "evidently.llm.optimization.prompts.AccuracyScorer", "evidently:optimizer_scorer:AccuracyScorer")
register_type_alias(OptimizationScorer, "evidently.llm.optimization.prompts.BinaryJudgeScorer", "evidently:optimizer_scorer:BinaryJudgeScorer")
register_type_alias(PromptExecutor, "evidently.llm.optimization.prompts.CallablePromptExecutor", "evidently:prompt_executor:CallablePromptExecutor")
register_type_alias(PromptExecutor, "evidently.llm.optimization.prompts.LLMJudgePromptExecutor", "evidently:prompt_executor:LLMJudgePromptExecutor")
register_type_alias(PromptOptimizerStrategy, "evidently.llm.optimization.prompts.FeedbackStrategy", "evidently:prompt_optimizer_strategy:FeedbackStrategy")
register_type_alias(PromptOptimizerStrategy, "evidently.llm.optimization.prompts.SimplePromptOptimizer", "evidently:prompt_optimizer_strategy:SimplePromptOptimizer")
