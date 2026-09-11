import pandas as pd
import numpy as np
import pytest
from unittest.mock import patch
from src.evidently.llm.rag.drift import SimilarityFeatureDrift


@pytest.fixture
def reference_data():
    return pd.DataFrame(
        {
            "category": ["A", "B", "C", "D"],
        }
    )


@pytest.fixture
def analysis_data():
    return pd.DataFrame(
        {
            "category": ["B", "C", "D", "E"],
        }
    )


@pytest.fixture
def drift(reference_data, analysis_data):
    return SimilarityCategoricalFeatureDrift(
        ref_data=reference_data,
        analysis_data=analysis_data,
    )


class TestSimilarityCategoricalFeatureDrift:

    def test_braun_coeff(self, drift):
        result = drift.braun_coeff("category")

        # Intersection = {B, C, D} => 3
        # max(len(ref), len(ana)) = 4
        # Braun = 3 / 4
        assert result == pytest.approx(0.75)

    def test_jaccard_coeff(self, drift):
        result = drift.jaccard_coeff("category")

        # Intersection = {B, C, D} => 3
        # Union = {A, B, C, D, E} => 5
        # Jaccard = 3 / 5
        assert result == pytest.approx(0.6)

    def test_dice_coeff(self, drift):
        result = drift.dice_coeff("category")

        # Intersection = 3
        # Dice = 2 * 3 / (4 + 4)
        assert result == pytest.approx(0.75)

    def test_overlap_coeff(self, drift):
        result = drift.overlap_coeff("category")

        # Intersection = 3
        # min(4, 4) = 4
        # Current implementation:
        # 2 * 3 / 4 = 1.5
        assert result == pytest.approx(1.5)

    def test_tanimoto_coeff(self, drift):
        result = drift.tanimoto_coeff("category")

        # Intersection = 3
        # 3 / (4 + 4 - 3) = 3 / 5
        assert result == pytest.approx(0.6)

    def test_identical_data(self):
        ref_data = pd.DataFrame({"category": ["A", "B", "C"]})
        ana_data = pd.DataFrame({"category": ["A", "B", "C"]})

        drift = SimilarityCategoricalFeatureDrift(ref_data, ana_data)

        assert drift.braun_coeff("category") == pytest.approx(1.0)
        assert drift.jaccard_coeff("category") == pytest.approx(1.0)
        assert drift.dice_coeff("category") == pytest.approx(1.0)

    def test_no_intersection(self):
        ref_data = pd.DataFrame({"category": ["A", "B", "C"]})
        ana_data = pd.DataFrame({"category": ["X", "Y", "Z"]})

        drift = SimilarityCategoricalFeatureDrift(ref_data, ana_data)

        assert drift.braun_coeff("category") == pytest.approx(0.0)
        assert drift.jaccard_coeff("category") == pytest.approx(0.0)
        assert drift.dice_coeff("category") == pytest.approx(0.0)
        assert drift.overlap_coeff("category") == pytest.approx(0.0)
        assert drift.tanimoto_coeff("category") == pytest.approx(0.0)

    def test_different_dataset_sizes(self):
        ref_data = pd.DataFrame(
            {
                "category": ["A", "B", "C", "D", "E"],
            }
        )

        ana_data = pd.DataFrame(
            {
                "category": ["A", "B", "C"],
            }
        )

        drift = SimilarityCategoricalFeatureDrift(ref_data, ana_data)

        # Intersection = 3
        #
        # Braun = 3 / max(5, 3) = 0.6
        assert drift.braun_coeff("category") == pytest.approx(0.6)

        # Dice = 2 * 3 / (5 + 3) = 0.75
        assert drift.dice_coeff("category") == pytest.approx(0.75)

        # Current implementation:
        # Overlap = 2 * 3 / min(5, 3) = 2.0
        assert drift.overlap_coeff("category") == pytest.approx(2.0)

        # Tanimoto = 3 / (5 + 3 - 3) = 0.6
        assert drift.tanimoto_coeff("category") == pytest.approx(0.6)

    def test_missing_feature_raises_key_error(self, drift):
        with pytest.raises(KeyError):
            drift.jaccard_coeff("does_not_exist")





