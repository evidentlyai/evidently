import abc
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from evidently.utils.data_operations import DatasetColumns

TObject = TypeVar("TObject")


class BaseGenerator(Generic[TObject]):
    """Base class for tests and metrics generator creation

    To create a new generator:
        - inherit a class from the base class
        - implement `generate_tests` method and return a list of test objects from it

    A Suite or a Report will call the method and add generated tests to its list instead of the generator object.

    You can use `columns_info` parameter in `generate` for getting data structure meta info like columns list.

    For example:
        if you want to create a test generator for 50, 90, 99 quantiles tests
        for all numeric columns with default condition, by reference quantiles

    class TestQuantiles(BaseTestGenerator):
        def generate(self, columns_info: DatasetColumns) -> List[TestValueQuantile]:
            return [
                TestValueQuantile(column_name=name, quantile=quantile)
                for quantile in (0.5, 0.9, 0.99)
                for name in columns_info.num_feature_names
            ]

    Do not forget set correct test type for `generate` return value
    """

    @abc.abstractmethod
    def generate(self, columns_info: DatasetColumns) -> List[TObject]:
        raise NotImplementedError()


def make_generator_by_columns(
    base_class: Type,
    columns: Optional[Union[str, list]] = None,
    parameters: Optional[Dict] = None,
) -> BaseGenerator:
    """Create a test generator for a columns list with a test class.

    Base class is specified with `base_class` parameter.
    If the test have no "column_name" parameter - TypeError will be raised.

    Columns list can be defined with parameter `columns`.
    If it is a list - just use it as a list of the columns.
    If `columns` is a string, it can be one of values:
    - "all" - make tests for all columns, including target/prediction columns
    - "num" - for numeric features
    - "cat" - for category features
    - "features" - for all features, not target/prediction columns.
    None value is the same as "all".
    If `columns` is string, and it is not one of the values, ValueError will be raised.

    `parameters` is used for specifying other parameters for each object, it is the same for all generated objects.
    """
    if parameters is None:
        parameters_for_generation: Dict = {}

    else:
        parameters_for_generation = parameters

    class ColumnsGenerator(BaseGenerator):
        def generate(self, columns_info: DatasetColumns) -> List[TObject]:
            nonlocal parameters_for_generation
            result = []

            if isinstance(columns, list):
                columns_for_generation = columns

            elif columns == "all" or columns is None:
                columns_for_generation = columns_info.get_all_columns_list()

            elif columns == "cat":
                columns_for_generation = columns_info.cat_feature_names

            elif columns == "num":
                columns_for_generation = columns_info.num_feature_names

            elif columns == "features":
                columns_for_generation = columns_info.get_all_features_list(
                    include_datetime_feature=True
                )

            else:
                raise ValueError("Incorrect parameter 'columns' for test generator")

            for column_name in columns_for_generation:
                parameters_for_generation["column_name"] = column_name
                # ignore possible parameters incompatibility
                # we cannot guarantee that a base class has column_name parameter
                # if it has not, type error will ve raised
                try:
                    result.append(base_class(**parameters_for_generation))  # type: ignore

                except TypeError as error:
                    raise TypeError(
                        f"Cannot generate {base_class.__name__}. Error: {error}"
                    )

            return result

    return ColumnsGenerator()
