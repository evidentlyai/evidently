import numpy as np
import pandas as pd

from evidently.core.datasets import DatasetColumn
from evidently.descriptors._context_relevance import semantic_similarity_scoring
from evidently.legacy.core import ColumnType
from evidently.legacy.options.base import Options


def test_context_relevance_semantic_similarity_scoring_series_conversion(mocker):
    mock_model = mocker.MagicMock()
    mock_model.encode.side_effect = lambda sentences: np.array([[0.1, 0.2] for _ in sentences])
    mocker.patch("sentence_transformers.SentenceTransformer", return_value=mock_model)

    question_col = DatasetColumn(
        data=pd.Series(["what is pandas?", "what is pytest?"], name="question"),
        type=ColumnType.Categorical,
    )
    context_col = DatasetColumn(
        data=pd.Series([["pandas is dataframe"], ["pytest is test runner"]], name="context"),
        type=ColumnType.List,
    )

    res = semantic_similarity_scoring(question_col, context_col, Options())
    assert res is not None
    assert isinstance(res.data, pd.Series)

    first_arg = mock_model.encode.call_args_list[0][0][0]
    second_arg = mock_model.encode.call_args_list[1][0][0]
    assert isinstance(first_arg, list)
    assert isinstance(second_arg, list)
