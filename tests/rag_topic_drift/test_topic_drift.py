import pandas as pd
import pytest
from unittest.mock import MagicMock

from src.evidently.llm.rag.topic_drift import (
    TopicContentQueryDrift,
    TopicSemanticContentDrift,
)


# ---------------------------------------------------------------------------
# TopicContentQueryDrift
# ---------------------------------------------------------------------------

@pytest.fixture
def content_drift():
    return TopicContentQueryDrift(
        content_docs=[
            "content document 1",
            "content document 2",
        ],
        query_docs=[
            "query 1",
            "query 2",
        ],
        embedding_model="test-model",
    )


@pytest.fixture
def semantic_drift():
    return TopicSemanticContentDrift(
        ref_content_docs=[
            "reference document 1",
            "reference document 2",
        ],
        analysis_content_docs=[
            "analysis document 1",
            "analysis document 2",
        ],
        embedding_model="test-model",
    )


@pytest.fixture
def topic_distribution():
    return {
        "Topic 0": {
            "python": 0.9,
            "code": 0.7,
        },
        "Topic 1": {
            "machine": 0.8,
            "learning": 0.6,
        },
    }


# ============================================================================
# TopicContentQueryDrift
# ============================================================================


def test_query_topic_distribution(
    content_drift,
    topic_distribution,
    monkeypatch,
):
    get_topic_distr = MagicMock(
        return_value=topic_distribution
    )

    monkeypatch.setitem(
        TopicContentQueryDrift.query_topic_distribution.__globals__,
        "get_topic_distr",
        get_topic_distr,
    )

    result = content_drift.query_topic_distribution()

    assert result == topic_distribution

    get_topic_distr.assert_called_once_with(
        embedding_model="test-model",
        text=["query 1", "query 2"],
    )


def test_content_topic_distribution(
    content_drift,
    topic_distribution,
    monkeypatch,
):
    get_topic_distr = MagicMock(
        return_value=topic_distribution
    )

    monkeypatch.setitem(
        TopicContentQueryDrift.content_topic_distribution.__globals__,
        "get_topic_distr",
        get_topic_distr,
    )

    result = content_drift.content_topic_distribution()

    assert result == topic_distribution

    get_topic_distr.assert_called_once_with(
        embedding_model="test-model",
        text=[
            "content document 1",
            "content document 2",
        ],
    )


def test_topic_words_dict(
    content_drift,
    monkeypatch,
):
    content_distribution = {
        "Topic 0": {
            "python": 0.9,
            "code": 0.7,
        },
        "Topic 1": {
            "machine": 0.8,
            "learning": 0.6,
        },
    }

    query_distribution = {
        "Topic 0": {
            "python": 0.95,
        },
        "Topic 2": {
            "database": 0.8,
        },
    }

    monkeypatch.setattr(
        content_drift,
        "content_topic_distribution",
        MagicMock(
            return_value=content_distribution
        ),
    )

    monkeypatch.setattr(
        content_drift,
        "query_topic_distribution",
        MagicMock(
            return_value=query_distribution
        ),
    )

    # Current implementation builds the dictionaries
    # but does not return them.
    result = content_drift.topic_words_dict()

    assert result is None


def test_topic_words_dataframes(
    content_drift,
    monkeypatch,
):
    content_distribution = {
        "Topic 0": {
            "python": 0.9,
            "code": 0.7,
        },
        "Topic 1": {
            "machine": 0.8,
        },
    }

    query_distribution = {
        "Topic 0": {
            "python": 0.95,
        },
        "Topic 2": {
            "database": 0.8,
        },
    }

    monkeypatch.setattr(
        content_drift,
        "content_topic_distribution",
        MagicMock(
            return_value=content_distribution
        ),
    )

    monkeypatch.setattr(
        content_drift,
        "query_topic_distribution",
        MagicMock(
            return_value=query_distribution
        ),
    )

    content_df, query_df = (
        content_drift.topic_words_dataframes()
    )

    expected_content = pd.DataFrame(
        {
            "words": [
                "python",
                "machine",
            ]
        }
    )

    expected_query = pd.DataFrame(
        {
            "words": [
                "python",
                "database",
            ]
        }
    )

    pd.testing.assert_frame_equal(
        content_df,
        expected_content,
    )

    pd.testing.assert_frame_equal(
        query_df,
        expected_query,
    )


def test_detect_mismatching_topics(
    content_drift,
    monkeypatch,
):
    content_df = pd.DataFrame(
        {"words": ["python", "machine"]}
    )

    query_df = pd.DataFrame(
        {"words": ["python", "database"]}
    )

    topic_words_dataframes = MagicMock(
        return_value=(content_df, query_df)
    )

    detect_mismatches = MagicMock()

    monkeypatch.setattr(
        content_drift,
        "topic_words_dataframes",
        topic_words_dataframes,
    )

    monkeypatch.setitem(
        TopicContentQueryDrift.detect_mismatching_topics.__globals__,
        "detect_mismatches",
        detect_mismatches,
    )

    result = content_drift.detect_mismatching_topics()

    assert result is None

    topic_words_dataframes.assert_called_once_with()

    detect_mismatches.assert_called_once_with(
        ref_data=content_df,
        ana_data=query_df,
        feature="words",
    )


def test_topic_word_drift(
    content_drift,
    monkeypatch,
):
    content_df = pd.DataFrame(
        {"words": ["python", "machine"]}
    )

    query_df = pd.DataFrame(
        {"words": ["python", "database"]}
    )

    topic_words_dataframes = MagicMock(
        return_value=(content_df, query_df)
    )

    similarity_drift = MagicMock()

    monkeypatch.setattr(
        content_drift,
        "topic_words_dataframes",
        topic_words_dataframes,
    )

    monkeypatch.setitem(
        TopicContentQueryDrift.topic_word_drift.__globals__,
        "SimilarityCategoricalFeatureDrift",
        similarity_drift,
    )

    result = content_drift.topic_word_drift()

    assert result is similarity_drift.return_value

    topic_words_dataframes.assert_called_once_with()

    similarity_drift.assert_called_once_with(
        ref_data=content_df,
        analysis_data=query_df,
    )


@pytest.mark.parametrize(
    "method_name",
    [
        "dice_coeff",
        "braun_coeff",
        "jaccard_coeff",
        "overlap_coeff",
        "tanimoto_coeff",
    ],
)
def test_similarity_methods_delegate_to_topic_word_drift(
    content_drift,
    method_name,
    monkeypatch,
):
    expected_value = 0.75

    drift = MagicMock()

    getattr(
        drift,
        method_name,
    ).return_value = expected_value

    topic_word_drift = MagicMock(
        return_value=drift
    )

    monkeypatch.setattr(
        content_drift,
        "topic_word_drift",
        topic_word_drift,
    )

    method = getattr(
        content_drift,
        method_name,
    )

    result = method()

    assert result == expected_value

    topic_word_drift.assert_called_once_with()

    getattr(
        drift,
        method_name,
    ).assert_called_once_with()


# ============================================================================
# TopicSemanticContentDrift
# ============================================================================


def test_ref_topic_distribution(
    semantic_drift,
    topic_distribution,
    monkeypatch,
):
    get_topic_distr = MagicMock(
        return_value=topic_distribution
    )

    monkeypatch.setitem(
        TopicSemanticContentDrift.ref_topic_distribution.__globals__,
        "get_topic_distr",
        get_topic_distr,
    )

    # Current implementation references self.query_docs,
    # which does not exist on TopicSemanticContentDrift.
    with pytest.raises(AttributeError):
        semantic_drift.ref_topic_distribution()


def test_analysis_topic_distribution(
    semantic_drift,
    topic_distribution,
    monkeypatch,
):
    get_topic_distr = MagicMock(
        return_value=topic_distribution
    )

    monkeypatch.setitem(
        TopicSemanticContentDrift.analysis_topic_distribution.__globals__,
        "get_topic_distr",
        get_topic_distr,
    )

    # Current implementation references self.content_docs,
    # which does not exist on TopicSemanticContentDrift.
    with pytest.raises(AttributeError):
        semantic_drift.analysis_topic_distribution()


def test_semantic_topic_words_dict(
    semantic_drift,
    monkeypatch,
):
    ref_distribution = {
        "Topic 0": {
            "python": 0.9,
        },
    }

    analysis_distribution = {
        "Topic 0": {
            "python": 0.8,
        },
    }

    monkeypatch.setattr(
        semantic_drift,
        "ref_topic_distribution",
        MagicMock(
            return_value=ref_distribution
        ),
    )

    monkeypatch.setattr(
        semantic_drift,
        "analysis_topic_distribution",
        MagicMock(
            return_value=analysis_distribution
        ),
    )

    # Current implementation does not return
    # the dictionaries it creates.
    result = semantic_drift.topic_words_dict()

    assert result is None


def test_semantic_topic_words_dataframes(
    semantic_drift,
    monkeypatch,
):
    ref_distribution = {
        "Topic 0": {
            "python": 0.9,
            "code": 0.7,
        },
        "Topic 1": {
            "machine": 0.8,
        },
    }

    analysis_distribution = {
        "Topic 0": {
            "python": 0.95,
        },
        "Topic 2": {
            "database": 0.8,
        },
    }

    monkeypatch.setattr(
        semantic_drift,
        "ref_topic_distribution",
        MagicMock(
            return_value=ref_distribution
        ),
    )

    monkeypatch.setattr(
        semantic_drift,
        "analysis_topic_distribution",
        MagicMock(
            return_value=analysis_distribution
        ),
    )

    ref_df, analysis_df = (
        semantic_drift.topic_words_dataframes()
    )

    expected_ref = pd.DataFrame(
        {
            "words": [
                "python",
                "machine",
            ]
        }
    )

    expected_analysis = pd.DataFrame(
        {
            "words": [
                "python",
                "database",
            ]
        }
    )

    pd.testing.assert_frame_equal(
        ref_df,
        expected_ref,
    )

    pd.testing.assert_frame_equal(
        analysis_df,
        expected_analysis,
    )


def test_semantic_detect_mismatching_topics(
    semantic_drift,
    monkeypatch,
):
    ref_df = pd.DataFrame(
        {"words": ["python", "machine"]}
    )

    analysis_df = pd.DataFrame(
        {"words": ["python", "database"]}
    )

    topic_words_dataframes = MagicMock(
        return_value=(ref_df, analysis_df)
    )

    detect_mismatches = MagicMock()

    monkeypatch.setattr(
        semantic_drift,
        "topic_words_dataframes",
        topic_words_dataframes,
    )

    monkeypatch.setitem(
        TopicSemanticContentDrift.detect_mismatching_topics.__globals__,
        "detect_mismatches",
        detect_mismatches,
    )

    result = semantic_drift.detect_mismatching_topics()

    assert result is None

    topic_words_dataframes.assert_called_once_with()

    detect_mismatches.assert_called_once_with(
        ref_data=ref_df,
        ana_data=analysis_df,
        feature="words",
    )


def test_semantic_topic_word_drift(
    semantic_drift,
    monkeypatch,
):
    ref_df = pd.DataFrame(
        {"words": ["python", "machine"]}
    )

    analysis_df = pd.DataFrame(
        {"words": ["python", "database"]}
    )

    topic_words_dataframes = MagicMock(
        return_value=(ref_df, analysis_df)
    )

    similarity_drift = MagicMock()

    monkeypatch.setattr(
        semantic_drift,
        "topic_words_dataframes",
        topic_words_dataframes,
    )

    monkeypatch.setitem(
        TopicSemanticContentDrift.topic_word_drift.__globals__,
        "SimilarityCategoricalFeatureDrift",
        similarity_drift,
    )

    result = semantic_drift.topic_word_drift()

    assert result is similarity_drift.return_value

    topic_words_dataframes.assert_called_once_with()

    similarity_drift.assert_called_once_with(
        ref_data=ref_df,
        analysis_data=analysis_df,
    )


@pytest.mark.parametrize(
    "method_name",
    [
        "dice_coeff",
        "braun_coeff",
        "jaccard_coeff",
        "overlap_coeff",
        "tanimoto_coeff",
    ],
)
def test_semantic_similarity_methods_delegate_to_topic_word_drift(
    semantic_drift,
    method_name,
    monkeypatch,
):
    expected_value = 0.75

    drift = MagicMock()

    getattr(
        drift,
        method_name,
    ).return_value = expected_value

    topic_word_drift = MagicMock(
        return_value=drift
    )

    monkeypatch.setattr(
        semantic_drift,
        "topic_word_drift",
        topic_word_drift,
    )

    method = getattr(
        semantic_drift,
        method_name,
    )

    result = method()

    assert result == expected_value

    topic_word_drift.assert_called_once_with()

    getattr(
        drift,
        method_name,
    ).assert_called_once_with()
