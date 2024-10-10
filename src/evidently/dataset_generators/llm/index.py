import os
from dataclasses import dataclass
from pathlib import Path
from typing import List
from typing import Optional

import chromadb
from chromadb.types import Collection
from chromadb.utils import embedding_functions
from llama_index.core.node_parser import SentenceSplitter

Chunk = str
DEFAULT_CHUNK_SIZE = 512
DEFAULT_CHUNK_OVERLAP = 20


@dataclass
class Document:
    id: str
    content: str


def load_md_from_dir(path: Path) -> List[Document]:
    """
    Loads Markdown (.md) files from the specified directory.

    Args:
        path (str): Path to the directory containing .md files.

    Returns:
        List[dict]: A list of dictionaries with the text content of each .md file.
    """
    documents = []

    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as file:
            documents.append(Document(id=file.name, content=file.read()))
        return documents

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            documents.append(Document(id=file.name, content=file.read()))

    return documents


class DataCollection:
    name: str
    chunks: List[Chunk]
    collection: Optional[Collection] = None

    def __init__(self, name: str, chunks: List[str], collection: Optional["Collection"] = None):
        self.name = name
        self.chunks = chunks
        self.collection = collection

    @classmethod
    def from_files(
        cls, path: str, chunk_size: int = DEFAULT_CHUNK_SIZE, chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
    ) -> "DataCollection":
        file_path = Path(path)
        # extractor = IndexExtractorFromFile(path=file_path, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        # documents = extractor.load_md_from_dir()
        documents = load_md_from_dir(path=file_path)
        splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        text_nodes = []

        for document in documents:
            text_nodes.extend(splitter.split_text(document.content))

        document_index = cls(name=file_path.name, chunks=text_nodes)
        document_index.get_collection()
        return document_index

    @classmethod
    def from_chunks(cls, chunks: List[str]):
        document_index = cls("kb_from_chunks", chunks=chunks)
        return document_index

    def get_collection(self):
        if self.collection is None:
            default_embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2",
            )
            chroma_client = chromadb.Client()
            collection = chroma_client.get_or_create_collection(
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

    def find_relevant_chunks(self, question: str, n_results: int = 3) -> List[Chunk]:
        """
        Queries the collection with a given question and returns the relevant text chunks.

        Args:
            question (str): The query or question text to search for.
            n_results (int): Number of results to retrieve. Default is 3.

        Returns:
            List[Chunk]: A list of relevant text chunks.
        """
        # Perform the query
        results = self.get_collection().query(
            query_texts=question,
            n_results=min(n_results, len(self.chunks)),
        )

        # Extract relevant text chunks from the documents
        relevant_chunks = [chunk for document in results["documents"] for chunk in document]
        return relevant_chunks


# class IndexExtractor(EvidentlyBaseModel, ABC):
#     @abc.abstractmethod
#     def extract_index(self) -> KnowledgeBase:
#         raise NotImplementedError


# class IndexExtractorFromFile(IndexExtractor):
#     class Config:
#         type_alias = "IndexExtractorFromFile"
#
#     path: Path
#     chunk_size: int = 512
#     chunk_overlap: int = 20
#
#     def load_md_from_dir(self) -> List[Document]:
#         """
#         Loads Markdown (.md) files from the specified directory.
#
#         Args:
#             path (str): Path to the directory containing .md files.
#
#         Returns:
#             List[dict]: A list of dictionaries with the text content of each .md file.
#         """
#         documents = []
#
#         if os.path.isfile(self.path):
#             with open(self.path, "r", encoding="utf-8") as file:
#                 documents.append(Document(id=file.name, content=file.read()))
#             return documents
#
#         for filename in os.listdir(self.path):
#             file_path = os.path.join(self.path, filename)
#             with open(file_path, "r", encoding="utf-8") as file:
#                 documents.append(Document(id=file.name, content=file.read()))
#
#         return documents
#
#     def extract_index(self) -> KnowledgeBase:
#         documents = self.load_md_from_dir()
#         splitter = SentenceSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
#         text_nodes = []
#         for document in documents:
#             text_nodes.extend(splitter.split_text(document.content))
#
#         return KnowledgeBase(self.path.name, chunks=text_nodes)

#         return DocumentIndex(self.path.name, chunks=text_nodes)
#
#
# class SimpleIndexExtractor(IndexExtractor):
#     class Config:
#         type_alias = "asdfasdasdfafasd"
#
#     chunks: List[Chunk]
#
#     def extract_index(self) -> DocumentIndex:
#         return DocumentIndex("inmemory", chunks=self.chunks)
