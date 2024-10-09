import abc
import dataclasses
from abc import ABC
from typing import Any
from typing import List
from typing import Optional

from llama_index.core.node_parser import SentenceSplitter

from evidently.pydantic_utils import EvidentlyBaseModel

Chunk = str


@dataclasses.dataclass
class DocumentIndex:
    chunks: List[Chunk]
    embeddings: Optional[Any] = None

    def get_embeddings(self):
        if self.embeddings is not None:
            self.embeddings = ...
        return self.embeddings


class IndexExtractor(EvidentlyBaseModel, ABC):
    @abc.abstractmethod
    def extract_index(self) -> DocumentIndex:
        raise NotImplementedError


class IndexExtractorFromFile(IndexExtractor):
    class Config:
        type_alias = "asdfasdfasd"

    path: str
    chunk_size: int = 512
    chunk_overlap: int = 20

    def extract_index(self) -> DocumentIndex:
        with open(self.path) as f:
            text = f.read()
        splitter = SentenceSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        text_nodes = splitter.split_text(text)
        return DocumentIndex(text_nodes)


class SimpleIndexExtractor(IndexExtractor):
    class Config:
        type_alias = "asdfasdasdfafasd"

    chunks: List[Chunk]

    def extract_index(self) -> DocumentIndex:
        return DocumentIndex(self.chunks)
