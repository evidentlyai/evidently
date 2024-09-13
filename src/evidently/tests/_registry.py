from evidently.pydantic_utils import register_type_alias
from evidently.tests.base_test import Test
from evidently.tests.base_test import TestParameters

register_type_alias(
    Test, "evidently.tests.classification_performance_tests.TestAccuracyScore", "evidently:test:TestAccuracyScore"
)
register_type_alias(
    Test, "evidently.tests.classification_performance_tests.TestF1ByClass", "evidently:test:TestF1ByClass"
)
register_type_alias(Test, "evidently.tests.classification_performance_tests.TestF1Score", "evidently:test:TestF1Score")
register_type_alias(Test, "evidently.tests.classification_performance_tests.TestFNR", "evidently:test:TestFNR")
register_type_alias(Test, "evidently.tests.classification_performance_tests.TestFPR", "evidently:test:TestFPR")
register_type_alias(Test, "evidently.tests.classification_performance_tests.TestLogLoss", "evidently:test:TestLogLoss")
register_type_alias(
    Test, "evidently.tests.classification_performance_tests.TestPrecisionByClass", "evidently:test:TestPrecisionByClass"
)
register_type_alias(
    Test, "evidently.tests.classification_performance_tests.TestPrecisionScore", "evidently:test:TestPrecisionScore"
)
register_type_alias(
    Test, "evidently.tests.classification_performance_tests.TestRecallByClass", "evidently:test:TestRecallByClass"
)
register_type_alias(
    Test, "evidently.tests.classification_performance_tests.TestRecallScore", "evidently:test:TestRecallScore"
)
register_type_alias(Test, "evidently.tests.classification_performance_tests.TestRocAuc", "evidently:test:TestRocAuc")
register_type_alias(Test, "evidently.tests.classification_performance_tests.TestTNR", "evidently:test:TestTNR")
register_type_alias(Test, "evidently.tests.classification_performance_tests.TestTPR", "evidently:test:TestTPR")
register_type_alias(Test, "evidently.tests.custom_test.CustomValueTest", "evidently:test:CustomValueTest")
register_type_alias(Test, "evidently.tests.data_drift_tests.TestColumnDrift", "evidently:test:TestColumnDrift")
register_type_alias(Test, "evidently.tests.data_drift_tests.TestEmbeddingsDrift", "evidently:test:TestEmbeddingsDrift")
register_type_alias(
    Test, "evidently.tests.data_drift_tests.TestNumberOfDriftedColumns", "evidently:test:TestNumberOfDriftedColumns"
)
register_type_alias(
    Test, "evidently.tests.data_drift_tests.TestShareOfDriftedColumns", "evidently:test:TestShareOfDriftedColumns"
)
register_type_alias(
    Test,
    "evidently.tests.data_integrity_tests.TestColumnAllConstantValues",
    "evidently:test:TestColumnAllConstantValues",
)
register_type_alias(
    Test, "evidently.tests.data_integrity_tests.TestColumnAllUniqueValues", "evidently:test:TestColumnAllUniqueValues"
)
register_type_alias(
    Test,
    "evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues",
    "evidently:test:TestColumnNumberOfDifferentMissingValues",
)
register_type_alias(
    Test,
    "evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues",
    "evidently:test:TestColumnNumberOfMissingValues",
)
register_type_alias(
    Test,
    "evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues",
    "evidently:test:TestColumnShareOfMissingValues",
)
register_type_alias(Test, "evidently.tests.data_integrity_tests.TestColumnsType", "evidently:test:TestColumnsType")
register_type_alias(
    Test, "evidently.tests.data_integrity_tests.TestNumberOfColumns", "evidently:test:TestNumberOfColumns"
)
register_type_alias(
    Test,
    "evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues",
    "evidently:test:TestNumberOfColumnsWithMissingValues",
)
register_type_alias(
    Test,
    "evidently.tests.data_integrity_tests.TestNumberOfConstantColumns",
    "evidently:test:TestNumberOfConstantColumns",
)
register_type_alias(
    Test,
    "evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues",
    "evidently:test:TestNumberOfDifferentMissingValues",
)
register_type_alias(
    Test,
    "evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns",
    "evidently:test:TestNumberOfDuplicatedColumns",
)
register_type_alias(
    Test, "evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows", "evidently:test:TestNumberOfDuplicatedRows"
)
register_type_alias(
    Test, "evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns", "evidently:test:TestNumberOfEmptyColumns"
)
register_type_alias(
    Test, "evidently.tests.data_integrity_tests.TestNumberOfEmptyRows", "evidently:test:TestNumberOfEmptyRows"
)
register_type_alias(
    Test, "evidently.tests.data_integrity_tests.TestNumberOfMissingValues", "evidently:test:TestNumberOfMissingValues"
)
register_type_alias(Test, "evidently.tests.data_integrity_tests.TestNumberOfRows", "evidently:test:TestNumberOfRows")
register_type_alias(
    Test,
    "evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues",
    "evidently:test:TestNumberOfRowsWithMissingValues",
)
register_type_alias(
    Test,
    "evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues",
    "evidently:test:TestShareOfColumnsWithMissingValues",
)
register_type_alias(
    Test, "evidently.tests.data_integrity_tests.TestShareOfMissingValues", "evidently:test:TestShareOfMissingValues"
)
register_type_alias(
    Test,
    "evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues",
    "evidently:test:TestShareOfRowsWithMissingValues",
)
register_type_alias(Test, "evidently.tests.data_quality_tests.TestCategoryCount", "evidently:test:TestCategoryCount")
register_type_alias(Test, "evidently.tests.data_quality_tests.TestCategoryShare", "evidently:test:TestCategoryShare")
register_type_alias(Test, "evidently.tests.data_quality_tests.TestColumnQuantile", "evidently:test:TestColumnQuantile")
register_type_alias(Test, "evidently.tests.data_quality_tests.TestColumnValueMax", "evidently:test:TestColumnValueMax")
register_type_alias(
    Test, "evidently.tests.data_quality_tests.TestColumnValueMean", "evidently:test:TestColumnValueMean"
)
register_type_alias(
    Test, "evidently.tests.data_quality_tests.TestColumnValueMedian", "evidently:test:TestColumnValueMedian"
)
register_type_alias(Test, "evidently.tests.data_quality_tests.TestColumnValueMin", "evidently:test:TestColumnValueMin")
register_type_alias(Test, "evidently.tests.data_quality_tests.TestColumnValueStd", "evidently:test:TestColumnValueStd")
register_type_alias(
    Test, "evidently.tests.data_quality_tests.TestConflictPrediction", "evidently:test:TestConflictPrediction"
)
register_type_alias(Test, "evidently.tests.data_quality_tests.TestConflictTarget", "evidently:test:TestConflictTarget")
register_type_alias(
    Test, "evidently.tests.data_quality_tests.TestCorrelationChanges", "evidently:test:TestCorrelationChanges"
)
register_type_alias(
    Test, "evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns", "evidently:test:TestHighlyCorrelatedColumns"
)
register_type_alias(Test, "evidently.tests.data_quality_tests.TestMeanInNSigmas", "evidently:test:TestMeanInNSigmas")
register_type_alias(
    Test, "evidently.tests.data_quality_tests.TestMostCommonValueShare", "evidently:test:TestMostCommonValueShare"
)
register_type_alias(
    Test, "evidently.tests.data_quality_tests.TestNumberOfOutListValues", "evidently:test:TestNumberOfOutListValues"
)
register_type_alias(
    Test, "evidently.tests.data_quality_tests.TestNumberOfOutRangeValues", "evidently:test:TestNumberOfOutRangeValues"
)
register_type_alias(
    Test, "evidently.tests.data_quality_tests.TestNumberOfUniqueValues", "evidently:test:TestNumberOfUniqueValues"
)
register_type_alias(
    Test,
    "evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations",
    "evidently:test:TestPredictionFeaturesCorrelations",
)
register_type_alias(
    Test, "evidently.tests.data_quality_tests.TestShareOfOutListValues", "evidently:test:TestShareOfOutListValues"
)
register_type_alias(
    Test, "evidently.tests.data_quality_tests.TestShareOfOutRangeValues", "evidently:test:TestShareOfOutRangeValues"
)
register_type_alias(
    Test,
    "evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations",
    "evidently:test:TestTargetFeaturesCorrelations",
)
register_type_alias(
    Test,
    "evidently.tests.data_quality_tests.TestTargetPredictionCorrelation",
    "evidently:test:TestTargetPredictionCorrelation",
)
register_type_alias(
    Test, "evidently.tests.data_quality_tests.TestUniqueValuesShare", "evidently:test:TestUniqueValuesShare"
)
register_type_alias(Test, "evidently.tests.data_quality_tests.TestValueList", "evidently:test:TestValueList")
register_type_alias(Test, "evidently.tests.data_quality_tests.TestValueRange", "evidently:test:TestValueRange")
register_type_alias(Test, "evidently.tests.recsys_tests.TestARP", "evidently:test:TestARP")
register_type_alias(Test, "evidently.tests.recsys_tests.TestCoverage", "evidently:test:TestCoverage")
register_type_alias(Test, "evidently.tests.recsys_tests.TestDiversity", "evidently:test:TestDiversity")
register_type_alias(Test, "evidently.tests.recsys_tests.TestFBetaTopK", "evidently:test:TestFBetaTopK")
register_type_alias(Test, "evidently.tests.recsys_tests.TestGiniIndex", "evidently:test:TestGiniIndex")
register_type_alias(Test, "evidently.tests.recsys_tests.TestHitRateK", "evidently:test:TestHitRateK")
register_type_alias(Test, "evidently.tests.recsys_tests.TestMAPK", "evidently:test:TestMAPK")
register_type_alias(Test, "evidently.tests.recsys_tests.TestMARK", "evidently:test:TestMARK")
register_type_alias(Test, "evidently.tests.recsys_tests.TestMRRK", "evidently:test:TestMRRK")
register_type_alias(Test, "evidently.tests.recsys_tests.TestNDCGK", "evidently:test:TestNDCGK")
register_type_alias(Test, "evidently.tests.recsys_tests.TestNovelty", "evidently:test:TestNovelty")
register_type_alias(Test, "evidently.tests.recsys_tests.TestPersonalization", "evidently:test:TestPersonalization")
register_type_alias(Test, "evidently.tests.recsys_tests.TestPrecisionTopK", "evidently:test:TestPrecisionTopK")
register_type_alias(Test, "evidently.tests.recsys_tests.TestRecallTopK", "evidently:test:TestRecallTopK")
register_type_alias(Test, "evidently.tests.recsys_tests.TestScoreEntropy", "evidently:test:TestScoreEntropy")
register_type_alias(Test, "evidently.tests.recsys_tests.TestSerendipity", "evidently:test:TestSerendipity")
register_type_alias(
    Test, "evidently.tests.regression_performance_tests.TestValueAbsMaxError", "evidently:test:TestValueAbsMaxError"
)
register_type_alias(Test, "evidently.tests.regression_performance_tests.TestValueMAE", "evidently:test:TestValueMAE")
register_type_alias(Test, "evidently.tests.regression_performance_tests.TestValueMAPE", "evidently:test:TestValueMAPE")
register_type_alias(
    Test, "evidently.tests.regression_performance_tests.TestValueMeanError", "evidently:test:TestValueMeanError"
)
register_type_alias(
    Test, "evidently.tests.regression_performance_tests.TestValueR2Score", "evidently:test:TestValueR2Score"
)
register_type_alias(Test, "evidently.tests.regression_performance_tests.TestValueRMSE", "evidently:test:TestValueRMSE")


register_type_alias(
    TestParameters, "evidently.tests.base_test.CheckValueParameters", "evidently:test_parameters:CheckValueParameters"
)
register_type_alias(
    TestParameters,
    "evidently.tests.base_test.ColumnCheckValueParameters",
    "evidently:test_parameters:ColumnCheckValueParameters",
)
register_type_alias(
    TestParameters,
    "evidently.tests.base_test.ConditionTestParameters",
    "evidently:test_parameters:ConditionTestParameters",
)
register_type_alias(
    TestParameters, "evidently.tests.base_test.TestParameters", "evidently:test_parameters:TestParameters"
)
register_type_alias(
    TestParameters,
    "evidently.tests.classification_performance_tests.ByClassParameters",
    "evidently:test_parameters:ByClassParameters",
)
register_type_alias(
    TestParameters,
    "evidently.tests.data_drift_tests.ColumnDriftParameter",
    "evidently:test_parameters:ColumnDriftParameter",
)
register_type_alias(
    TestParameters,
    "evidently.tests.data_drift_tests.ColumnsDriftParameters",
    "evidently:test_parameters:ColumnsDriftParameters",
)
register_type_alias(
    TestParameters,
    "evidently.tests.data_integrity_tests.ColumnTypeParameter",
    "evidently:test_parameters:ColumnTypeParameter",
)
register_type_alias(
    TestParameters,
    "evidently.tests.data_integrity_tests.ColumnTypesParameter",
    "evidently:test_parameters:ColumnTypesParameter",
)
register_type_alias(
    TestParameters,
    "evidently.tests.data_quality_tests.ColumnValueListParameters",
    "evidently:test_parameters:ColumnValueListParameters",
)
register_type_alias(
    TestParameters,
    "evidently.tests.data_quality_tests.MeanInNSigmasParameter",
    "evidently:test_parameters:MeanInNSigmasParameter",
)
register_type_alias(
    TestParameters,
    "evidently.tests.data_quality_tests.ShareOfOutRangeParameters",
    "evidently:test_parameters:ShareOfOutRangeParameters",
)
register_type_alias(
    TestParameters,
    "evidently.tests.data_quality_tests.ValueListParameters",
    "evidently:test_parameters:ValueListParameters",
)
