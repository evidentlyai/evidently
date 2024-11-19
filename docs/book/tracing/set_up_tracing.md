---
description: Set up LLM tracing with tracely.
---   

For an end-to-end example, check the [Tracing Quickstart](../get-started/cloud_quickstart_tracing.md).

# Installation and Imports

Install the `tracely` package from PyPi.

```python
!pip install tracely 
```

Imports:

```python
from tracely import init_tracing
from tracely import trace_event
```

# Initialize tracing 

Use `init_tracing` to enable tracely tracing. Example:

```python
init_tracing(
   address="https://app.evidently.cloud/",
   api_key=”YOUR_EVIDENTLY_TOKEN”,
   project_id="YOUR_PROJECT_ID",
   export_name="YOUR_TRACING_DATASET_NAME",
   )
```

## Tracing parameters

| **Parameter**                  | **Description**                                                                                                                                                       |
|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `address: Optional[str]`       | The URL of the collector service where tracing data will be sent. For Evidently Cloud, set `https://app.evidently.cloud/`.<br>**Required:** No, **Default:** `None` |
| `exporter_type: Optional[str]` | Specifies the type of exporter to use for tracing. Options are `grpc` for gRPC protocol or `http` for HTTP protocol.<br>**Required:** No, **Default:** `None` |
| `api_key: Optional[str]`       | The authorization API key for Evidently Cloud tracing. This key authenticates your requests and is necessary for sending data to Evidently Cloud.<br>**Required:** No, **Default:** `None` |
| `project_id: str`       | The ID of your Project in Evidently Cloud. <br>**Required:** Yes, **Default:** `None` |
| `export_name: Optional[str]`   | A string name assigned to the exported tracing data. All data with the same `export_name` will be grouped into a single dataset.<br>**Required:** No, **Default:** `None` |
| `as_global: bool = True`       | Indicates whether to register the tracing provider globally for OpenTelemetry (`opentelemetry.trace.TracerProvider`) or use it locally within a scope. **Default:** `True` |

# Tracing a function

To trace a function call use `trace_event()` decorator. 

**Example 1.** To log all arguments of the function:

```
@trace_event()
```

**Example 2.** To log only input arguments of the function:

```
@trace_event(track_args=[])
```

**Example 3.** To log only "arg1" and "arg2":

```
@trace_event(track_args=["arg1", "arg2"])
```

See the [Tracing Quickstart](../get-started/cloud_quickstart_tracing.md) for an end-to-end example.

| **Parameter**                | **Description**                                                                                                                                                  |
|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `span_name: Optional[str]`   | The name of the span to track. This is how the event will be labeled in the trace. By giving it a name, you can identify and analyze this particular step within your tracing data.<br>**Required:** No, **Default:** `None` |
| `track_args: Optional[List[str]]` | A list of arguments to capture during tracing. If set to `None`, it captures all arguments by default. If set to `[]`, it captures no arguments.<br>**Required:** No, **Default:** `None` |
| `ignore_args: Optional[List[str]]` | A list of arguments to ignore from tracking. For instance, if a function has sensitive information that you don’t want to log, you can list those arguments here. If set to `None`, no arguments are ignored.<br>**Required:** No, **Default:** `None` |
| `track_output: Optional[bool]` | Indicates whether to track the output of the function call. If set to `True`, the trace will include the function’s output, allowing you to see not just what was passed in but also what was returned.<br>**Required:** No, **Default:** `True` |


