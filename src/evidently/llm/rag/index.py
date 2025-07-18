import glob
import os
from abc import ABC
from abc import abstractmethod
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import List
from typing import Optional

import numpy as np

from evidently._pydantic_compat import PrivateAttr
from evidently.llm.rag.splitter import AnySplitter
from evidently.llm.rag.splitter import Chunk
from evidently.llm.rag.splitter import Splitter
from evidently.llm.rag.utils import read_text
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel

if TYPE_CHECKING:
    from faiss import IndexFlatL2


DEFAULT_CHUNK_SIZE = 512
DEFAULT_CHUNK_OVERLAP = 20


class DataCollectionProvider(AutoAliasMixin, EvidentlyBaseModel, ABC):
    __alias_type__: ClassVar = "data_collection_provider"

    class Config:
        is_base_type = True

    chunk_size: int = DEFAULT_CHUNK_SIZE
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
    splitter: AnySplitter = "llama_index"
    _data_collection_cache: "DataCollection" = PrivateAttr()

    def get_data_collection(self, use_cache: bool = True) -> "DataCollection":
        if use_cache and hasattr(self, "_data_collection_cache"):
            return self._data_collection_cache
        self._data_collection_cache = self._get_data_collection()
        return self._data_collection_cache

    @abstractmethod
    def _get_data_collection(self) -> "DataCollection":
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
    chunks: List[Chunk]

    def _get_data_collection(self):
        dc = DataCollection(name="chunks", chunks=self.chunks)
        dc.init_collection()
        return dc


class FileDataCollectionProvider(DataCollectionProvider):
    class Config:
        type_alias = "evidently:data_collection_provider:FileDataCollectionProvider"

    path: str
    recursive: bool = False
    pattern: str = "*"

    def _get_data_collection(self):
        file_path = Path(self.path)
        if file_path.is_file():
            paths = [self.path]
        elif not self.recursive:
            paths = [p for p in glob.glob(os.path.join(self.path, self.pattern)) if os.path.isfile(p)]
        else:
            paths = [
                p for p in glob.glob(os.path.join(self.path, "**", self.pattern), recursive=True) if os.path.isfile(p)
            ]

        splitter = Splitter.from_any(self.splitter, self.chunk_size, self.chunk_overlap)
        chunks = list(splitter.split([read_text(p) for p in paths]))

        data_collection = DataCollection(name=file_path.name, chunks=chunks)
        data_collection.init_collection()
        return data_collection


EMBEDDING_DIMENSION = 384


@lru_cache
def _get_embedding_model():
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as e:
        raise ImportError("Run `pip install evidently[llm]` to use datagen") from e
    _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model


def _get_embedding(text):
    embedding = _get_embedding_model().encode(text)
    return np.array(embedding).astype("float32")  # Convert to numpy float32 for FAISS compatibility


class DataCollection:
    name: str
    chunks: List[Chunk]
    index: Optional["IndexFlatL2"] = None

    def __init__(self, name: str, chunks: List[str], index: Optional["IndexFlatL2"] = None):
        self.name = name
        self.chunks = chunks
        self.index = index

    def init_collection(self):
        try:
            import faiss
        except ImportError as e:
            raise ImportError("Run `pip install evidently[llm]` to use datagen") from e
        if self.index is None:
            # fixme: huggingface/tokenizers warns about clean_up_tokenization_spaces

            # os.environ["TOKENIZERS_PARALLELISM"] = "false"
            # warnings.filterwarnings("ignore", category=FutureWarning)

            self.index = faiss.IndexFlatL2(EMBEDDING_DIMENSION)

            self.index.add(np.array([_get_embedding(text) for text in self.chunks]))

    def find_relevant_chunks(self, question: str, n_results: int = 3) -> List[Chunk]:
        """
        Queries the collection with a given question and returns the relevant text chunks.

        Args:
            question (str): The query or question text to search for.
            n_results (int): Number of results to retrieve. Default is 3.

        Returns:
            List[Chunk]: A list of relevant text chunks.
        """
        if self.index is None:
            raise ValueError("Collection is not initialized")
        query_emb = _get_embedding(question)

        n_results = min(n_results, len(self.chunks))
        _, indexes = self.index.search(np.array([query_emb]), n_results)
        relevant_chunks = [self.chunks[i] for i in indexes.reshape(-1)]
        return relevant_chunks
