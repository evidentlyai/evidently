import warnings
from typing import Optional

from evidently.guardrails import GuardException
from evidently.guardrails.core import GuardsException

try:
    import tracely
    from tracely import SpanObject
    from tracely.interceptors import InterceptorContext
except ImportError:
    warnings.warn("tracely not installed, but required to use traces in guardrails")
    raise


class GuardrailsInterceptor(tracely.Interceptor):
    def before_call(self, span: SpanObject, context: InterceptorContext, *args, **kwargs):
        pass

    def after_call(self, span: SpanObject, context: InterceptorContext, return_value):
        guards = span.get_context_value("evidently.guardrails")
        if guards:
            for idx, guard in enumerate(guards):
                self._set_span_for_guard(span, f"g_{idx}", guard.name(), "passed", None)

    def on_exception(self, span: SpanObject, context: InterceptorContext, ex: Exception) -> bool:
        if not isinstance(ex, GuardException):
            return False
        guards = span.get_context_value("evidently.guardrails")
        if not guards:
            return False

        if isinstance(ex, GuardsException):
            for idx, guard in enumerate(guards):
                if guard in ex.failed_guards:
                    self._set_span_for_guard(span, f"g_{idx}", guard.name(), "failed", str(ex.failed_guards.get(guard)))
                else:
                    self._set_span_for_guard(span, f"g_{idx}", guard.name(), "passed", None)
        else:
            self._set_span_for_guard(span, "guard", guards[0].name(), "failed", str(ex))
        return True

    def _set_span_for_guard(self, span: SpanObject, guard_id: str, guard_name: str, status: str, error: Optional[str]):
        span.set_attribute(f"evidently.guardrail.{guard_id}.name", guard_name)
        span.set_attribute(f"evidently.guardrail.{guard_id}.status", status)
        if error:
            span.set_attribute(f"evidently.guardrail.{guard_id}.error", error)
