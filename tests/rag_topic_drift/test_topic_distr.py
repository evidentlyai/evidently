import pytest
from unittest.mock import MagicMock, patch
from src.evidently.llm.rag.topic_drift.topic_distr import get_topic_distr


@pytest.fixture
def mock_topic_model():
    return MagicMock()


@pytest.fixture
def mock_bertopic(mock_topic_model):
    with patch(
        f"{get_topic_distr.__module__}.BERTopic",
        return_value=mock_topic_model,
    ) as mock:
        yield mock


def test_get_topic_distr_returns_topic_distribution(
    mock_topic_model,
    mock_bertopic,
):
    mock_topic_model.fit_transform.return_value = (
        [0, 1, 0],
        [[0.9, 0.1], [0.2, 0.8], [0.7, 0.3]],
    )

    mock_topic_model.get_topic_info.return_value = MagicMock(
        Topic=[0, 1]
    )

    mock_topic_model.get_topic.side_effect = [
        [
            ("python", 0.8),
            ("programming", 0.6),
        ],
        [
            ("machine", 0.9),
            ("learning", 0.7),
        ],
    ]

    result = get_topic_distr(
        embedding_model="test-model",
        text=[
            "Python programming",
            "machine learning",
            "Python code",
        ],
    )

    assert result == {
        "Topic 0": {
            "python": 0.8,
            "programming": 0.6,
        },
        "Topic 1": {
            "machine": 0.9,
            "learning": 0.7,
        },
    }


def test_get_topic_distr_creates_topic_model_with_expected_parameters(
    mock_topic_model,
    mock_bertopic,
):
    mock_topic_model.fit_transform.return_value = ([], [])
    mock_topic_model.get_topic_info.return_value = MagicMock(
        Topic=[]
    )

    get_topic_distr(
        embedding_model="test-model",
        text=["some text"],
    )

    mock_bertopic.assert_called_once_with(
        embedding_model="test-model",
        min_topic_size=3,
        verbose=True,
    )


def test_get_topic_distr_calls_fit_transform_with_text(
    mock_topic_model,
    mock_bertopic,
):
    text = [
        "first document",
        "second document",
    ]

    mock_topic_model.fit_transform.return_value = (
        [0, 0],
        [[0.8], [0.9]],
    )

    mock_topic_model.get_topic_info.return_value = MagicMock(
        Topic=[0]
    )

    mock_topic_model.get_topic.return_value = [
        ("document", 0.75),
    ]

    get_topic_distr(
        embedding_model="test-model",
        text=text,
    )

    mock_topic_model.fit_transform.assert_called_once_with(text)


def test_get_topic_distr_ignores_outlier_topic(
    mock_topic_model,
    mock_bertopic,
):
    mock_topic_model.fit_transform.return_value = (
        [-1, 0, -1],
        [[0.5], [0.9], [0.5]],
    )

    mock_topic_model.get_topic_info.return_value = MagicMock(
        Topic=[-1, 0]
    )

    mock_topic_model.get_topic.return_value = [
        ("python", 0.8),
        ("code", 0.6),
    ]

    result = get_topic_distr(
        embedding_model="test-model",
        text=["text one", "text two", "text three"],
    )

    assert result == {
        "Topic 0": {
            "python": 0.8,
            "code": 0.6,
        }
    }

    mock_topic_model.get_topic.assert_called_once_with(0)


def test_get_topic_distr_converts_scores_to_float(
    mock_topic_model,
    mock_bertopic,
):
    mock_topic_model.fit_transform.return_value = (
        [0],
        [[1.0]],
    )

    mock_topic_model.get_topic_info.return_value = MagicMock(
        Topic=[0]
    )

    mock_topic_model.get_topic.return_value = [
        ("python", 1),
        ("code", 2),
    ]

    result = get_topic_distr(
        embedding_model="test-model",
        text=["Python code"],
    )

    assert result == {
        "Topic 0": {
            "python": 1.0,
            "code": 2.0,
        }
    }

    assert isinstance(result["Topic 0"]["python"], float)
    assert isinstance(result["Topic 0"]["code"], float)


def test_get_topic_distr_with_no_topics_returns_empty_dict(
    mock_topic_model,
    mock_bertopic,
):
    mock_topic_model.fit_transform.return_value = ([], [])
    mock_topic_model.get_topic_info.return_value = MagicMock(
        Topic=[]
    )

    result = get_topic_distr(
        embedding_model="test-model",
        text=[],
    )

    assert result == {}


def test_get_topic_distr_with_only_outlier_topic_returns_empty_dict(
    mock_topic_model,
    mock_bertopic,
):
    mock_topic_model.fit_transform.return_value = (
        [-1, -1, -1],
        [[1.0], [1.0], [1.0]],
    )

    mock_topic_model.get_topic_info.return_value = MagicMock(
        Topic=[-1]
    )

    result = get_topic_distr(
        embedding_model="test-model",
        text=["text one", "text two", "text three"],
    )

    assert result == {}

    mock_topic_model.get_topic.assert_not_called()


def test_get_topic_distr_gets_each_topic(
    mock_topic_model,
    mock_bertopic,
):
    mock_topic_model.fit_transform.return_value = (
        [2, 5],
        [[0.8], [0.9]],
    )

    mock_topic_model.get_topic_info.return_value = MagicMock(
        Topic=[-1, 2, 5]
    )

    mock_topic_model.get_topic.side_effect = [
        [("apple", 0.8)],
        [("banana", 0.9)],
    ]

    result = get_topic_distr(
        embedding_model="test-model",
        text=["apple text", "banana text"],
    )

    assert result == {
        "Topic 2": {
            "apple": 0.8,
        },
        "Topic 5": {
            "banana": 0.9,
        },
    }

    assert mock_topic_model.get_topic.call_count == 2
    mock_topic_model.get_topic.assert_any_call(2)
    mock_topic_model.get_topic.assert_any_call(5)
