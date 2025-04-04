from evidently.legacy.options import ColorOptions
from evidently.legacy.options.base import Options
from evidently.legacy.options.color_scheme import GREY
from evidently.legacy.options.option import Option


def test_options_creation():
    opt = ColorOptions(primary_color=GREY)

    obj = Options.from_any_options([opt])
    assert obj.color_options == opt

    obj = Options.from_any_options({"color": opt})
    assert obj.color_options == opt


class CustomOption(Option):
    field: int = 10


def test_custom_option():
    option = CustomOption(field=10)

    obj = Options.from_any_options([option])
    assert obj.get(CustomOption) == option

    obj = Options.from_any_options({"custom": {CustomOption: option}})
    assert obj.get(CustomOption) == option
