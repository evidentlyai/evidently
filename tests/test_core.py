from typing import List
from typing import Union

from evidently.legacy.core import BaseResult
from evidently.legacy.core import IncludeTags
from evidently.legacy.core import get_all_fields_tags


class A(BaseResult):
    class Config:
        field_tags = {"f1": {IncludeTags.Render}}
        tags = {IncludeTags.Current}

    f1: str


def test_get_fields_tags():
    assert get_all_fields_tags(A) == {"f1": {IncludeTags.Render, IncludeTags.Current}}


def test_get_field_tags_subclass():
    class B(A):
        class Config:
            field_tags = {"f1": {IncludeTags.Reference}}
            tags = {IncludeTags.Extra}

    assert get_all_fields_tags(B) == {"f1": {IncludeTags.Reference, IncludeTags.Extra}}


def test_get_field_tags_field_add_tag():
    class C(BaseResult):
        class Config:
            field_tags = {"a2": {IncludeTags.Render}}

        a1: A
        a2: A

    assert get_all_fields_tags(C) == {"a1": {IncludeTags.Current}, "a2": {IncludeTags.Current, IncludeTags.Render}}


def test_get_field_tags_list_field():
    class D(BaseResult):
        class Config:
            field_tags = {"a2": {IncludeTags.Render}}

        a1: List[A]
        a2: List[A]

    assert get_all_fields_tags(D) == {"a1": {IncludeTags.Current}, "a2": {IncludeTags.Current, IncludeTags.Render}}


def test_get_field_tags_union_field():
    class C(BaseResult):
        pass

    class E(BaseResult):
        class Config:
            field_tags = {"ac2": {IncludeTags.Render}}

        ac1: Union[A, C]
        ac2: Union[A, C]

    assert get_all_fields_tags(E) == {"ac1": {IncludeTags.Current}, "ac2": {IncludeTags.Current, IncludeTags.Render}}


def test_get_field_tags_remove_tags():
    class F(A):
        class Config:
            field_tags = {"f1": set()}
            tags = set()

    assert get_all_fields_tags(F) == {"f1": set()}
