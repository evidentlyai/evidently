import numpy as np
import pytest
from collections import Counter
from src.evidently.llm.rag.rag_utils.sets import (
    compute_union_values,
    compute_intersection_values,
)


# ---------------------------------------------------------------------------
# compute_union_values
# ---------------------------------------------------------------------------

class TestComputeUnionValues:

    def test_identical_lists(self):
        ref = ["A", "B", "C"]
        ana = ["A", "B", "C"]

        result = compute_union_values(ref, ana)

        assert result == 3

    def test_empty_lists(self):
        result = compute_union_values([], [])

        assert result == 0

    def test_one_empty_list(self):
        ref = ["A", "B", "C"]

        assert compute_union_values(ref, []) == 3
        assert compute_union_values([], ref) == 3

    def test_completely_different_categories(self):
        ref = ["A", "B", "C"]
        ana = ["D", "E", "F"]

        result = compute_union_values(ref, ana)

        assert result == 6

    def test_single_category(self):
        ref = ["A"]
        ana = ["A"]

        result = compute_union_values(ref, ana)

        assert result == 1

    def test_same_category_with_different_counts(self):
        ref = ["A", "A", "A"]
        ana = ["A"]

        result = compute_union_values(ref, ana)

        assert result == 3

    def test_analysis_has_more_duplicates(self):
        ref = ["A"]
        ana = ["A", "A", "A", "A"]

        result = compute_union_values(ref, ana)

        assert result == 4

    def test_multiple_categories_with_duplicates(self):
        ref = ["A", "A", "B"]
        ana = ["A", "B", "B", "C"]

        result = compute_union_values(ref, ana)

        # A -> max(2, 1) = 2
        # B -> max(1, 2) = 2
        # C -> max(0, 1) = 1
        # Total = 5
        assert result == 5

    def test_duplicate_categories_are_not_counted_as_unique_values(self):
        ref = ["A", "A", "A", "B", "B"]
        ana = ["A", "B", "B", "B"]

        result = compute_union_values(ref, ana)

        # A -> max(3, 1) = 3
        # B -> max(2, 3) = 3
        assert result == 6

    def test_union_is_symmetric(self):
        ref = ["A", "A", "B", "C"]
        ana = ["A", "B", "B", "D"]

        result_ref_ana = compute_union_values(ref, ana)
        result_ana_ref = compute_union_values(ana, ref)

        assert result_ref_ana == result_ana_ref

    def test_subset_case(self):
        ref = ["A", "A", "B"]
        ana = ["A", "A"]

        result = compute_union_values(ref, ana)

        assert result == 3

    def test_categories_with_zero_overlap(self):
        ref = ["A", "A", "B", "B"]
        ana = ["C", "C", "D"]

        result = compute_union_values(ref, ana)

        assert result == 7

    def test_mixed_string_categories(self):
        ref = ["cat", "dog", "dog", "bird"]
        ana = ["dog", "dog", "bird", "fish"]

        result = compute_union_values(ref, ana)

        # cat = 1
        # dog = max(2, 2) = 2
        # bird = 1
        # fish = 1
        assert result == 5

    def test_integer_categories(self):
        ref = [1, 1, 2, 3]
        ana = [1, 2, 2, 4]

        result = compute_union_values(ref, ana)

        # 1 -> 2
        # 2 -> 2
        # 3 -> 1
        # 4 -> 1
        assert result == 6

    def test_tuple_categories(self):
        ref = [("A", 1), ("A", 1), ("B", 2)]
        ana = [("A", 1), ("B", 2), ("B", 2)]

        result = compute_union_values(ref, ana)

        # ("A", 1) -> 2
        # ("B", 2) -> 2
        assert result == 4


# ---------------------------------------------------------------------------
# compute_intersection_values
# ---------------------------------------------------------------------------

class TestComputeIntersectionValues:

    def test_identical_lists(self):
        ref = ["A", "B", "C"]
        ana = ["A", "B", "C"]

        result = compute_intersection_values(ref, ana)

        assert result == 3

    def test_empty_lists(self):
        result = compute_intersection_values([], [])

        assert result == 0

    def test_one_empty_list(self):
        ref = ["A", "B", "C"]

        assert compute_intersection_values(ref, []) == 0
        assert compute_intersection_values([], ref) == 0

    def test_completely_different_categories(self):
        ref = ["A", "B", "C"]
        ana = ["D", "E", "F"]

        result = compute_intersection_values(ref, ana)

        assert result == 0

    def test_single_category(self):
        ref = ["A"]
        ana = ["A"]

        result = compute_intersection_values(ref, ana)

        assert result == 1

    def test_same_category_with_different_counts(self):
        ref = ["A", "A", "A"]
        ana = ["A"]

        result = compute_intersection_values(ref, ana)

        assert result == 1

    def test_analysis_has_more_duplicates(self):
        ref = ["A"]
        ana = ["A", "A", "A", "A"]

        result = compute_intersection_values(ref, ana)

        assert result == 1

    def test_multiple_categories_with_duplicates(self):
        ref = ["A", "A", "B"]
        ana = ["A", "B", "B", "C"]

        result = compute_intersection_values(ref, ana)

        # A -> min(2, 1) = 1
        # B -> min(1, 2) = 1
        # C -> min(0, 1) = 0
        # Total = 2
        assert result == 2

    def test_duplicate_categories_are_counted_correctly(self):
        ref = ["A", "A", "A", "B", "B"]
        ana = ["A", "B", "B", "B"]

        result = compute_intersection_values(ref, ana)

        # A -> min(3, 1) = 1
        # B -> min(2, 3) = 2
        assert result == 3

    def test_intersection_is_symmetric(self):
        ref = ["A", "A", "B", "C"]
        ana = ["A", "B", "B", "D"]

        result_ref_ana = compute_intersection_values(ref, ana)
        result_ana_ref = compute_intersection_values(ana, ref)

        assert result_ref_ana == result_ana_ref

    def test_subset_case(self):
        ref = ["A", "A", "B"]
        ana = ["A", "A"]

        result = compute_intersection_values(ref, ana)

        assert result == 2

    def test_categories_with_zero_overlap(self):
        ref = ["A", "A", "B", "B"]
        ana = ["C", "C", "D"]

        result = compute_intersection_values(ref, ana)

        assert result == 0

    def test_mixed_string_categories(self):
        ref = ["cat", "dog", "dog", "bird"]
        ana = ["dog", "dog", "bird", "fish"]

        result = compute_intersection_values(ref, ana)

        # cat = 0
        # dog = 2
        # bird = 1
        # fish = 0
        assert result == 3

    def test_integer_categories(self):
        ref = [1, 1, 2, 3]
        ana = [1, 2, 2, 4]

        result = compute_intersection_values(ref, ana)

        # 1 -> min(2, 1) = 1
        # 2 -> min(1, 2) = 1
        # 3 -> 0
        # 4 -> 0
        assert result == 2

    def test_tuple_categories(self):
        ref = [("A", 1), ("A", 1), ("B", 2)]
        ana = [("A", 1), ("B", 2), ("B", 2)]

        result = compute_intersection_values(ref, ana)

        # ("A", 1) -> 1
        # ("B", 2) -> 1
        assert result == 2


# ---------------------------------------------------------------------------
# Mathematical properties of union/intersection
# ---------------------------------------------------------------------------

class TestCategoricalSetProperties:

    def test_union_is_at_least_intersection(self):
        ref = ["A", "A", "B", "C"]
        ana = ["A", "B", "B", "D"]

        union = compute_union_values(ref, ana)
        intersection = compute_intersection_values(ref, ana)

        assert union >= intersection

    def test_union_plus_intersection_equals_total_counts(self):
        ref = ["A", "A", "B", "C"]
        ana = ["A", "B", "B", "D"]

        union = compute_union_values(ref, ana)
        intersection = compute_intersection_values(ref, ana)

        # For multisets:
        # max(a,b) + min(a,b) = a + b
        assert union + intersection == len(ref) + len(ana)

    def test_union_plus_intersection_property_with_duplicates(self):
        ref = ["A", "A", "A", "B", "B", "C"]
        ana = ["A", "A", "B", "B", "B", "D"]

        union = compute_union_values(ref, ana)
        intersection = compute_intersection_values(ref, ana)

        assert union + intersection == len(ref) + len(ana)

    def test_identical_lists_union_equals_intersection(self):
        values = ["A", "A", "B", "C", "C"]

        union = compute_union_values(values, values)
        intersection = compute_intersection_values(values, values)

        assert union == intersection
        assert union == len(values)

    def test_union_is_bounded_by_total_observations(self):
        ref = ["A", "A", "B"]
        ana = ["A", "C", "C", "D"]

        union = compute_union_values(ref, ana)

        assert union <= len(ref) + len(ana)

    def test_intersection_is_bounded_by_smaller_dataset(self):
        ref = ["A", "A", "B", "C"]
        ana = ["A", "B"]

        intersection = compute_intersection_values(ref, ana)

        assert intersection <= min(len(ref), len(ana))

    def test_intersection_cannot_exceed_union(self):
        ref = ["A", "A", "B", "C"]
        ana = ["A", "B", "B", "D"]

        intersection = compute_intersection_values(ref, ana)
        union = compute_union_values(ref, ana)

        assert intersection <= union


# ---------------------------------------------------------------------------
# Randomized tests
# ---------------------------------------------------------------------------

class TestRandomizedCategoricalData:

    @pytest.mark.parametrize("seed", range(10))
    def test_union_intersection_identity(self, seed):
        rng = __import__("numpy").random.default_rng(seed)

        categories = np.array(["A", "B", "C", "D", "E"])

        n_ref = rng.integers(1, 30)
        n_ana = rng.integers(1, 30)

        ref = rng.choice(categories, size=n_ref).tolist()
        ana = rng.choice(categories, size=n_ana).tolist()

        union = compute_union_values(ref, ana)
        intersection = compute_intersection_values(ref, ana)

        assert union + intersection == len(ref) + len(ana)

    @pytest.mark.parametrize("seed", range(10))
    def test_random_union_is_greater_than_or_equal_to_intersection(
        self,
        seed,
    ):
        rng = __import__("numpy").random.default_rng(seed)

        categories = np.array(["A", "B", "C", "D"])

        ref = rng.choice(
            categories,
            size=rng.integers(1, 30),
        ).tolist()

        ana = rng.choice(
            categories,
            size=rng.integers(1, 30),
        ).tolist()

        union = compute_union_values(ref, ana)
        intersection = compute_intersection_values(ref, ana)

        assert union >= intersection

    @pytest.mark.parametrize("seed", range(10))
    def test_random_intersection_is_bounded(
        self,
        seed,
    ):
        rng = __import__("numpy").random.default_rng(seed)

        categories = np.array(["A", "B", "C", "D", "E"])

        ref = rng.choice(
            categories,
            size=rng.integers(1, 30),
        ).tolist()

        ana = rng.choice(
            categories,
            size=rng.integers(1, 30),
        ).tolist()

        intersection = compute_intersection_values(ref, ana)

        assert 0 <= intersection <= min(len(ref), len(ana))
