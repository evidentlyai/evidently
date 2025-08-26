from evidently.guardrails import GuardException
from evidently.guardrails.core import GuardrailBase
from evidently.legacy.descriptors.llm_judges import PIILLMEval
from evidently.legacy.options.base import Options
from evidently.llm.utils.wrapper import LLMRequest
from evidently.llm.utils.wrapper import get_llm_wrapper


class PIICheck(GuardrailBase):
    def __init__(self):
        super().__init__()

    def validate(self, data: str):
        piillm_eval = PIILLMEval()
        request = LLMRequest(
            messages=piillm_eval.template.get_messages({"input": data}),
            response_parser=piillm_eval.template.get_parser(),
            response_type=dict,
        )
        response = get_llm_wrapper(piillm_eval.provider, piillm_eval.model, Options()).run_sync(request)
        if response.get("category") != "OK":
            raise GuardException("PII Check failed: {}".format(response.get("reasoning")))
