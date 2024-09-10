---
description: How to self-host the open-source Evidently UI service.
---

In addition to using Evidently Python library, you can self-host the UI Service to get a monitoring Dashboard and organize the results of your evaluations. This is optional: you can also run evaluations and render results directly in Python or export them elsewhere.

{% hint style="info" %}
**Evidently Cloud.** Sign up for a free [Evidently Cloud](cloud_account.md) account to get a managed version with extra features.
{% endhint %}

{% hint style="info" %}
**Evidently Enterprise.** This page explains how to self-host the open-source platform. For the Enterprise version with extra features and support, [contact us](https://www.evidentlyai.com/get-demo). Host it in your cloud or on-premises.
{% endhint %}

To get a self-hostable Dashboard, you must:
1. Create a Workspace (local or remote) to store your data.
2. Launch the UI service.

# 1. Create a Workspace

Once you [install Evidently](install-evidently.md), you will need to create a `workspace`. This designates a remote or local directory where you will store the evaluation results (as JSON `snapshots` of the Evidently `Reports` or `Test Suites`). The UI Service will read the data from this source. 

There are three scenarios, based on where you run the UI Service and store data. 
* **Local Workspace**. Both the UI Service and data storage are local.
* **Remote Workspace**. Both the UI Service and data storage are remote.
* **Workspace with remote data storage**. You run the UI Service and store data on different servers.

## Local Workspace

In this scenario, you generate, store the snapshots and run the monitoring UI on the same machine.

Imports:
```python
from evidently.ui.workspace import Workspace
from evidently.ui.workspace import WorkspaceBase
```

To create a local Workspace and assign a name:

```python
ws = Workspace.create("evidently_ui_workspace")
```

You can pass a `path` parameter to specify the path to a local directory.

{% hint style="info" %}
**Code example**. [Self-hosting tutorial](../examples/tutorial-monitoring.md) shows a complete Python script to create and populate a local Workspace.
{% endhint %}

## Remote Workspace

In this scenario, you send the snapshots to a remote server. You must run the Monitoring UI on the same remote server. It will directly interface with the filesystem where the snapshots are stored.

Imports:

```
from evidently.ui.remote import RemoteWorkspace
from evidently.ui.workspace import Workspace
from evidently.ui.workspace import WorkspaceBase
```

To create a remote Workspace (UI should be running at this address):

```python
workspace = RemoteWorkspace("http://localhost:8000")
```

You can pass the following parameters:

| Parameter | Description |
|---|---|
| `self.base_url = base_url` | URL for the remote UI service. |
| `self.secret = secret` | String with secret, None by default. Use it if access to the URL is protected by a password. |

{% hint style="info" %}
**Code example**. See the [remote service example](https://github.com/evidentlyai/evidently/tree/main/examples/service).
{% endhint %}

## Remote snapshot storage

In the examples above, you store the snapshots and run the UI on the same server. Alternatively, you can store snapshots in a remote data store (such as an S3 bucket). The Monitoring UI service will interface with the designated data store to read the snapshot data.

To connect to data stores Evidently uses `fsspec` that allows accessing data on remote file systems via a standard Python interface. 

You can verify supported data stores in the Fsspec documentation: [built-in implementations](https://filesystem-spec.readthedocs.io/en/latest/api.html#built-in-implementations) and [other implementations](https://filesystem-spec.readthedocs.io/en/latest/api.html#other-known-implementations).

For example, to read snapshots from an S3 bucket (with MinIO running on localhost:9000), you must specify environment variables:

```
FSSPEC_S3_ENDPOINT_URL=http://localhost:9000/
FSSPEC_S3_KEY=my_key FSSPEC_S3_SECRET=my_secret
evidently ui --workspace s3://my_bucket/workspace
```

## [DANGER] Delete Workspace

To delete a Workspace (for example, an empty or a test Workspace), run the command from the Terminal:

```
cd src/evidently/ui/
rm -r workspace
```

{% hint style="danger" %}
**You are deleting all the data**. This command will delete the snapshots stored in the folder. To maintain access to the generated snapshots, you must store them elsewhere.
{% endhint %}

# 2. Launch the UI service

To launch the Evidently UI service, you must run a command in the Terminal.

**Option 1**. If you log snapshots to a local Workspace directory, you run Evidently UI over it. Run the following command from the directory where the Workspace folder is located.

```
evidently ui
```

**Option 2**. If you have your Project in a different Workspace, specify the path:

```
evidently ui --workspace . /workspace
```

**Option 3**. If you have your Project in a specified Workspace and run the UI service at the specific port (if the default port 8000 is occupied).

```
evidently ui --workspace ./workspace --port 8080
```

To view the Evidently interface, go to URL http://localhost:8000 or a specified port in your web browser.
