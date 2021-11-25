import datetime
import unittest

import pandas

from evidently.analyzers.utils import process_columns
from evidently.pipeline.column_mapping import ColumnMapping


class TestUtils(unittest.TestCase):
    def test_process_columns(self):
        dataset = pandas.DataFrame.from_dict([
            dict(datetime=datetime.datetime.now(),
                 target=1,
                 prediction=1,
                 feature1=0,
                 feature2=1,
                 cat_feature1="o",
                 cat_feature2="b")])

        columns = process_columns(dataset, ColumnMapping())
        self.assertIsNone(columns.utility_columns.id_column)
        self.assertCountEqual(['feature1', 'feature2'], columns.num_feature_names)
        self.assertCountEqual(['cat_feature1', 'cat_feature2'], columns.cat_feature_names)
