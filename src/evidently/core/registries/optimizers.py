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
register_type_alias(OptimizationScorer, "evidently.llm.optimization.prompts.BinaryJudgeScorer", "evidently:optimizer_scorer:BinaryJudgeScorer")
register_type_alias(PromptExecutor, "evidently.llm.optimization.prompts.CallablePromptExecutor", "evidently:prompt_executor:CallablePromptExecutor")
register_type_alias(PromptExecutor, "evidently.llm.optimization.prompts.LLMJudgePromptExecutor", "evidently:prompt_executor:LLMJudgePromptExecutor")
register_type_alias(PromptOptimizerStrategy, "evidently.llm.optimization.prompts.FeedbackStrategy", "evidently:prompt_optimizer_strategy:FeedbackStrategy")
register_type_alias(PromptOptimizerStrategy, "evidently.llm.optimization.prompts.SimplePromptOptimizer", "evidently:prompt_optimizer_strategy:SimplePromptOptimizer")

register_type_alias(OptimizationScorer, "evidently.llm.optimization.prompts.NoopOptimizationScorer", "evidently:optimizer_scorer:NoopOptimizationScorer")
register_type_alias(PromptExecutor, "evidently.llm.optimization.prompts.NoopPromptExecutor", "evidently:prompt_executor:NoopPromptExecutor")

register_type_alias(OptimizationScorer, "evidently.llm.optimization.scorers.AccuracyScorer", "evidently:optimizer_scorer:AccuracyScorer")
register_type_alias(OptimizationScorer, "evidently.llm.optimization.scorers.BalancedAccuracyScorer", "evidently:optimizer_scorer:BalancedAccuracyScorer")
register_type_alias(OptimizationScorer, "evidently.llm.optimization.scorers.BrierScoreScorer", "evidently:optimizer_scorer:BrierScoreScorer")
register_type_alias(OptimizationScorer, "evidently.llm.optimization.scorers.CohenKappaScorer", "evidently:optimizer_scorer:CohenKappaScorer")
register_type_alias(OptimizationScorer, "evidently.llm.optimization.scorers.F1Scorer", "evidently:optimizer_scorer:F1Scorer")
register_type_alias(OptimizationScorer, "evidently.llm.optimization.scorers.LogLossScorer", "evidently:optimizer_scorer:LogLossScorer")
register_type_alias(OptimizationScorer, "evidently.llm.optimization.scorers.MCCScorer", "evidently:optimizer_scorer:MCCScorer")
register_type_alias(OptimizationScorer, "evidently.llm.optimization.scorers.PrecisionScorer", "evidently:optimizer_scorer:PrecisionScorer")
register_type_alias(OptimizationScorer, "evidently.llm.optimization.scorers.R2Scorer", "evidently:optimizer_scorer:R2Scorer")
register_type_alias(OptimizationScorer, "evidently.llm.optimization.scorers.RecallScorer", "evidently:optimizer_scorer:RecallScorer")
register_type_alias(OptimizationScorer, "evidently.llm.optimization.scorers.RocAucScorer", "evidently:optimizer_scorer:RocAucScorer")
register_type_alias(OptimizerLog, "evidently.llm.optimization.optimizer.LLMCallOptimizerLog", "evidently:optimizer_log:LLMCallOptimizerLog")
register_type_alias(OptimizerLog, "evidently.llm.optimization.prompts.InitGenerationLog", "evidently:optimizer_log:InitGenerationLog")
register_type_alias(OptimizerLog, "evidently.llm.optimization.prompts.PromptOptimizationResultLog", "evidently:optimizer_log:PromptOptimizationResultLog")
register_type_alias(PromptExecutor, "evidently.llm.optimization.prompts.BlankLLMJudge", "evidently:prompt_executor:BlankLLMJudge")
