--
How run the Tests in Evidently.
--

**TL;DR**: You can start with ready-made Test presets. You can also create custom Test Suites from 50+ individual Tests. All Tests have in-built defaults but can be customized.

# Installation and prep

After installation, import the TestSuite component and the required tests and presets:

from evidently.test_suite import TestSuite
from evidently.tests import *
from evidently.test_preset import NoTargetPerformance, DataQuality, DataStability, DataDrift, Regression, MulticlassClassification, BinaryClassificationTopK, BinaryClassification

You need to prepare two datasets for comparison: reference and current. The reference dataset is optional. 

Refer to the input data and column mapping for more details on data preparation and requirements.
