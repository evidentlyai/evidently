import dataclasses
from typing import Any

from sklearn import datasets
from sklearn import ensemble


@dataclasses.dataclass
class TestDataset:
    name: str
    current: Any
    reference: Any


dataset_fixtures = []


def dataset(f):
    # fixture = pytest.fixture(scope="session")(f)
    dataset_fixtures.append(f())
    return f


@dataset
def bcancer():
    bcancer_data = datasets.load_breast_cancer(as_frame="auto")
    bcancer = bcancer_data.frame

    bcancer_ref = bcancer.sample(n=300, replace=False)
    bcancer_cur = bcancer.sample(n=200, replace=False)

    # bcancer_label_ref = bcancer_ref.copy(deep=True)
    # bcancer_label_cur = bcancer_cur.copy(deep=True)

    model = ensemble.RandomForestClassifier(random_state=1, n_estimators=10)
    model.fit(bcancer_ref[bcancer_data.feature_names.tolist()], bcancer_ref.target)

    bcancer_ref["prediction"] = model.predict_proba(bcancer_ref[bcancer_data.feature_names.tolist()])[:, 1]
    bcancer_cur["prediction"] = model.predict_proba(bcancer_cur[bcancer_data.feature_names.tolist()])[:, 1]

    # bcancer_label_ref['prediction'] = model.predict(bcancer_label_ref[bcancer_data.feature_names.tolist()])
    # bcancer_label_cur['prediction'] = model.predict(bcancer_label_cur[bcancer_data.feature_names.tolist()])
    return TestDataset("bcancer", bcancer_cur, bcancer_ref)
