import dataclasses
from enum import Enum
from typing import Any
from typing import List
from typing import Optional

import numpy as np
from sklearn import datasets
from sklearn import ensemble

from evidently.pipeline.column_mapping import ColumnMapping


class DatasetTags(Enum):
    HAS_PREDICTION = "has_prediction"
    HAS_TARGET = "has_target"
    CLASSIFICATION = "classification"
    PROB_PREDICTIONS = "prob_predictions"
    BINARY_CLASSIFICATION = "binary_classification"
    MULTICLASS_CLASSIFICATION = "multiclass_classification"
    REGRESSION = "regression"


@dataclasses.dataclass(eq=True)
class TestDataset:
    name: str = ""
    current: Any = None
    reference: Any = None

    tags: List[DatasetTags] = dataclasses.field(default_factory=list)
    column_mapping: Optional[ColumnMapping] = None

    def __hash__(self):
        return id(self)


dataset_fixtures = []


def dataset(f):
    # fixture = pytest.fixture(scope="session")(f)
    dataset_fixtures.append(f())
    return f


@dataset
def bcancer():
    bcancer_data = datasets.load_breast_cancer(as_frame=True)
    bcancer = bcancer_data.frame

    bcancer_ref = bcancer.sample(n=300, replace=False)
    bcancer_cur = bcancer.sample(n=200, replace=False)

    model = ensemble.RandomForestClassifier(random_state=1, n_estimators=10)
    model.fit(bcancer_ref[bcancer_data.feature_names.tolist()], bcancer_ref.target)

    bcancer_ref["prediction"] = model.predict_proba(bcancer_ref[bcancer_data.feature_names.tolist()])[:, 1]
    bcancer_cur["prediction"] = model.predict_proba(bcancer_cur[bcancer_data.feature_names.tolist()])[:, 1]

    return TestDataset(
        "bcancer",
        bcancer_cur,
        bcancer_ref,
        [
            DatasetTags.CLASSIFICATION,
            DatasetTags.PROB_PREDICTIONS,
            DatasetTags.HAS_TARGET,
            DatasetTags.BINARY_CLASSIFICATION,
            DatasetTags.HAS_PREDICTION,
        ],
    )


@dataset
def bcancer_label():
    bcancer_data = datasets.load_breast_cancer(as_frame=True)
    bcancer = bcancer_data.frame

    bcancer_ref = bcancer.sample(n=300, replace=False)
    bcancer_cur = bcancer.sample(n=200, replace=False)

    bcancer_label_ref = bcancer_ref.copy(deep=True)
    bcancer_label_cur = bcancer_cur.copy(deep=True)

    model = ensemble.RandomForestClassifier(random_state=1, n_estimators=10)
    model.fit(bcancer_ref[bcancer_data.feature_names.tolist()], bcancer_ref.target)

    bcancer_label_ref["prediction"] = model.predict(bcancer_label_ref[bcancer_data.feature_names.tolist()])
    bcancer_label_cur["prediction"] = model.predict(bcancer_label_cur[bcancer_data.feature_names.tolist()])
    return TestDataset(
        "bcancer_label",
        bcancer_label_cur,
        bcancer_label_ref,
        [
            DatasetTags.CLASSIFICATION,
            DatasetTags.HAS_TARGET,
            DatasetTags.BINARY_CLASSIFICATION,
            DatasetTags.HAS_PREDICTION,
        ],
    )


@dataset
def adult():
    adult_data = datasets.fetch_openml(name="adult", version=2, as_frame=True)
    adult = adult_data.frame
    adult.education = adult.education.astype(object)

    adult_ref = adult[~adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]
    adult_cur = adult[adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]

    adult_cur.iloc[:2000, 3:5] = np.nan
    return TestDataset("adult", adult_cur, adult_ref, [])


@dataset
def housing():
    housing_data = datasets.fetch_california_housing(as_frame=True)
    housing = housing_data.frame

    housing.rename(columns={"MedHouseVal": "target"}, inplace=True)
    housing["prediction"] = housing_data["target"].values + np.random.normal(0, 3, housing.shape[0])

    housing_ref = housing.sample(n=5000, replace=False)
    housing_cur = housing.sample(n=5000, replace=False)
    return TestDataset(
        "housing",
        housing_cur,
        housing_ref,
        [DatasetTags.REGRESSION, DatasetTags.HAS_PREDICTION, DatasetTags.HAS_TARGET],
    )


@dataset
def reviews():
    reviews_data = datasets.fetch_openml(name="Womens-E-Commerce-Clothing-Reviews", version=2, as_frame=True)
    reviews = reviews_data.frame

    # In[ ]:

    reviews["prediction"] = reviews["Rating"]
    reviews_ref = reviews[reviews.Rating > 3].sample(
        n=5000, replace=True, ignore_index=True, random_state=42
    )  # .dropna()
    reviews_cur = reviews[reviews.Rating < 3].sample(
        n=5000, replace=True, ignore_index=True, random_state=42
    )  # .dropna()

    column_mapping = ColumnMapping(
        target="Rating",
        numerical_features=["Age", "Positive_Feedback_Count"],
        categorical_features=["Division_Name", "Department_Name", "Class_Name"],
        text_features=["Review_Text", "Title"],
    )

    return TestDataset(name="reviews", current=reviews_cur, reference=reviews_ref, column_mapping=column_mapping)
