import pathlib

import numpy as np
import numpy.testing
import pandas as pd
import pytest
from sklearn import datasets
from sklearn import ensemble

from evidently.legacy.test_preset import BinaryClassificationTestPreset
from evidently.legacy.test_preset import BinaryClassificationTopKTestPreset
from evidently.legacy.test_preset import DataDriftTestPreset
from evidently.legacy.test_preset import DataQualityTestPreset
from evidently.legacy.test_preset import DataStabilityTestPreset
from evidently.legacy.test_preset import MulticlassClassificationTestPreset
from evidently.legacy.test_preset import NoTargetPerformanceTestPreset
from evidently.legacy.test_preset import RegressionTestPreset
from evidently.legacy.test_suite import TestSuite
from tests.conftest import slow


@pytest.fixture
def adult():
    adult = pd.read_parquet(
        pathlib.Path(__file__).parent.joinpath("../../test_data/adults.parquet"),
    )

    adult_ref = adult[~adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]
    adult_cur = adult[adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]

    adult_cur.iloc[:2000, 3:5] = np.nan
    return adult_cur, adult_ref


@pytest.fixture
def housing():
    housing_data = datasets.fetch_california_housing(as_frame=True)
    housing = housing_data.frame

    housing.rename(columns={"MedHouseVal": "target"}, inplace=True)
    housing["prediction"] = housing_data["target"].values + np.random.normal(0, 3, housing.shape[0])

    housing_ref = housing.sample(n=5000, replace=False)
    housing_cur = housing.sample(n=5000, replace=False)
    return housing_cur, housing_ref


@pytest.fixture
def iris():
    iris_data = datasets.load_iris(as_frame=True)
    iris = iris_data.frame

    iris_ref = iris.sample(n=75, replace=False)
    iris_cur = iris.sample(n=75, replace=False)

    model = ensemble.RandomForestClassifier(random_state=1, n_estimators=3)
    model.fit(iris_ref[iris_data.feature_names], iris_ref.target)

    iris_ref["prediction"] = model.predict(iris_ref[iris_data.feature_names])
    iris_cur["prediction"] = model.predict(iris_cur[iris_data.feature_names])
    return iris_cur, iris_ref


@pytest.fixture
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

    return bcancer_label_cur, bcancer_label_ref


@pytest.fixture
def bcancer():
    bcancer_data = datasets.load_breast_cancer(as_frame=True)
    bcancer = bcancer_data.frame

    bcancer_ref = bcancer.sample(n=300, replace=False)
    bcancer_cur = bcancer.sample(n=200, replace=False)

    model = ensemble.RandomForestClassifier(random_state=1, n_estimators=10)
    model.fit(bcancer_ref[bcancer_data.feature_names.tolist()], bcancer_ref.target)

    bcancer_ref["prediction"] = model.predict_proba(bcancer_ref[bcancer_data.feature_names.tolist()])[:, 1]
    bcancer_cur["prediction"] = model.predict_proba(bcancer_cur[bcancer_data.feature_names.tolist()])[:, 1]

    return bcancer_cur, bcancer_ref


@slow
@pytest.mark.parametrize(
    "preset,data",
    [
        (DataStabilityTestPreset(), "adult"),
        (DataQualityTestPreset(), "adult"),
        (DataDriftTestPreset(stattest="psi"), "adult"),
        (
            NoTargetPerformanceTestPreset(
                columns=["education-num", "hours-per-week"], num_stattest="ks", cat_stattest="psi"
            ),
            "adult",
        ),
        (RegressionTestPreset(), "housing"),
        (MulticlassClassificationTestPreset(stattest="psi"), "iris"),
        (BinaryClassificationTestPreset(), "bcancer_label"),
        (BinaryClassificationTestPreset(stattest="psi", probas_threshold=0.89), "bcancer"),
        (BinaryClassificationTopKTestPreset(k=1, stattest="psi"), "bcancer"),
    ],
)
def test_suite(request, preset, data, tmp_path):
    cur, ref = request.getfixturevalue(data)
    suite = TestSuite(tests=[preset])

    suite.run(reference_data=ref, current_data=cur)
    suite._inner_suite.raise_for_error()
    suite.json()
    suite.as_dict()
    path = str(tmp_path / "suite.json")
    suite.save(path)
    suite2 = TestSuite.load(path)
    numpy.testing.assert_equal(suite2.as_dict(), suite.as_dict())
    suite2.show()
    suite2.save_html(str(tmp_path / "suite.html"))
