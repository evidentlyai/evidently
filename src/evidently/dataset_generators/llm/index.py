import abc
from abc import ABC
from dataclasses import dataclass
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


@dataclass
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

    def find_relevant_chunks(self, question: str, n_results=3) -> List[Chunk]:
        """
        Queries the collection with a given question and returns the relevant text chunks.

        Args:
            question (str): The query or question text to search for.
            n_results (int): Number of results to retrieve. Default is 3.

        Returns:
            List[Chunk]: A list of relevant text chunks.
        """
        # Perform the query
        results = self.collection.query(
            query_texts=question,
            n_results=n_results,
        )

        # Extract relevant text chunks from the documents
        relevant_chunks = [chunk for document in results["documents"] for chunk in document]

        return relevant_chunks


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
