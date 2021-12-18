import datetime

import pandas

from evidently.analyzers.utils import process_columns
from evidently.pipeline.column_mapping import ColumnMapping


def test_process_columns() -> None:
    dataset = pandas.DataFrame.from_dict([
        dict(datetime=datetime.datetime.now(),
             target=1,
             prediction=1,
             feature1=0,
             feature2=1,
             cat_feature1="o",
             cat_feature2="b")])

    columns = process_columns(dataset, ColumnMapping())
    assert columns.utility_columns.id_column is None
    # process_columns has a problem with columns order - it returns not sorted list
    # we have to before a fix use sorted for comparing with sorted expected data
    assert sorted(columns.num_feature_names) == ['feature1', 'feature2']
    assert sorted(columns.cat_feature_names) == ['cat_feature1', 'cat_feature2']
