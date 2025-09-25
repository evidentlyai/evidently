import abc
from typing import Dict
from typing import List


class GuardrailBase:
    def __init__(self):
        pass

    def name(self) -> str:
        return self.__class__.__name__

    @abc.abstractmethod
    def validate(self, data: str):
        """
        validate input to meet a criteria
        Args:
            data: input data to check against criteria

        Returns:
            None
        Raises:
            GuardException: raised if validation fails
        """
        raise NotImplementedError()


class GuardException(Exception):
    guard: GuardrailBase

    def __init__(self, guard: GuardrailBase, message: str = "") -> None:
        self.guard = guard
        self.message = message

    def __str__(self):
        return f"Guard {self.guard.name()} validation failed: {self.message}"


class AggregationGuardrail(GuardrailBase):
    def validate(self, data: str):
        pass

    def name(self) -> str:
        return "Aggregation"


class GuardsException(GuardException):
    guard = AggregationGuardrail()
    failed_guards: Dict[GuardrailBase, GuardException]

    def __init__(self, failed_guards: Dict[GuardrailBase, GuardException]):
        self.failed_guards = failed_guards

    def __str__(self):
        return f"Multiple guards validation failed: {', '.join([g.name() for g in self.failed_guards.keys()])}."


def validate_guards(data: str, guards: List[GuardrailBase]):
    failed = {}
    for guard in guards:
        try:
            guard.validate(data)
        except GuardException as e:
            failed[e.guard] = e
    if len(failed) > 0:
        raise GuardsException(failed)
