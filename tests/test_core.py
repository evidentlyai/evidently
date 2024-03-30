from evidently.core import BaseResult
from evidently.core import IncludeTags
from evidently.core import get_fields_tags


def test_get_fields_tags():
    class A(BaseResult):
        class Config:
            field_tags = {"f1": {IncludeTags.Render}}
            tags = {IncludeTags.Current}

        f1: str

    class B(A):
        class Config:
            field_tags = {"f1": {IncludeTags.Reference}}
            tags = {IncludeTags.Extra}

    assert get_fields_tags(A) == {"f1": {IncludeTags.Render, IncludeTags.Current}}
    assert get_fields_tags(B) == {"f1": {IncludeTags.Reference, IncludeTags.Extra}}
