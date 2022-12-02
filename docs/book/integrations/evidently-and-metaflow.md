---
description: Run model evaluation or data drift analysis as Metaflow Flow and save the Evidently metrics in S3, visualizing it with the optional Metaflow UI.
---

*This is a community-contributed integration. Author: Marcello Victorino (https://github.com/marcellovictorino).*

Metaflow is an open-source [framework to helps scientists and engineers build and manage real-life data science projects](https://github.com/Netflix/metaflow).

You can use this integration to generate Evidently HTML reports, executed via a Metaflow Flow and visualize it as a [Card](https://docs.metaflow.org/api/cards) - using the [metaflow-card-html](https://pypi.org/project/metaflow-card-html/) plugin.

# **Overview**

Many machine learning teams use [Metaflow](https://outerbounds.com/) to orchestrate the multiple stages of ML lifecycle, such as data preparation, training, deployment, serving predictions, and as a model registry. 

If you are already familiar with Metaflow, here is an example on how to integrate it with Evidently to **track the quality of data** and the **data drift**.

In this case, Metaflow will orchestrate the execution of the Flow, using **Evidently to calculate the metrics/tests and generate the visual report** and **Metaflow to log the HTML results as an artefact**. You can then access the metrics in the Metaflow UI interface - or [retrieve it via the cards api](https://docs.metaflow.org/api/cards#retrieving-cards).

# **How it works**

With Metaflow, you can organize your Batch process into multiple Flows, such as:

1. **TrainingFlow**: retrieve data, split into train/test, train multiple models in parallel, identify the best and store it as an artifact
2. **ServingFlow**: from the latest successful TrainingFlow, retrieves the best model and use it to make predictions on the new data
3. **MonitoringFlow**: triggered by the `ServingFlow`, retrieves the data used in each last successful Flow and calculates the desired metrics, such as data quality and data drift, where `reference` is the data used in the `TrainingFlow` and `current` comes from the `ServingFlow`

**Note**: Evidently calculates a rich set of metrics and statistical tests. You can choose any of the pre-built [reports and test suites](../reports/) to define the metrics you’d want to get.

Within every Flow, it is possible to store artifacts that can be visualised with the `card` feature. This way, you can save the HTML content of the Evidently reports to be visualized with the `metaflow-card-html` plugin.

# Tutorial: Evaluating Data Drift with **Metaflow and Evidently**

In this example, we will use Evidently to check input features for [Data Drift](../reports/data-drift.md) and log and visualize the resulting report with Metaflow.

## **Step 1. Install Metaflow and Evidently**

Evidently is available as a PyPI package:

```
$ pip install evidently
```

For more details, refer to the Evidently [installation guide](../get-started/install-evidently.md).

To install Metaflow, run:

```
$ pip install metaflow
```

For more details, refer to the Metaflow [documentation](https://docs.metaflow.org/getting-started/install).

Install the `metaflow-card-html` plugin:
```
$ pip install metaflow-card-html
```

And any other dependencies, such as scikit-learn.

## Step 2. Define the helper function to obtain rendered HTML

We will use the following helper function to simplify obtaining the final fully rendered HTML content for the Evidently reports.

```python
def get_evidently_html(evidently_object) -> str:
    """Returns the rendered EvidentlyAI report/metric as HTML

    Should be assigned to `self.html`, installing `metaflow-card-html` to be rendered
    """
    import tempfile

    with tempfile.NamedTemporaryFile() as tmp:
        evidently_object.save_html(tmp.name)
        with open(tmp.name) as fh:
            return fh.read()
```

## Step 3. Define the Metaflow Flow
The `start` step is based on the Evidently getting started tutorial, preparing the data to be used in the following steps.

The `monitoring_data_quality` behaves as a **step**, due to the `@mf.step` decorator. The `@mf.card(type='html')` decorator adds behavior, ensuring the attribute `self.html` will be stored and properly rendered as HTML in the Card.

```python
import metaflow as mf


class GettingStartedEvidentlyFlow(mf.FlowSpec):
    @mf.step
    def start(self):
        import numpy as np
        from sklearn.datasets import fetch_california_housing

        data = fetch_california_housing(as_frame=True)
        housing_data = data.frame
        housing_data.rename(columns={"MedHouseVal": "target"}, inplace=True)
        housing_data["prediction"] = housing_data["target"].values + np.random.normal(
            0, 5, housing_data.shape[0]
        )
        self.reference = housing_data.sample(n=5000, replace=False)
        self.current = housing_data.sample(n=5000, replace=False)

        self.next(self.monitoring_data_quality)

    @mf.card(type="html")
    @mf.step
    def monitoring_data_quality(self):
        import os

        os.system("pip install evidently --quiet")
        from evidently.test_preset import DataStabilityTestPreset
        from evidently.test_suite import TestSuite

        from tools.helper_functions import get_evidently_html

        print("Monitoring: data quality tests")
        data_stability = TestSuite(
            tests=[
                DataStabilityTestPreset(),
            ]
        )
        data_stability.run(reference_data=self.reference, current_data=self.current)

        self.html = get_evidently_html(data_stability)

        self.next(self.end)

    @mf.step
    def end():
        print("Flow completed")
```

Which can be executed with the command:
```
$ python <path_to_the_metaflow_script>.py run
```

### Step 4. Visualize the report in the respective Card

The respective card can be visualized in multiple ways, such as via the optional Metaflow UI, the api client, or just simply using the command line interface:
```
$ python <path_to_the_metaflow_script>.py card view <step_name>
```
Here is an example of the Card in the Metaflow UI:
![Metaflow UI: card html](<../.gitbook/assets/metaflow_card_html.png>)
