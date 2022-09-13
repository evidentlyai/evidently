How to read the tables:

* Test: the name of an individual test that you can include in a Test Suite. If a test has an optional parameter, we'll include an example. 
* Level: we specify if the test can apply to the dataset or individual columns. Note that you can still apply column-level tests to all the columns in the dataset.
* Description: plain text explanation of how the test works.
* Default: plain text explanation of the default parameters. Many tests have two types of defaults. The first applies when you pass a reference dataset and Evidently can derive expectations from this baseline. The second applies if you do not provide the reference. You can always override the defaults by specifying a custom condition.   

We organize the tests into logical groups. Note that the groups do not match the presets with the same name, e.g., there are more Data Quality tests below than in the DataQuality preset.

!!! We are doing our best to maintain this page up to date. In case of discrepancies, consult the code (API reference coming soon!) or the current version of the "All tests and presets" example notebook in the [Examples](https://docs.evidentlyai.com/examples) section. If you notice an error, please send us a pull request to update the documentation!
