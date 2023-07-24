---
description: How to log data for Evidently monitoring.
---   

**TL;DR:** To track model and data quality in the Evidently monitoring UI, you need to save JSON `snapshots` that contain data and model summaries. 

# Code example

You can refer to an example How-to-notebook showing how to save and load JSON snapshots.

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_calculate_embeddings_drift.ipynb" %}

# Save and load snapshots 

## What is snapshot

A `snapshot` is a compressed representation of the Evidently Report or Test Suite. You can use these “snapshots” to log data and model performance.

This snapshot contains all the necessary information to recreate the initial Evidently Report or Test Suite. You can load the snapshot file and restore the visual Report or Test Suite. You can also export them as HTML files or in JSON or a Python dictionary format.

**Note**: This feature is different from using json() or save_json(“file.json”). When using the usual JSON export, you generate a structured output with limited information. You cannot convert this JSON back to HTML. With `snapshot`, you generate a comprehensive summary of the contents and can restore the output in any available Evidently format without accessing the initial raw data. 

## Save and load `snapshots`

To save the snapshot, use the `save` function and specify the path.

```python
data_drift_dataset_report._save(os.path.join(PATH, f”data_drift_profile.json’’))
```

To load the snapshot back, use the “load” function. 

```python
restored_report = Report._load(os.path.join(PATH, f”data_drift_profile.json’’))
restored_report
```

## Log `snapshots`

To enable Evidently Monitoring, you need to store these `snapshots` for different periods in a folder corresponding to the `workspace` and `project` name.


