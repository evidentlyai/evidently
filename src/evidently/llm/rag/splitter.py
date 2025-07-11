import re
from abc import ABC
from abc import abstractmethod
from enum import Enum
from typing import ClassVar
from typing import Iterator
from typing import List
from typing import Optional
from typing import Union

from evidently._pydantic_compat import PrivateAttr
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel


class TextSource:
    @classmethod
    def from_any(cls, text_source: "AnyTextSource"):
        if isinstance(text_source, TextSource):
            return text_source
        if isinstance(text_source, str):
            return StrSource(text_source)
        raise NotImplementedError(f"Cannot create TextSource from {text_source.__class__.__name__}")

    @abstractmethod
    def get_text(self) -> str:
        raise NotImplementedError


class StrSource(TextSource):
    def __init__(self, value: str):
        self.value = value

    def get_text(self) -> str:
        return self.value


AnyTextSource = Union[str, bytes, TextSource]

Chunk = str
ChunkSet = List[Chunk]
Split = str


class Splitters(str, Enum):
    Simple = "simple"
    LlamaIndex = "llama_index"


AnySplitter = Union[str, Splitters, "Splitter"]


class Splitter(AutoAliasMixin, EvidentlyBaseModel, ABC):
    __alias_type__: ClassVar[str] = "splitter"

    class Config:
        is_base_type = True

    chunk_size: int
    chunk_overlap: int

    def split(self, texts: Union[AnyTextSource, List[AnyTextSource]]) -> Iterator[Chunk]:
        if not isinstance(texts, list):
            texts = [texts]

        for text in texts:
            yield from self.split_text(TextSource.from_any(text))

    @abstractmethod
    def split_text(self, text: TextSource) -> Iterator[Chunk]:
        raise NotImplementedError

    @classmethod
    def from_any(cls, splitter: AnySplitter, chunk_size: int, chunk_overlap: int, **kwargs):
        if isinstance(splitter, Splitter):
            return splitter
        if isinstance(splitter, str):
            splitter = Splitters(splitter)
        if isinstance(splitter, Splitters):
            if splitter == Splitters.Simple:
                return SimpleSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            if splitter == Splitters.LlamaIndex:
                return LlamaIndexSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, **kwargs)
            raise ValueError(f"Unknown splitter {splitter}")
        raise NotImplementedError(f"Cannot create splitter from {splitter.__class__.__name__}")


class SimpleSplitter(Splitter):
    split_re: ClassVar = re.compile(r"([^,.;。？！]+[,.;。？！]?)")

    def split_text(self, text: TextSource) -> Iterator[Chunk]:
        current_splits: List[str] = []
        current_size = 0
        for split in self.split_re.split(text.get_text()):
            split_size = len(split)
            if len(current_splits) > 0 and current_size + split_size > self.chunk_size:
                yield "".join(current_splits)
                while current_size > self.chunk_overlap and len(current_splits) > 0:
                    last, *current_splits = current_splits
                    last_size = len(last)
                    current_size -= last_size
            current_size += split_size
            current_splits.append(split)
        if current_size > 0:
            yield "".join(current_splits)


class LlamaIndexSplitter(Splitter):
    separator: str = " "
    paragraph_separator: Optional[str] = None
    _splitter = PrivateAttr(None)

    @property
    def splitter(self):
        if self._splitter is None:
            from llama_index.core.node_parser import SentenceSplitter
            from llama_index.core.node_parser.text.sentence import DEFAULT_PARAGRAPH_SEP

            self._splitter = SentenceSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                separator=self.separator,
                paragraph_separator=self.paragraph_separator or DEFAULT_PARAGRAPH_SEP,
            )
        return self._splitter

    def split_text(self, text: TextSource) -> Iterator[Chunk]:
        yield from self.splitter.split_text(text.get_text())
