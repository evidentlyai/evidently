from typing import Type

from evidently.pydantic_utils import FrozenBaseMeta
from evidently.pydantic_utils import FrozenBaseModel


class OptionField:
    def __init__(self, model: Type["Option"], field_name: str):
        self.model = model
        self.field_name = field_name

    def __repr__(self):
        return f"{self.model.__name__}.{self.field_name}"


class OptionMeta(FrozenBaseMeta):
    def __getattr__(self, item):
        try:
            return super().__getattr__(item)
        except AttributeError as e:
            if item in self.__fields__:
                return OptionField(self, item)
            raise e


class Option(FrozenBaseModel, metaclass=OptionMeta):
    pass


def main():
    class MyOption(Option):
        f: str

    print(MyOption.f)


if __name__ == "__main__":
    main()
