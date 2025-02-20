class EvidentlyError(Exception):
    def get_message(self):
        return f"{self.__class__.__name__}: {self}"
