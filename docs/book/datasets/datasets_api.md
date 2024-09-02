---
description: Working with Datasets on Evidently Platform.
---   

To access or upload your Datasets, navigate to the [Datasets page](https://app.evidently.cloud/datasets) in the user interface. 

You will be able to view all Datasets: created from traces, uploaded directly to the platform, or generated as a result of an evaluation.

# User interface

## Upload a CSV file

Once you go to the Datasets page, you can upload any existing dataset as a CSV file directly there. Click on "Add dataset". 

When you upload the Dataset, you must also add a [column mapping](../input-data/column-mapping.md). This allows Evidently to understand the meaning of specific columns and prepare your Dataset for future evaluations.

# Python API

To work with Datasets programmatically from Python, you must first [connect to Workspace](../installation/cloud_account.md).

## Upload the Dataset

Prepare your dataset as a Pandas DataFrame. To upload a dataframe `df` to the specified Project in workspace `ws`, use the `add_dataset` method:

```python
ws.add_dataset(
    df,
    name = "dataset_name",
    project_id = project.id, 
    description = "Optional description")
```

You must always specify the "dataset_name" you want to see in the UI. The description is optional. 

To get a Project ID, grab it from the existing Project page or create a new Project first. (How to [work with Projects](../project/projects_overview.md).)  

## Download Dataset 

You can also download the Dataset from Evidently platform to your local environment. For example, if you store the test dataset on the platform and want to pull it into your local evaluation script.

Use the `load_dataset` method:

```python
downloaded_df = ws.load_dataset(dataset_id = "YOUR_DATASET_ID") 
```

## Include Dataset 

You can also include Datasets when you upload Reports or Test Suites to the platform. This way, after running an evaluation locally you simultaneously upload the evaluation result and the Dataset it was generated for, with added scores if applicable.

Use `include_data` parameter (False by default):

```python
ws.add_report(project.id, data_report, include_data=True)
```

This is optional. Check the docs on [generating snapshots](../evaluations/snapshots.md) for details.
