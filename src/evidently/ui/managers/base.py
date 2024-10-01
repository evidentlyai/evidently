from collections import defaultdict
from functools import wraps
from typing import Callable
from typing import Dict
from typing import Generic
from typing import List
from typing import NamedTuple
from typing import TypeVar

TManager = TypeVar("TManager", bound="BaseManager")


def create_augmented_method(method_name: str, raw: Callable):
    @wraps(raw)
    def augmented(self: "BaseManager", *args, **kwargs):
        for before_aug in self.method_augs[method_name].before:
            before_aug(self, *args, **kwargs)
        result = raw(self, *args, **kwargs)
        for after_aug in self.method_augs[method_name].after:
            after_aug(self, result, *args, **kwargs)
        return result

    return augmented


class ManagerMeta(type):
    def __new__(mcs, name, bases, namespace):
        augmentable = {key: value for key, value in namespace.items() if callable(value) and not key.startswith("_")}
        augmented = {key: create_augmented_method(key, value) for key, value in augmentable.items()}
        namespace.update(augmented)
        cls = super().__new__(mcs, name, bases, namespace)
        cls.augmentable = augmentable
        return cls


class AugmenterMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls: AugmenterMeta = super().__new__(mcs, name, bases, namespace)
        cls.befores = defaultdict(list)
        cls.afters = defaultdict(list)
        for method in namespace.values():
            if not callable(method):
                continue
            if hasattr(method, "is_before"):
                is_before = method.is_before
                cls.befores[is_before].append(method)
            if hasattr(method, "is_after"):
                is_after = method.is_after
                cls.afters[is_after].append(method)
        return cls


class BaseManagerAugmenter(Generic[TManager], metaclass=AugmenterMeta):
    befores: Dict[str, List[Callable]]
    afters: Dict[str, List[Callable]]

    def get_before_augs_for_method(self, method_name: str) -> List[Callable]:
        return self.befores.get(method_name)

    def get_after_augs_for_method(self, method_name: str) -> List[Callable]:
        return self.afters.get(method_name)


class MethodAugs(NamedTuple):
    before: List[Callable]
    after: List[Callable]

    @classmethod
    def create(cls, method_name: str, augs: List[BaseManagerAugmenter]):
        before_augs = []
        after_augs = []
        for a in augs:
            before_augs.extend(a.get_before_augs_for_method(method_name))
        for a in augs:
            after_augs.extend(a.get_after_augs_for_method(method_name))
        return MethodAugs(before=before_augs, after=after_augs)


class BaseManager(metaclass=ManagerMeta):
    def __init__(self: TManager, augs: List[BaseManagerAugmenter[TManager]]):
        self.augs = augs
        self.method_augs: Dict[str, MethodAugs] = {
            method_name: MethodAugs.create(method_name, augs) for method_name in self.augmentable.keys()
        }


def before(for_method: Callable):
    def dec(aug_method):
        aug_method.is_before = for_method.__name__
        return aug_method

    return dec


def after(for_method: Callable):
    def dec(aug_method):
        aug_method.is_after = for_method.__name__
        return aug_method

    return dec


def main():
    class MyManager(BaseManager):
        def my_func(self, a: int):
            print(a)

    class MyAugmenter(BaseManagerAugmenter[MyManager]):
        @before(MyManager.my_func)
        def also_print_kek(self, instance):
            print("kek")

        @before(MyManager.my_func)
        def also_print_lol(self, instance):
            print("lol")

        @after(MyManager.my_func)
        def print_42_on_finish(self, instance, result):
            print("42")

    aug = MyAugmenter()
    man = MyManager([aug])

    man.my_func(123)


if __name__ == "__main__":
    main()
