from evidently.errors import EvidentlyError


class EvidentlyLLMError(EvidentlyError):
    pass


class LLMResponseParseError(EvidentlyLLMError):
    def __init__(self, message: str, response):
        self.message = message
        self.response = response

    def get_message(self):
        return f"{self.__class__.__name__}: {self.message}"


class LLMRequestError(EvidentlyLLMError):
    def __init__(self, message: str, original_error: Exception = None):
        super().__init__(message)
        self.original_error = original_error


class LLMRateLimitError(LLMRequestError):
    pass
