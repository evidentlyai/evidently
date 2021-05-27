import abc


class Preprocess:
    @abc.abstractmethod
    def preprocess(self):
        raise NotImplementedError()
