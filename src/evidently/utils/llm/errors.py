from evidently.errors import EvidentlyError


class EvidentlyLLMError(EvidentlyError):
    pass


class LLMResponseParseError(EvidentlyLLMError):
    pass


class LLMRequestError(EvidentlyLLMError):
    def __init__(self, message: str, original_error: Exception = None):
        super().__init__(message)
        self.original_error = original_error


class LLMRateLimitError(LLMRequestError):
    pass
