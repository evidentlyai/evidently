import abc
import glob
import os
from pathlib import Path
from typing import List
from typing import Optional

import chromadb
from chromadb.types import Collection
from chromadb.utils import embedding_functions

from evidently.experimental.dataset_generators.llm.splitter import AnySplitter
from evidently.experimental.dataset_generators.llm.splitter import Splitter
from evidently.pydantic_utils import EvidentlyBaseModel

Chunk = str
DEFAULT_CHUNK_SIZE = 512
DEFAULT_CHUNK_OVERLAP = 20


def read_text(filename: str) -> str:
    file_path = Path(filename)
    if file_path.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as e:
            raise ImportError("Please install pypdf to extract context from .pdf files") from e
        reader = PdfReader(file_path)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text
    else:
        return Path(filename).read_text()


class DataCollectionProvider(EvidentlyBaseModel, abc.ABC):
    class Config:
        is_base_type = True

    chunk_size: int = DEFAULT_CHUNK_SIZE
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
    splitter: AnySplitter = "llama_index"

    @abc.abstractmethod
    def get_data_collection(self) -> "DataCollection":
        raise NotImplementedError

    @classmethod
    def from_files(
        cls,
        path: str,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
        splitter: AnySplitter = "llama_index",
    ) -> "DataCollectionProvider":
        return FileDataCollectionProvider(
            path=path, chunk_size=chunk_size, chunk_overlap=chunk_overlap, splitter=splitter
        )

    @classmethod
    def from_chunks(cls, chunks: List[str]):
        return ChunksDataCollectionProvider(chunks=chunks)


class ChunksDataCollectionProvider(DataCollectionProvider):
    class Config:
        type_alias = "evidently:data_collecton_provider:ChunksDataCollectionProvider"

    chunks: List[Chunk]

    def get_data_collection(self):
        dc = DataCollection(name="chunks", chunks=self.chunks)
        dc.init_collection()
        return dc


class FileDataCollectionProvider(DataCollectionProvider):
    class Config:
        type_alias = "evidently:data_collecton_provider:FileDataCollectionProvider"

    path: str

    def get_data_collection(self):
        file_path = Path(self.path)
        paths = [self.path] if file_path.is_file() else glob.glob(os.path.join(self.path, "*"))

        splitter = Splitter.from_any(self.splitter, self.chunk_size, self.chunk_overlap)
        chunks = list(splitter.split([read_text(p) for p in paths]))

        data_collection = DataCollection(name=file_path.name, chunks=chunks)
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
            # fixme: huggingface/tokenizers warns about clean_up_tokenization_spaces
            import warnings

            os.environ["TOKENIZERS_PARALLELISM"] = "false"
            warnings.filterwarnings("ignore", category=FutureWarning)

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
