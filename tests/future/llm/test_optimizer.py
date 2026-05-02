from unittest.mock import MagicMock

import pytest

from evidently.llm.optimization.optimizer import OptimizationConfigurationError
from evidently.llm.optimization.optimizer import OptimizerConfig
from evidently.llm.optimization.optimizer import OptimizerContext
from evidently.llm.optimization.optimizer import Params


def test_optimizer_context_set_get_param():
    """Test setting and getting parameters in OptimizerContext."""
    ctx = OptimizerContext(config=OptimizerConfig(), params={}, runs=[])
    ctx.set_param("foo", 123)
    assert ctx.params["foo"] == 123
    ctx.locked = True
    # Should be able to get param when locked
    assert ctx.get_param("foo") == 123
    # Should raise if setting param when locked
    with pytest.raises(OptimizationConfigurationError):
        ctx.set_param("bar", 456)
    # Should raise if getting param when not locked
    ctx.locked = False
    with pytest.raises(OptimizationConfigurationError):
        ctx.get_param("foo")


def test_optimizer_context_missing_param():
    """Test error on missing param with custom message."""
    ctx = OptimizerContext(config=OptimizerConfig(), params={}, runs=[])
    ctx.locked = True
    with pytest.raises(OptimizationConfigurationError, match="missing!"):
        ctx.get_param("notfound", missing_error_message="missing!")


@pytest.mark.asyncio
async def test_optimizer_context_add_log_and_get_log():
    """Test adding and retrieving logs in OptimizerContext."""
    ctx = OptimizerContext(config=OptimizerConfig(), params={}, runs=[])
    log = MagicMock()
    log.id = "logid"
    log.message.return_value = "msg"
    run = await ctx.new_run()
    run.add_log(log)
    assert run.get_log("logid") == log
    with pytest.raises(KeyError):
        run.get_log("notfound")


def test_resolve_provider_model_from_config():
    """Explicit provider/model on config are returned as-is."""
    ctx = OptimizerContext(
        config=OptimizerConfig(provider="anthropic", model="claude-3-haiku"),
        params={Params.Options: MagicMock()},
        runs=[],
    )
    ctx.locked = True
    provider, model = ctx.resolve_provider_model()
    assert provider == "anthropic"
    assert model == "claude-3-haiku"


def test_resolve_provider_model_inherits_from_executor_judge():
    """When config has no provider/model, they are inherited from the executor's judge."""
    mock_judge = MagicMock()
    mock_judge.provider = "vertex_ai"
    mock_judge.model = "gemini-2.5-flash"
    mock_executor = MagicMock()
    mock_executor.judge = mock_judge

    ctx = OptimizerContext(
        config=OptimizerConfig(),
        params={Params.Options: MagicMock(), Params.Executor: mock_executor},
        runs=[],
    )
    ctx.locked = True
    provider, model = ctx.resolve_provider_model()
    assert provider == "vertex_ai"
    assert model == "gemini-2.5-flash"


def test_resolve_provider_model_falls_back_to_openai():
    """With no config and no executor judge, defaults to openai/gpt-4o-mini."""
    ctx = OptimizerContext(
        config=OptimizerConfig(),
        params={Params.Options: MagicMock()},
        runs=[],
    )
    ctx.locked = True
    provider, model = ctx.resolve_provider_model()
    assert provider == "openai"
    assert model == "gpt-4o-mini"
