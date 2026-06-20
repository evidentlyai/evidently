import sys
import types

import numpy as np
import pandas as pd

from evidently.legacy.features.semantic_similarity_feature import SemanticSimilarityFeature
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import create_data_definition


def test_semantic_similarity_encodes_lists(monkeypatch):
    class FakeSentenceTransformer:
        instances = []

        def __init__(self, model):
            self.model = model
            self.calls = []
            self.instances.append(self)

        def encode(self, sentences):
            if not isinstance(sentences, list):
                raise ValueError(f"Unsupported input type: {type(sentences).__name__}")
            self.calls.append(sentences)
            return np.array([[float(index + 1), 1.0] for index, _ in enumerate(sentences)])

    sentence_transformers = types.ModuleType("sentence_transformers")
    sentence_transformers.SentenceTransformer = FakeSentenceTransformer
    monkeypatch.setitem(sys.modules, "sentence_transformers", sentence_transformers)

    feature_generator = SemanticSimilarityFeature(columns=["answer", "reference_answer"])
    data = pd.DataFrame(
        {
            "answer": ["same", None],
            "reference_answer": ["same", "different"],
        },
        index=[10, 11],
    )

    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )

    assert FakeSentenceTransformer.instances[0].calls == [["same", ""], ["same", "different"]]
    expected = pd.DataFrame({"answer|reference_answer": [1.0, 1.0]}, index=[10, 11])
    pd.testing.assert_frame_equal(result, expected)
