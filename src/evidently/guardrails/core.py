import abc


class GuardException(Exception):
    pass


class GuardrailBase:
    def __init__(self):
        pass

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
