# evidently.test_suite package

## Submodules

## <a name="module-evidently.test_suite.test_suite"></a>test_suite module


### class TestSuite(tests: Optional[List[Union[[Test](evidently.tests.md#evidently.tests.base_test.Test), [TestPreset](evidently.test_preset.md#evidently.test_preset.test_preset.TestPreset), [BaseGenerator](evidently.utils.md#evidently.utils.generators.BaseGenerator)]]], options: Optional[list] = None)
Bases: [`Display`](evidently.suite.md#evidently.suite.base_suite.Display)


#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; as_dict()

##### &nbsp;&nbsp;&nbsp;&nbsp; run(\*, reference_data: Optional[DataFrame], current_data: DataFrame, column_mapping: Optional[[ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping)] = None)
