import pandas as pd

from evidently import DataDefinition
from evidently import Dataset
from evidently import Report
from evidently.core.metric_types import SingleValue
from evidently.metrics import EmbeddingsDrift


def test_embeddings_drift():
    current_data = pd.DataFrame(data={"a": list(range(1, 30)) + [31], "b": list(range(41, 70)) + [71]})
    reference_data = pd.DataFrame(data={"a": list(range(1, 30)) + [31], "b": list(range(41, 70)) + [71]})
    definition = DataDefinition(embeddings={"emb1": ["a", "b"]})
    current_dataset = Dataset.from_pandas(current_data, definition)
    reference_dataset = Dataset.from_pandas(reference_data, definition)
    metric = EmbeddingsDrift(embeddings_name="emb1")
    report = Report(metrics=[metric])
    snapshot = report.run(current_dataset, reference_dataset)
    assert len(snapshot.metric_results) > 0
    result = list(snapshot.metric_results.values())[0]
    assert isinstance(result, SingleValue)
    assert result.value == 0.5
