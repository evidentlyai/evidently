from unittest.mock import MagicMock

import pytest

from evidently.llm.optimization.optimizer import OptimizationConfigurationError
from evidently.llm.optimization.optimizer import OptimizerConfig
from evidently.llm.optimization.optimizer import OptimizerContext


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
