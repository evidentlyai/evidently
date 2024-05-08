---
description: Set up an Evidently Cloud account or self-hosted workspace.
---   

# What is a Workspace?

You need a workspace to organize your data and Projects. 

* In Evidently Cloud, your account is your workspace. As simple as that! 
* In self-hosted deployments, a workspace means a remote or local directory where you store the snapshots. The Monitoring UI will read the data from this source. 

# Evidently Cloud 

If you do not have one yet, create an [Evidently Cloud account](https://app.evidently.cloud/signup).

**Get the API token**. You will use it to connect to the Evidently Cloud workspace from your Python environment. Use the "key" sign in the left menu to get to the token page, and click "generate token." Save it in a temporary file since it won't be visible once you leave the page.

**Connect to the workspace**. To connect to the Evidently Cloud workspace, you must first [install Evidently](../installation/install-evidently.md).

```python
pip install evidently
```

Then, run imports and pass your API token to connect: 

```python
from evidently.ui.workspace.cloud import CloudWorkspace

ws = CloudWorkspace(
token="YOUR_TOKEN_HERE",
url="https://app.evidently.cloud")
```

{% hint style="info" %}
**What's next?** Head to the next section to see how to [add your first Project](add_project.md).
{% endhint %}

# Self-hosting

## Local Workspace
In this scenario, you will generate, store the snapshots and run the monitoring UI on the same machine.

To create a local workspace and assign a name:

```python
ws = Workspace.create("evidently_ui_workspace")
```

You can pass a `path` parameter to specify the path to a local directory.

{% hint style="info" %}
**Code example** [Self-hosting tutorial](../get-started/tutorial-monitoring.md) shows a complete Python script to create and populate a local workspace.
{% endhint %}

# Remote Workspace

In this scenario, after generating the snapshots, you will send them to the remote server. You must run the Monitoring UI on the same remote server, so that it directly interfaces with the filesystem where the snapshots are stored.

To create a remote workspace (UI should be running at this address):

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

In the examples above, you store the snapshots and run the UI on the same server. Alternatively, you can store snapshots in a remote data store (such as an S3 bucket). In this case, the Monitoring UI service will interface with the designated data store to read the snapshot data.

To connect to data stores Evidently uses `fsspec` that allows accessing data on remote file systems via a standard Python interface. 

You can verify supported data stores in the [Fsspec documentation](https://filesystem-spec.readthedocs.io/en/latest/api.html#built-in-implementations](https://filesystem-spec.readthedocs.io/en/latest/api.html#other-known-implementations).

For example, to read snapshots from an S3 bucket (in this example we have MinIO running on localhost:9000), you must specify environment variables:

```
FSSPEC_S3_ENDPOINT_URL=http://localhost:9000/
FSSPEC_S3_KEY=my_key FSSPEC_S3_SECRET=my_secret
evidently ui --workspace s3://my_bucket/workspace
```

## Launch the UI service

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

To view the Evidently interface, go to URL http://localhost:8000 or a different specified port in your web browser.

## [DANGER] Delete workspace

If you want to delete an existing workspace (for example, an empty or a test workspace), run the command from the Terminal:

```
cd src/evidently/ui/
rm -r workspace
```

{% hint style="danger" %}
**You are deleting all the data**. This command will delete the snapshots stored in the folder. To maintain access to the generated snapshots, you must store them elsewhere.
{% endhint %}

# What’s next?

Regardless of the workspace type (cloud, local, or remote), you can use the same methods to create and manage Projects. Head to the next section to see how.

