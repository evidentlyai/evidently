from typing import List

from evidently.llm.rag.index import DataCollection
from evidently.llm.rag.index import DataCollectionProvider
from evidently.llm.rag.index import _get_embedding
from evidently.llm.rag.splitter import Chunk
from evidently.llm.rag.splitter import ChunkSet


class IrisConnection:
    """Connection configuration and management for Iris database."""

    def __init__(
        self,
        hostname: str,
        namespace: str,
        username: str,
        password: str,
        port: int = 1972,
    ):
        self.hostname = hostname
        self.port = port
        self.namespace = namespace
        self.username = username
        self.password = password
        self._connection = None

    def get_connection_string(self) -> str:
        """Generate connection string for Iris."""
        return f"{self.hostname}:{self.port}/{self.namespace}"

    def connect(self):
        """Establish connection to Iris database."""
        try:
            import iris
        except ImportError as e:
            raise ImportError("Run `pip install intersystems-irispython` to use Iris vector database") from e

        connection_string = self.get_connection_string()
        connection = iris.connect(connection_string, self.username, self.password)
        return connection

    def get_cursor(self):
        """Get database cursor, creating connection if needed."""
        if self._connection is None:
            self._connection = self.connect()
        return self._connection.cursor()

    def close(self):
        """Close database connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None


class IrisDataCollectionProvider(DataCollectionProvider):
    """Data collection provider for Iris vector database."""

    # Flat connection parameters
    hostname: str
    port: int = 1972
    namespace: str
    username: str
    password: str

    # Table configuration
    table_name: str
    text_column: str = "text"
    vector_column: str = "vector_data"
    id_column: str = "id"

    def _get_data_collection(self) -> "DataCollection":
        """Create and return IrisDataCollection instance."""
        # Create connection from flat parameters
        connection = IrisConnection(
            hostname=self.hostname,
            port=self.port,
            namespace=self.namespace,
            username=self.username,
            password=self.password,
        )

        return IrisDataCollection(
            connection=connection,
            table_name=self.table_name,
            text_column=self.text_column,
            vector_column=self.vector_column,
            id_column=self.id_column,
        )


class IrisDataCollection(DataCollection):
    """Data collection implementation for Iris vector database."""

    def __init__(
        self,
        connection: IrisConnection,
        table_name: str,
        text_column: str = "text",
        vector_column: str = "vector_data",
        id_column: str = "id",
    ):
        self.connection = connection
        self.table_name = table_name
        self.text_column = text_column
        self.vector_column = vector_column
        self.id_column = id_column

    def generate_chunksets(self, count: int, chunks_per_set: int) -> List[ChunkSet]:
        """Generate random chunksets for RAG dataset generation."""
        import random

        cursor = self.connection.get_cursor()

        # First, get all IDs from the table
        ids_sql = f"SELECT {self.id_column} FROM {self.table_name}"
        cursor.execute(ids_sql)
        id_results = cursor.fetchall()

        # Extract IDs
        all_ids = [result[0] for result in id_results]

        if not all_ids:
            return []

        # Sample list of lists of IDs
        chunkset_ids = [[random.choice(all_ids) for _ in range(chunks_per_set)] for _ in range(count)]

        # Flatten into set to get unique IDs
        unique_ids = {id_ for ids in chunkset_ids for id_ in ids}

        # Fetch all unique IDs in one query
        placeholders = ",".join(["?" for _ in unique_ids])
        fetch_sql = f"SELECT {self.id_column}, {self.text_column} FROM {self.table_name} WHERE {self.id_column} IN ({placeholders})"
        cursor.execute(fetch_sql, list(unique_ids))
        text_results = cursor.fetchall()

        # Create mapping id -> text
        id_to_text = {result[0]: result[1] for result in text_results}

        # Use mapping on original list of lists of IDs
        chunksets = [[id_to_text[chunk_id] for chunk_id in ids_list] for ids_list in chunkset_ids]

        return chunksets

    def get_count(self) -> int:
        """Get the total number of chunks in the IRIS table."""
        cursor = self.connection.get_cursor()

        # Count total rows in the table
        count_sql = f"SELECT COUNT(*) FROM {self.table_name}"
        cursor.execute(count_sql)
        result = cursor.fetchone()

        return result[0] if result else 0

    def find_relevant_chunks(self, question: str, n_results: int = 3) -> List[Chunk]:
        """
        Find relevant chunks using vector similarity search in Iris.

        Args:
            question (str): The query text to search for.
            n_results (int): Number of results to retrieve.

        Returns:
            List[Chunk]: List of relevant text chunks.
        """
        cursor = self.connection.get_cursor()

        # Generate embedding for the question
        query_embedding = _get_embedding(question)
        query_vector = query_embedding.tolist()

        # Perform vector similarity search using VECTOR_DOT_PRODUCT
        search_sql = f"""
        SELECT TOP {n_results} {self.id_column}, {self.text_column}
        FROM {self.table_name}
        ORDER BY VECTOR_DOT_PRODUCT({self.vector_column}, ?) DESC
        """

        cursor.execute(search_sql, [str(query_vector)])
        results = cursor.fetchall()

        # Convert results to Chunk objects (which are just strings)
        chunks = []
        for result in results:
            _, text = result
            chunks.append(text)

        return chunks

    def close(self):
        """Close database connection."""
        self.connection.close()
