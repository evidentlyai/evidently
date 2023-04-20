from evidently.options import ColorOptions
from evidently.options.base import Options
from evidently.options.color_scheme import GREY
from evidently.options.option import Option


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
