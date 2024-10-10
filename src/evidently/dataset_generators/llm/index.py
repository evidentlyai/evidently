import glob
import os
import warnings
from pathlib import Path
from typing import List
from typing import Optional

import chromadb
from chromadb.types import Collection
from chromadb.utils import embedding_functions
from llama_index.core.node_parser import SentenceSplitter
from pypdf import PdfReader

from evidently.pydantic_utils import EvidentlyBaseModel

Chunk = str
DEFAULT_CHUNK_SIZE = 512
DEFAULT_CHUNK_OVERLAP = 20

os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", category=FutureWarning)


def read_text(filename: str) -> str:
    file_path = Path(filename)
    if file_path.suffix.lower() == ".pdf":
        reader = PdfReader(file_path)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text
    else:
        return Path(filename).read_text()


class DataCollectionProvider(EvidentlyBaseModel):
    class Config:
        alias_required = False  # fixme

    chunk_size: int = DEFAULT_CHUNK_SIZE
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP

    def get_data_collection(self) -> "DataCollection":
        raise NotImplementedError

    @classmethod
    def from_files(
        cls, path: str, chunk_size: int = DEFAULT_CHUNK_SIZE, chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
    ) -> "DataCollectionProvider":
        return FileDataCollectionProvider(path=path, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    @classmethod
    def from_chunks(cls, chunks: List[str]):
        return ChunksDataCollectionProvider(chunks=chunks)


class ChunksDataCollectionProvider(DataCollectionProvider):
    chunks: List[Chunk]

    def get_data_collection(self):
        dc = DataCollection(name="chunks", chunks=self.chunks)
        dc.init_collection()
        return dc


class FileDataCollectionProvider(DataCollectionProvider):
    path: str

    def get_data_collection(self):
        splitter = SentenceSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        text_nodes = []
        file_path = Path(self.path)
        paths = [self.path] if file_path.is_file() else glob.glob(os.path.join(self.path, "*"))

        for filename in paths:
            nodes = splitter.split_text(read_text(filename))
            text_nodes.extend(nodes)

        data_collection = DataCollection(name=file_path.name, chunks=text_nodes)
        data_collection.init_collection()
        return data_collection


class DataCollection:
    name: str
    chunks: List[Chunk]
    collection: Optional[Collection] = None

    def __init__(self, name: str, chunks: List[str], collection: Optional["Collection"] = None):
        self.name = name
        self.chunks = chunks
        self.collection = collection

    def init_collection(self):
        if self.collection is None:
            default_embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2",
            )
            chroma_client = chromadb.Client()
            collection = chroma_client.get_or_create_collection(
                name=self.name,
                embedding_function=default_embedding_function,
            )
            for i, chunk in enumerate(self.chunks):
                collection.upsert(
                    ids=str(i),
                    documents=chunk,
                )
            self.collection = collection

    def find_relevant_chunks(self, question: str, n_results: int = 3) -> List[Chunk]:
        """
        Queries the collection with a given question and returns the relevant text chunks.

        Args:
            question (str): The query or question text to search for.
            n_results (int): Number of results to retrieve. Default is 3.

        Returns:
            List[Chunk]: A list of relevant text chunks.
        """
        if self.collection is None:
            raise ValueError("Collection is not initialized")
        results = self.collection.query(
            query_texts=question,
            n_results=min(n_results, len(self.chunks)),
        )

        relevant_chunks = [chunk for document in results["documents"] for chunk in document]
        return relevant_chunks
