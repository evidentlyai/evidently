import abc
import dataclasses
from abc import ABC
from pathlib import Path
from typing import List
from typing import Optional

import chromadb
from chromadb import ClientAPI
from chromadb.types import Collection
from chromadb.utils import embedding_functions
from llama_index.core.node_parser import SentenceSplitter

from evidently.pydantic_utils import EvidentlyBaseModel

Chunk = str


@dataclasses.dataclass
class DocumentIndex:
    name: str
    chunks: List[Chunk]
    collection: Collection = None
    chroma_client: Optional[ClientAPI] = None

    def get_collection(self):
        if self.collection is None:
            default_embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2",
            )
            self.chroma_client = chromadb.Client()
            collection = self.chroma_client.get_or_create_collection(
                name=self.name,
                embedding_function=default_embedding_function,
            )
            # insert documents with embeddings to collection ChromaDB
            for i, chunk in enumerate(self.chunks):
                collection.upsert(
                    ids=str(i),
                    documents=chunk,
                )
            self.collection = collection
        return self.collection


class IndexExtractor(EvidentlyBaseModel, ABC):
    @abc.abstractmethod
    def extract_index(self) -> DocumentIndex:
        raise NotImplementedError


class IndexExtractorFromFile(IndexExtractor):
    class Config:
        type_alias = "IndexExtractorFromFile"

    path: Path
    chunk_size: int = 512
    chunk_overlap: int = 20

    def extract_index(self) -> DocumentIndex:
        with open(self.path) as f:
            text = f.read()
        splitter = SentenceSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        text_nodes = splitter.split_text(text)
        return DocumentIndex(self.path.name, chunks=text_nodes)


class SimpleIndexExtractor(IndexExtractor):
    class Config:
        type_alias = "asdfasdasdfafasd"

    chunks: List[Chunk]

    def extract_index(self) -> DocumentIndex:
        return DocumentIndex(self.chunks)
