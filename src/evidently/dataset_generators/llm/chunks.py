import abc
from abc import ABC
from typing import Iterator
from typing import List

from llama_index.core.node_parser import SentenceSplitter

from evidently.pydantic_utils import EvidentlyBaseModel

LLMChunk = str


class ChunkGenerator(EvidentlyBaseModel, ABC):
    @abc.abstractmethod
    def generate_chunks(self) -> Iterator[LLMChunk]:
        raise NotImplementedError


class FileContextGenerator(ChunkGenerator):
    class Config:
        type_alias = "asdfasdfasd"

    path: str

    def generate_chunks(self) -> Iterator[LLMChunk]:
        with open(self.path) as f:
            text = f.read()
        splitter = SentenceSplitter(chunk_size=512, chunk_overlap=20)
        text_nodes = splitter.split_text(text)
        yield from text_nodes


class SimpleChunkGenerator(ChunkGenerator):
    class Config:
        type_alias = "asdfasdasdfafasd"

    chunks: List[LLMChunk]

    def generate_chunks(self) -> Iterator[LLMChunk]:
        yield from self.chunks
