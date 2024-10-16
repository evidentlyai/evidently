from evidently.errors import EvidentlyError


class EvidentlyLLMError(EvidentlyError):
    pass


class LLMResponseParseError(EvidentlyLLMError):
    pass


class LLMRequestError(EvidentlyLLMError):
    pass
