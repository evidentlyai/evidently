import warnings

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
            for guard in guards.split("|"):
                span.set_attribute("evidently.guardrail.name", guard)
                span.set_attribute("evidently.guardrail.status", "passed")

    def on_exception(self, span: SpanObject, context: InterceptorContext, ex: Exception) -> bool:
        if not isinstance(ex, GuardException):
            return False
        guards = span.get_context_value("evidently.guardrails")
        if not guards:
            return False

        if isinstance(ex, GuardsException):
            for guard in guards.split("|"):
                if guard in ex.failed_guards:
                    span.set_attribute(f"evidently.guardrail.{guard}.status", "failed")
                    span.set_attribute(f"evidently.guardrail.{guard}.error", str(ex.failed_guards.get(guard)))
                else:
                    span.set_attribute(f"evidently.guardrail.{guard}.status", "passed")
        else:
            span.set_attribute(f"evidently.guardrail.{ex.guard}.name", "failed")
            span.set_attribute(f"evidently.guardrail.{ex.guard}.error", str(ex))
        return True
